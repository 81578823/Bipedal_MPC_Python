# core/estimation/state_estimation_lkf.py

import yaml
import threading
import time
from typing import Optional, List

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy
from sensor_msgs.msg import Imu, JointState
from nav_msgs.msg import Odometry
import numpy as np
from core.gait.leg_logic import get_time_of_next_lift_off

# 假设trans.msg和trans.srv已经通过ROS 2接口生成

# 假设mujoco Python绑定已安装
from core.misc.buffer import Buffer      
from core.gait.mode_schedule import ModeSchedule  
from core.gait.motion_phase_definition import mode_number_to_stance_leg
from generation.pinocchio_interface import PinocchioInterface

class StateEstimationLKF:
    """
    StateEstimationLKF 类用于执行线性卡尔曼滤波器（LKF）状态估计，
    基于IMU、关节状态和里程计数据。
    """
    
    def __init__(self, node: Node):
        """
        初始化 StateEstimationLKF 实例。
        
        Args:
            node (Node): ROS 2 节点实例。
        """
        self.node = node
        
        # 加载配置文件
        config_file = self.node.get_parameter("/config_file").get_parameter_value().string_value
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
        except Exception as e:
            self.node.get_logger().error(f"Failed to load config file: {e}")
            raise e
        
        # 初始化机器人相关参数
        self.robot_name = config["model"]["name"]
        self.node.get_logger().info(f"robot_name: {self.robot_name}")
        
        model_package = config["model"]["package"]
        from ament_index_python.packages import get_package_share_directory
        urdf_path = get_package_share_directory(model_package) + config["model"]["urdf"]
        self.node.get_logger().info(f"model file: {urdf_path}")
        
        # 初始化 Pinocchio 接口
        self.pinocchio_interface = PinocchioInterface(urdf_path)
        
        self.foot_names = config["model"]["foot_names"]
        self.dt = config["estimation"]["dt"]
        self.use_odom = config["estimation"]["use_odom"]
        
        self.node.get_logger().info(f"dt: {self.dt}")
        self.node.get_logger().info(f"use odom: {'true' if self.use_odom else 'false'}")
        
        self.cflag = [True for _ in self.foot_names]
        
        for foot_name in self.foot_names:
            self.node.get_logger().info(f"foot name: {foot_name}")
        
        # 初始化缓冲区
        self.mode_schedule_buffer = Buffer[ModeSchedule]()
        self.qpos_ptr_buffer = Buffer[np.ndarray]()
        self.qvel_ptr_buffer = Buffer[np.ndarray]()
        self.imu_msg_buffer = Buffer[Imu]()
        self.joint_state_msg_buffer = Buffer[JointState]()
        self.odom_msg_buffer = Buffer[Odometry]()
        
        # 创建订阅者
        qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.BEST_EFFORT  # 适用于传感器数据
        )
        
        topic_prefix = config["global"]["topic_prefix"]
        imu_topic = config["global"]["topic_names"]["imu"]
        joints_topic = config["global"]["topic_names"]["joints_state"]
        odom_topic = config["global"]["topic_names"]["odom"]
        
        self.imu_subscription = self.node.create_subscription(
            Imu,
            topic_prefix + imu_topic,
            self.imu_callback,
            qos
        )
        
        self.joints_state_subscription = self.node.create_subscription(
            JointState,
            topic_prefix + joints_topic,
            self.joint_callback,
            qos
        )
        
        if self.use_odom:
            self.odom_subscription = self.node.create_subscription(
                Odometry,
                topic_prefix + odom_topic,
                self.odom_callback,
                qos
            )
        else:
            self.odom_subscription = None
        
        # 创建发布者
        self.odom_est_publisher = self.node.create_publisher(
            Odometry,
            topic_prefix + odom_topic + "_est",
            qos
        )
        
        self.setup()

        
        # 启动内部循环线程
        self.run_flag = True
        self.inner_loop_thread = threading.Thread(target=self.inner_loop)
        self.inner_loop_thread.start()
    
    def __del__(self):
        """
        析构函数，确保线程被正确关闭。
        """
        self.run_flag = False
        if self.inner_loop_thread.is_alive():
            self.inner_loop_thread.join()
    
    def getQpos(self) -> Optional[np.ndarray]:
        """
        获取当前估计的关节位置。
        
        Returns:
            Optional[np.ndarray]: 关节位置向量。
        """
        return self.qpos_ptr_buffer.get()
    
    def getQvel(self) -> Optional[np.ndarray]:
        """
        获取当前估计的关节速度。
        
        Returns:
            Optional[np.ndarray]: 关节速度向量。
        """
        return self.qvel_ptr_buffer.get()
    
    def setContactFlag(self, flag: List[bool]):
        """
        设置接触标志。
        
        Args:
            flag (List[bool]): 每个足的接触标志。
        """
        self.cflag = flag
    
    def setImuMsg(self, msg: Imu):
        """
        设置IMU消息。
        
        Args:
            msg (Imu): IMU消息。
        """
        if msg.header.frame_id == self.robot_name:
            self.imu_msg_buffer.push(msg)
    
    def setJointsMsg(self, msg: JointState):
        """
        设置关节状态消息。
        
        Args:
            msg (JointState): 关节状态消息。
        """
        if msg.header.frame_id == self.robot_name:
            self.joint_state_msg_buffer.push(msg)
    
    def updateModeSchedule(self, mode_schedule: ModeSchedule):
        """
        更新模式调度。
        
        Args:
            mode_schedule (ModeSchedule): 模式调度实例。
        """
        self.mode_schedule_buffer.push(mode_schedule)
    
    def setup(self):
        """
        设置初始状态和协方差矩阵。
        """        
        self.x_est = np.zeros((12, 1))  # 状态估计向量
        self.x_est[2, 0] = 0.5  # 设置z轴位置初始值
        self.ps = np.zeros((6, 1))
        self.vs = np.zeros((6, 1))
        # 初始化状态向量和矩阵
        self.A = np.eye(12)
        self.A[0:3, 3:6] = np.eye(3) * self.dt
        self.B = np.zeros((12, 3))
        self.B[3:6, 0:3] = np.eye(3) * self.dt
        self.C = np.zeros((14, 12))
        
        C1 = np.zeros((3, 6))
        C1[0:3, 0:3] = np.eye(3)
        C2 = np.zeros((3, 6))
        C2[0:3, 3:6] = np.eye(3)
        
        self.C[0:3, 0:6] = C1
        self.C[3:6, 0:6] = C1
        self.C[0:6, 6:12] = -np.eye(6)
        self.C[6:9, 0:6] = C2
        self.C[9:12, 0:6] = C2
        self.C[12, 8] = 1.0
        self.C[13, 11] = 1.0
        
        self.Sigma = np.zeros((12, 12))
        np.fill_diagonal(self.Sigma, 100.0)
        self.Q0 = np.eye(12)
        self.Q0[0:3, 0:3] *= self.dt / 20.0
        self.Q0[3:6, 3:6] *= (self.dt * 9.81) / 20.0
        self.Q0[6:12, 6:12] *= self.dt
        self.R0 = np.eye(14)
        
        # 噪声参数
        self.noise_pimu = 0.02
        self.noise_vimu = 0.02
        self.noise_pfoot = 0.002
        self.noise_pimu_rel_foot = 0.001
        self.noise_vimu_rel_foot = 0.1
        self.noise_zfoot = 0.001

    def angularMotionEstimate(self, imu_data: Imu, qpos: np.ndarray, qvel: np.ndarray):
        """
        基于IMU数据进行角度估计。
        
        Args:
            imu_data (Imu): IMU消息。
            qpos (np.ndarray): 关节位置向量。
            qvel (np.ndarray): 关节速度向量。
        """
        quat_imu = imu_data.orientation
        quat = np.array([quat_imu.w, quat_imu.x, quat_imu.y, quat_imu.z])
        qpos[3:7] = [quat_imu.x, quat_imu.y, quat_imu.z, quat_imu.w]
        qvel[3:6] = [
            imu_data.angular_velocity.x,
            imu_data.angular_velocity.y,
            imu_data.angular_velocity.z
        ]
    
    def linearMotionEstimate(self, imu_data: Imu, qpos: np.ndarray, qvel: np.ndarray):
        """
        基于IMU数据进行线性加速度估计。
        
        Args:
            imu_data (Imu): IMU消息。
            qpos (np.ndarray): 关节位置向量。
            qvel (np.ndarray): 关节速度向量。
        """
        quat = np.array([imu_data.orientation.w, imu_data.orientation.x,
                         imu_data.orientation.y, imu_data.orientation.z])
        b_acc = np.array([
            imu_data.linear_acceleration.x,
            imu_data.linear_acceleration.y,
            imu_data.linear_acceleration.z
        ])
        rot_matrix = self.quaternion_to_rotation_matrix(quat)
        w_acc = rot_matrix @ b_acc
        g = np.array([0.0, 0.0, -9.81])
        w_acc += g
        
        # 构建Q和R矩阵
        Q = np.eye(12)
        Q[0:3, 0:3] = self.Q0[0:3, 0:3] * self.noise_pimu
        Q[3:6, 3:6] = self.Q0[3:6, 3:6] * self.noise_vimu
        Q[6:12, 6:12] = self.Q0[6:12, 6:12] * self.noise_pfoot
        
        R = np.eye(14)
        R[0:6, 0:6] = self.R0[0:6, 0:6] * self.noise_pimu_rel_foot
        R[6:12, 6:12] = self.R0[6:12, 6:12] * self.noise_vimu_rel_foot
        R[12, 12] = self.R0[12, 12] * self.noise_zfoot
        R[13, 13] = self.R0[13, 13] * self.noise_zfoot

        self.q_idx = 0
        self.idx1 = 0
        self.idx2 = 0

        self.pzs= np.zeros((4, 1))
        
        # 获取关节位置信息
        p0 = self.x_est[0:3, 0]
        v0 = self.x_est[3:6, 0]
        
        # 更新Pinocchio接口
        self.pinocchio_interface.updateRobotState(qpos, qvel)
        mode_schedule = self.mode_schedule_buffer.get()
        if mode_schedule is None:
            self.node.get_logger().warn("ModeSchedule is not available.")
            return
        
        contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(0.0))
        ntlo = get_time_of_next_lift_off(0,mode_schedule)
        gait_cycle = mode_schedule.gait_cycle()
        
        release_ = (abs(w_acc[2]) < 1.0)
        for flag in contact_flag:
            release_ &= (not flag)
        
        for i, foot_name in enumerate(self.foot_names):
            pose = self.pinocchio_interface.getFramePose(foot_name)
            v = self.pinocchio_interface.getFrame6dVel_localWorldAligned(foot_name)
            p_f = pose.translation - np.array([0.0, 0.0, 0.02])  # 减去脚底半径
            v_f = v.linear
            
            q_idx = 6 + 3 * i
            idx1 = 6 + 3 * i
            idx2 = 12 + i
            
            trust = 1.0
            if contact_flag[i] or release_:
                trust_window = 0.15
                contact_phase = 1.0 - ntlo[i] / (0.5 * gait_cycle)
                if contact_phase < trust_window:
                    trust = contact_phase / trust_window
                elif contact_phase > (1.0 - trust_window):
                    trust = (1.0 - contact_phase) / trust_window
            else:
                trust = 0.0
            
            high_suspect_number = 500.0
            
            Q[q_idx:q_idx+3, q_idx:q_idx+3] *= (1.0 + (1.0 - trust) * high_suspect_number)
            R[idx1, idx1] *= (1.0 + (1.0 - trust) * high_suspect_number)
            R[idx2, idx2] *= (1.0 + (1.0 - trust) * high_suspect_number)
            
            self.ps[3*i:3*i+3, 0] = -p_f
            self.pzs[i, 0] = (1.0 - trust) * (p0[2]+p_f[2])
            self.vs[3*i:3*i+3, 0] = (1.0 - trust) * v0 + trust * (-v_f)
        
        # print("self.pzs",self.pzs)
        y = np.concatenate([self.ps.flatten(), self.vs.flatten(), self.pzs[:2, 0]]).reshape(14, 1)    # maybe bug
        x_pred = self.A @ self.x_est + self.B @ w_acc.reshape(3, 1)
        
        Sigma_bar = self.A @ self.Sigma @ self.A.T + Q
        S = self.C @ Sigma_bar @ self.C.T + R
        # print("C.shape",self.C.shape)
        # print("x_pred.shape",x_pred.shape)
        # print("C@x_pred.shape",(self.C @ x_pred).shape)
        # print("y.shape",y.shape)
        # print("S.shape",S.shape)    
        # print("y - self.C @ x_pred.shape",(y - self.C @ x_pred).shape)
        correct = np.linalg.solve(S, (y - self.C @ x_pred)).reshape(-1, 1)
        self.x_est = x_pred + Sigma_bar @ self.C.T @ correct
        SC_ = np.linalg.solve(S, self.C)
        self.Sigma = (np.eye(12) - Sigma_bar @ self.C.T @ SC_) @ Sigma_bar
        self.Sigma = 0.5 * (self.Sigma + self.Sigma.T)
        
        if np.linalg.det(self.Sigma[0:2, 0:2]) > 1e-6:
            self.Sigma[0:2, 6:12] = 0.0
            self.Sigma[6:12, 0:2] = 0.0
            self.Sigma[0:2, 0:2] *= 0.1
        
        qpos[0:3] = self.x_est[0:3, 0]
        qvel[0:3] = self.quaternion_to_rotation_matrix(quat).T @ self.x_est[3:6, 0]
    
    def imu_callback(self, msg: Imu):
        """
        IMU消息回调函数。
        
        Args:
            msg (Imu): 接收到的IMU消息。
        """
        if msg.header.frame_id == self.robot_name:
            self.imu_msg_buffer.push(msg)
    
    def joint_callback(self, msg: JointState):
        """
        关节状态消息回调函数。
        
        Args:
            msg (JointState): 接收到的关节状态消息。
        """
        if msg.header.frame_id == self.robot_name:
            self.joint_state_msg_buffer.push(msg)
    
    def odom_callback(self, msg: Odometry):
        """
        里程计消息回调函数。
        
        Args:
            msg (Odometry): 接收到的里程计消息。
        """
        if msg.header.frame_id == self.robot_name:
            self.odom_msg_buffer.push(msg)
    
    def inner_loop(self):
        """
        内部循环线程，执行状态估计。
        """
        # rate = self.node.create_rate(1.0 / self.dt)
        loop_rate = self.dt
        t0 = self.node.get_clock().now().nanoseconds*1e-9
        
        while rclpy.ok() and self.run_flag:
            start_time = time.time()
            if (self.imu_msg_buffer.get() is None or
                self.mode_schedule_buffer.get() is None or
                self.joint_state_msg_buffer.get() is None or
                (self.use_odom and self.odom_msg_buffer.get() is None)):
                continue
            
            imu_msg = self.imu_msg_buffer.get()
            joint_state_msg = self.joint_state_msg_buffer.get()
            odom_msg = self.odom_msg_buffer.get() if self.use_odom else None
            
            model = self.pinocchio_interface.getModel()
            qpos_ptr = np.zeros(model.nq)
            qvel_ptr = np.zeros(model.nv)
            
            for k, name in enumerate(joint_state_msg.name):
                if k < model.njoints and model.existJointName(name):
                    joint_id = model.getJointId(name) - 2
                    if 0 <= (joint_id + 7) < len(qpos_ptr):
                        qpos_ptr[joint_id + 7] = joint_state_msg.position[k]
                    if 0 <= (joint_id + 6) < len(qvel_ptr):
                        qvel_ptr[joint_id + 6] = joint_state_msg.velocity[k]
            
            if self.use_odom and odom_msg is not None:
                orientation = odom_msg.pose.pose.orientation
                position = odom_msg.pose.pose.position
                vel = odom_msg.twist.twist.linear
                ang_vel = odom_msg.twist.twist.angular
                
                quat = np.array([orientation.w, orientation.x, orientation.y, orientation.z])
                rot_matrix = self.quaternion_to_rotation_matrix(quat)
                qpos_ptr[0:3] = [position.x, position.y, position.z]
                qvel_ptr[0:3] = rot_matrix.T @ np.array([vel.x, vel.y, vel.z])
                qpos_ptr[3:7] = [orientation.x, orientation.y, orientation.z, orientation.w]
                qvel_ptr[3:6] = [ang_vel.x, ang_vel.y, ang_vel.z]
            else:
                self.angularMotionEstimate(imu_msg, qpos_ptr, qvel_ptr)
                self.linearMotionEstimate(imu_msg, qpos_ptr, qvel_ptr)
            
            if self.node.get_clock().now().nanoseconds*1e-9 - t0 > 0.3:
                self.qpos_ptr_buffer.push(qpos_ptr)
                self.qvel_ptr_buffer.push(qvel_ptr)
            
            # 发布估计的里程计消息
            est_odom = Odometry()
            est_odom.header.frame_id = self.robot_name
            est_odom.header.stamp = self.node.get_clock().now().to_msg()
            est_odom.pose.pose.position.x = qpos_ptr[0]
            est_odom.pose.pose.position.y = qpos_ptr[1]
            est_odom.pose.pose.position.z = qpos_ptr[2]
            est_odom.pose.pose.orientation.w = qpos_ptr[6]
            est_odom.pose.pose.orientation.x = qpos_ptr[3]
            est_odom.pose.pose.orientation.y = qpos_ptr[4]
            est_odom.pose.pose.orientation.z = qpos_ptr[5]
            
            quat = np.array([qpos_ptr[6], qpos_ptr[3], qpos_ptr[4], qpos_ptr[5]])
            rot_matrix = self.quaternion_to_rotation_matrix(quat)
            vel_world = rot_matrix @ qvel_ptr[0:3]
            est_odom.twist.twist.linear.x = vel_world[0]
            est_odom.twist.twist.linear.y = vel_world[1]
            est_odom.twist.twist.linear.z = vel_world[2]
            est_odom.twist.twist.angular.x = qvel_ptr[3]
            est_odom.twist.twist.angular.y = qvel_ptr[4]
            est_odom.twist.twist.angular.z = qvel_ptr[5]
            
            self.odom_est_publisher.publish(est_odom)

            # rate.sleep()
            
            now = time.time()
            if now - start_time < loop_rate:
                time.sleep(loop_rate-(now - start_time))
    
    def quaternion_to_rotation_matrix(self, quat: np.ndarray) -> np.ndarray:
        """
        将四元数转换为旋转矩阵。
        
        Args:
            quat (np.ndarray): 四元数 [w, x, y, z]
        
        Returns:
            np.ndarray: 3x3旋转矩阵
        """
        w, x, y, z = quat
        rot_matrix = np.array([
            [1 - 2*(y**2 + z**2),     2*(x*y - z*w),         2*(x*z + y*w)],
            [2*(x*y + z*w),           1 - 2*(x**2 + z**2),   2*(y*z - x*w)],
            [2*(x*z - y*w),           2*(y*z + x*w),         1 - 2*(x**2 + y**2)]
        ])
        return rot_matrix

