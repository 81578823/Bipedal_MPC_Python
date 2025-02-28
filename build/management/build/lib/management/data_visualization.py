# core/gait/data_visualization.py

import yaml
import numpy as np
import threading
import time
from typing import Dict, Tuple, List, Optional
import pinocchio as pin
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped, Point
from visualization_msgs.msg import Marker, MarkerArray
import tf2_ros
from core.types import scalar_t, vector3_t, vector_t
from generation.pinocchio_interface import PinocchioInterface
from core.trajectory.reference_buffer import ReferenceBuffer
from generation.foothold_optimization import FootholdOptimization
from generation.convex_mpc import ConvexMPC
from core.misc.buffer import Buffer
from core.misc.benchmark import RepeatedTimer
from core.misc.numeric_traits import limit_epsilon
from core.trajectory.cubic_spline_trajectory import CubicSplineTrajectory, CubicSplineInterpolation
import rclpy

class DataVisualization:
    """
    DataVisualization 类用于可视化机器人的状态、足部位置和轨迹。
    """

    def __init__(self, node_handle: Node):
        """
        初始化 DataVisualization 实例。

        Args:
            node_handle (Node): ROS 2 节点句柄。
        """
        self.node_handle = node_handle

        # 从参数服务器获取配置文件路径
        try:
            config_file = self.node_handle.get_parameter("/config_file").value
            self.load_config(config_file)
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to get config_file parameter: {e}")
            raise e

        # 获取模型包和URDF路径
        try:
            model_package = self.config_["model"]["package"]
            urdf_relative_path = self.config_["model"]["urdf"]
            from ament_index_python.packages import get_package_share_directory
            urdf_path = get_package_share_directory(model_package) + urdf_relative_path
            self.node_handle.get_logger().info(f"Model file: {urdf_path}")
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to load URDF path: {e}")
            raise e

        # 初始化 PinocchioInterface
        self.pinocchio_interface = PinocchioInterface(urdf_path)

        # 初始化足部名称、基座名称和关节名称
        self.foot_names = self.config_["model"]["foot_names"]
        self.actuated_joints_name = self.config_["model"]["actuated_joints_name"]
        self.base_name = self.config_["model"]["base_name"]

        self.node_handle.get_logger().info(f"[DataVisualization] Base name: {self.base_name}")

        # 初始化 ROS 发布者和 TF 广播器
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self.node_handle)
        self.joint_state_publisher = self.node_handle.create_publisher(JointState, "joint_states", qos_profile)
        topic_prefix = self.config_["global"]["topic_prefix"]
        self.footholds_pub = self.node_handle.create_publisher(MarkerArray, f"{topic_prefix}footholds_vis", qos_profile)
        self.foot_traj_msg_publisher = self.node_handle.create_publisher(MarkerArray, f"{topic_prefix}foot_traj_vis", qos_profile)
        self.foot_traj_ref_msg_publisher = self.node_handle.create_publisher(MarkerArray, f"{topic_prefix}foot_traj_ref_vis", qos_profile)
        self.base_traj_pub = self.node_handle.create_publisher(Marker, f"{topic_prefix}base_trajectory", qos_profile)
        self.base_traj_ref_pub = self.node_handle.create_publisher(Marker, f"{topic_prefix}base_trajectory_ref", qos_profile)

        # 初始化可视化标记
        self.initialize_markers()

        # 初始化缓冲区
        self.qpos_ptr_buffer = Buffer[vector_t]()
        self.qvel_ptr_buffer = Buffer[vector_t]()

        # 初始化 ReferenceBuffer
        self.reference_buffer: Optional[ReferenceBuffer] = None

        # 初始化线程控制
        self.run = Buffer[bool]()
        self.run.push(True)

        # 初始化 ReferenceBuffer
        # ReferenceBuffer 的初始化将在 updateReferenceBuffer 中完成

        # 启动内部循环线程
        self.inner_loop_thread = threading.Thread(target=self.inner_loop)
        self.inner_loop_thread.start()

    def load_config(self, config_file: str):
        """
        加载配置文件，初始化模型名称和足部名称。

        Args:
            config_file (str): 配置文件路径。
        """
        try:
            with open(config_file, 'r') as file:
                self.config_ = yaml.safe_load(file)
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to load config file: {e}")
            raise e

    def initialize_markers(self):
        """
        初始化可视化标记的属性。
        """
        # 初始化基座轨迹标记
        self.line_strip_base = Marker()
        self.line_strip_base.header.frame_id = "world"
        self.line_strip_base.action = Marker.ADD
        self.line_strip_base.type = Marker.LINE_STRIP
        self.line_strip_base.scale.x = 0.01
        self.line_strip_base.scale.y = 0.01
        self.line_strip_base.scale.z = 0.01
        self.line_strip_base.color.a = 0.6
        self.line_strip_base.color.r = 0.0
        self.line_strip_base.color.g = 0.0
        self.line_strip_base.color.b = 0.0
        self.line_strip_base.ns = self.base_name

        # 初始化基座参考轨迹标记
        self.line_strip_base_ref = Marker()
        self.line_strip_base_ref.header.frame_id = "world"
        self.line_strip_base_ref.action = Marker.ADD
        self.line_strip_base_ref.type = Marker.LINE_STRIP
        self.line_strip_base_ref.scale.x = 0.01
        self.line_strip_base_ref.scale.y = 0.01
        self.line_strip_base_ref.scale.z = 0.01
        self.line_strip_base_ref.color.a = 0.6
        self.line_strip_base_ref.color.r = 1.0
        self.line_strip_base_ref.color.g = 0.0
        self.line_strip_base_ref.color.b = 0.0
        self.line_strip_base_ref.ns = self.base_name

        # 初始化足部轨迹标记
        self.line_strip_foot_traj_ = MarkerArray()
        self.line_strip_foot_traj_.markers = [Marker() for _ in self.foot_names]
        self.line_strip_foot_traj_ref_ = MarkerArray()
        self.line_strip_foot_traj_ref_.markers = [Marker() for _ in self.foot_names]
        self.line_strip_footholds_ = MarkerArray()
        self.line_strip_footholds_.markers = [Marker() for _ in self.foot_names]

        for i, foot_name in enumerate(self.foot_names):
            # 足部轨迹标记
            marker = self.line_strip_foot_traj_.markers[i]
            marker.header.frame_id = "world"
            marker.action = Marker.ADD
            marker.type = Marker.LINE_STRIP
            marker.color.a = 0.6
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.scale.x = 0.01
            marker.scale.y = 0.01
            marker.scale.z = 0.01
            marker.ns = foot_name

            # 足部参考轨迹标记
            ref_marker = self.line_strip_foot_traj_ref_.markers[i]
            ref_marker.header.frame_id = "world"
            ref_marker.action = Marker.ADD
            ref_marker.type = Marker.LINE_STRIP
            ref_marker.color.a = 0.6
            ref_marker.color.r = 1.0
            ref_marker.color.g = 0.0
            ref_marker.color.b = 0.0
            ref_marker.scale.x = 0.01
            ref_marker.scale.y = 0.01
            ref_marker.scale.z = 0.01
            ref_marker.ns = foot_name

            # 足部支撑点标记
            foothold_marker = self.line_strip_footholds_.markers[i]
            foothold_marker.header.frame_id = "world"
            foothold_marker.action = Marker.ADD
            foothold_marker.type = Marker.SPHERE_LIST
            foothold_marker.color.a = 0.7
            foothold_marker.color.r = 0.0
            foothold_marker.color.g = 0.6
            foothold_marker.color.b = 0.6
            foothold_marker.scale.x = 0.04
            foothold_marker.scale.y = 0.04
            foothold_marker.scale.z = 0.04
            foothold_marker.ns = foot_name

    def __del__(self):
        """
        析构函数。停止内部循环线程并等待其结束。
        """
        self.run.push(False)
        if self.inner_loop_thread.is_alive():
            self.inner_loop_thread.join()

    def update_current_state(self, qpos_ptr: vector_t, qvel_ptr: vector_t):
        """
        更新当前的关节位置和速度状态。

        Args:
            qpos_ptr (vector_t): 关节位置向量。
            qvel_ptr (vector_t): 关节速度向量。
        """
        self.qpos_ptr_buffer.push(qpos_ptr)
        self.qvel_ptr_buffer.push(qvel_ptr)

    def update_reference_buffer(self, reference_buffer: ReferenceBuffer):
        """
        更新 ReferenceBuffer 实例。

        Args:
            reference_buffer (ReferenceBuffer): ReferenceBuffer 实例。
        """
        self.reference_buffer = reference_buffer

    def inner_loop(self):
        """
        内部循环，定期执行数据发布。
        """
        loop_rate = 1.0 / 500.0 

        # self.node_handle.get_logger().info("Start DataVisualization loop")

        time.sleep(0.01)  # Sleep 10ms
        iter_count = 0

        while self.run.get() and rclpy.ok():        
            next_time = time.time()  # 获取当前时间

            if self.qpos_ptr_buffer.get() is None or self.qvel_ptr_buffer.get() is None:
                time.sleep(0.005)  # Sleep 5ms
                continue

            qpos_ptr = self.qpos_ptr_buffer.get()
            qvel_ptr = self.qvel_ptr_buffer.get()

            # 更新机器人状态
            self.pinocchio_interface.updateRobotState(qpos_ptr, qvel_ptr)

            # 发布当前状态
            self.publish_current_state()

            if self.reference_buffer is None or not self.reference_buffer.isReady():
                continue

            # 每隔一定次数发布足部轨迹和基座轨迹
            if iter_count % 5 == 0:
                self.publish_foot_trajectory()
            if iter_count % 10 == 0:
                self.publish_base_trajectory()
            if iter_count % 50 == 0:
                self.publish_footholds()            
            
            iter_count += 1
            now = time.time()
            elapsed_time = now - next_time
            if elapsed_time < loop_rate:
                time.sleep(loop_rate - elapsed_time)

        self.node_handle.get_logger().info("[DataVisualization] Loop terminated")

    def publish_footholds(self):
        """
        发布足部支撑点的可视化标记。
        """
        footholds = self.reference_buffer.getFootholds()
        if not footholds:
            return
        if len(footholds) != len(self.foot_names):
            self.node_handle.get_logger().warn("Footholds size mismatch")
            return

        for i, foot_name in enumerate(self.foot_names):
            marker = self.line_strip_footholds_.markers[i]
            marker.header.stamp = self.node_handle.get_clock().now().to_msg()
            marker.points.clear()
            pos = footholds[foot_name][1]
            point = Point(x=pos[0], y=pos[1], z=pos[2])
            marker.points.append(point)

        self.footholds_pub.publish(self.line_strip_footholds_)

    def publish_base_trajectory(self):
        """
        发布基座轨迹的可视化标记。
        """
        base_pos_traj_int = self.reference_buffer.getLipBasePosTraj()
        base_pos_traj = self.reference_buffer.getOptimizedBasePosTraj()
        if base_pos_traj_int is None or base_pos_traj is None:
            return

        # 发布基座当前轨迹
        self.line_strip_base.header.stamp = self.node_handle.get_clock().now().to_msg()
        self.line_strip_base.points.clear()
        time_dur1 = base_pos_traj_int.duration()
        for i in range(int(time_dur1 / 0.02)):
            pos = base_pos_traj_int.evaluate(i * 0.02 + base_pos_traj_int.ts())
            point = Point(x=pos[0], y=pos[1], z=pos[2])
            self.line_strip_base.points.append(point)
        self.base_traj_pub.publish(self.line_strip_base)

        # 发布基座参考轨迹
        self.line_strip_base_ref.header.stamp = self.node_handle.get_clock().now().to_msg()
        self.line_strip_base_ref.points.clear()
        time_dur2 = base_pos_traj.duration()
        for i in range(int(time_dur2 / 0.02)):
            pos = base_pos_traj.evaluate(i * 0.02 + base_pos_traj.ts())
            point = Point(x=pos[0], y=pos[1], z=pos[2])
            self.line_strip_base_ref.points.append(point)
        self.base_traj_ref_pub.publish(self.line_strip_base_ref)

    def publish_foot_trajectory(self):
        """
        发布足部轨迹的可视化标记。
        """
        foot_traj = self.reference_buffer.getFootPosTraj()
        if len(foot_traj) != len(self.foot_names):
            self.node_handle.get_logger().warn("Foot trajectories size mismatch")
            return

        for i, foot_name in enumerate(self.foot_names):
            marker = self.line_strip_foot_traj_.markers[i]
            ref_marker = self.line_strip_foot_traj_ref_.markers[i]

            marker.header.stamp = self.node_handle.get_clock().now().to_msg()
            ref_marker.header.stamp = self.node_handle.get_clock().now().to_msg()

            # 限制轨迹点数量
            if len(marker.points) > 200:
                marker.points.pop(0)

            # 添加当前足部位置到轨迹
            pos = self.pinocchio_interface.getFramePose(foot_name).translation
            point = Point(x=pos[0], y=pos[1], z=pos[2])
            marker.points.append(point)

            # 更新参考轨迹
            ref_marker.points.clear()
            foot_traj_i = foot_traj[foot_name]
            time_dur = foot_traj_i.duration()
            for j in range(int(time_dur / 0.02)):
                pos = foot_traj_i.evaluate(j * 0.02 + foot_traj_i.ts())
                point = Point(x=pos[0], y=pos[1], z=pos[2])
                ref_marker.points.append(point)

        self.foot_traj_msg_publisher.publish(self.line_strip_foot_traj_)
        self.foot_traj_ref_msg_publisher.publish(self.line_strip_foot_traj_ref_)

    def publish_current_state(self):
        """
        发布当前机器人的状态，包括基座位姿和关节状态。
        """
        # 发布基座位姿
        base_pose_msg = TransformStamped()
        base_pose = self.pinocchio_interface.getFramePose(self.base_name)
        quat = self.to_quaternion(base_pose.rotation)

        base_pose_msg.header.stamp = self.node_handle.get_clock().now().to_msg()
        base_pose_msg.header.frame_id = "world"
        base_pose_msg.child_frame_id = self.base_name
        base_pose_msg.transform.translation.x = base_pose.translation[0]
        base_pose_msg.transform.translation.y = base_pose.translation[1]
        base_pose_msg.transform.translation.z = base_pose.translation[2]
        base_pose_msg.transform.rotation.w = quat.w
        base_pose_msg.transform.rotation.x = quat.x
        base_pose_msg.transform.rotation.y = quat.y
        base_pose_msg.transform.rotation.z = quat.z

        # 发布关节状态
        jnt_state_msg = JointState()
        jnt_state_msg.header.stamp = self.node_handle.get_clock().now().to_msg()
        jnt_state_msg.name = []
        jnt_state_msg.position = []
        model = self.pinocchio_interface.getModel()
        qpos = self.qpos_ptr_buffer.get()
        if qpos is None:
            qpos = np.zeros(self.pinocchio_interface.nq())
        for joint_name in self.actuated_joints_name:
            if model.existJointName(joint_name):
                joint_id = model.getJointId(joint_name)
                # 注意：根据您的Pinocchio模型，可能需要调整索引
                # 这里假设关节位置从7开始
                pos = qpos[joint_id + 7] if joint_id + 7 < len(qpos) else 0.0
                jnt_state_msg.name.append(joint_name)
                jnt_state_msg.position.append(pos)

        # 发送TF和关节状态
        self.tf_broadcaster.sendTransform(base_pose_msg)
        self.joint_state_publisher.publish(jnt_state_msg)

    @staticmethod
    def to_quaternion(rotation_matrix: np.ndarray) -> pin.Quaternion:
        """
        将旋转矩阵转换为四元数。

        Args:
            rotation_matrix (np.ndarray): 3x3旋转矩阵。

        Returns:
            pin.Quaternion: 四元数表示。
        """
        quat = pin.Quaternion()
        quat = pin.Quaternion(rotation_matrix)
        return quat

