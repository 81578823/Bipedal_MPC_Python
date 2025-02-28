# trajectory_stabilization.py

import threading
import time
from typing import Optional, List
import numpy as np
import yaml
import rclpy
from rclpy.node import Node
from .whole_body_controller import ActuatorCommands
from .matrix_db import MatrixDB
from core.trajectory.reference_buffer import ReferenceBuffer
from core.misc.buffer import Buffer
from .whole_body_controller import WholeBodyController
from trans.msg import ActuatorCmds  # 确保此消息类型已定义并可导入
import pinocchio as pin
from ament_index_python.packages import get_package_share_directory
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy
from generation.pinocchio_interface import PinocchioInterface
from core.misc.benchmark import RepeatedTimer

vector_t = np.ndarray  # 1D数组
matrix_t = np.ndarray  # 2D数组
scalar_t = float

class TrajectoryStabilization:
    def __init__(self, node_handle: Node):
        self.node_handle = node_handle

        # 读取配置文件
        config_file = self.node_handle.get_parameter("/config_file").value
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        topic_prefix = config["global"]["topic_prefix"]
        actuators_cmds_topic = config["global"]["topic_names"]["actuators_cmds"]
        self.log_dir = config["global"]["log_dir"]
        self.freq = config["controller"]["frequency"]
        self.node_handle.get_logger().info(f"frequency: {self.freq}")

        self.actuated_joints_name = config["model"]["actuated_joints_name"]
        self.joints_default_pos = config["model"]["default"]["joint_pos"]
        self.robot_name = config["model"]["name"]

        qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE
        )
        
        self.actuators_cmds_pub = self.node_handle.create_publisher(
            ActuatorCmds,
            topic_prefix + actuators_cmds_topic,
            qos
        )

        model_package = config["model"]["package"]
        urdf_relative_path = config["model"]["urdf"]
        urdf_path = get_package_share_directory(model_package) + urdf_relative_path
        self.node_handle.get_logger().info(f"Model file: {urdf_path}")

        self.pinocchioInterface_ptr = PinocchioInterface(urdf_path)

        self.base_name = config["model"]["base_name"]

        # 初始化PinocchioInterface（假设它是WholeBodyController的一部分）
        # 如果有单独的PinocchioInterface类，请相应调整
        # 这里我们直接使用WholeBodyController

        self.run_buffer = Buffer[bool]()
        self.run_buffer.push(True)

        self.wbc = WholeBodyController(node_handle)

        # 初始化Buffers
        self.qpos_ptr_buffer = Buffer[Optional[vector_t]]()
        self.qvel_ptr_buffer = Buffer[Optional[vector_t]]()
        self.actuator_commands_buffer = Buffer[Optional[ActuatorCommands]]()

        self.reference_buffer: Optional[ReferenceBuffer] = None

        # 启动内循环线程
        self.inner_loop_thread = threading.Thread(target=self.inner_loop, daemon=True)
        self.inner_loop_thread.start()

    def __del__(self):
        # 停止内循环线程
        self.run_buffer.push(False)
        self.inner_loop_thread.join()

    def update_current_state(self, qpos_ptr: vector_t, qvel_ptr: vector_t):
        self.qpos_ptr_buffer.push(qpos_ptr)
        self.qvel_ptr_buffer.push(qvel_ptr)

    def update_reference_buffer(self, reference_buffer: ReferenceBuffer):
        self.reference_buffer = reference_buffer

    def get_cmds(self) -> Optional[ActuatorCmds]:
        actuator_commands = self.actuator_commands_buffer.get()
        if actuator_commands is None:
            return None

        msg = ActuatorCmds()
        msg.header.frame_id = self.robot_name
        msg.header.stamp = self.node_handle.get_clock().now().to_msg()

        model = self.pinocchioInterface_ptr.model_
        for joint_name in self.actuated_joints_name:
            # print("model.existJointName(joint_name): ", model.existJointName(joint_name))   
            if model.existJointName(joint_name):
                joint_id = model.getJointId(joint_name) - 2  # 根据C++代码的偏移
                msg.names.append(joint_name)
                msg.gain_p.append(actuator_commands.Kp[joint_id])
                msg.pos_des.append(actuator_commands.pos[joint_id])
                msg.gaid_d.append(actuator_commands.Kd[joint_id])
                msg.vel_des.append(actuator_commands.vel[joint_id])
                msg.feedforward_torque.append(actuator_commands.torque[joint_id])
        return msg

    def publish_cmds(self):
        actuator_commands = self.actuator_commands_buffer.get()
        if actuator_commands is None:
            return

        msg = ActuatorCmds()
        msg.header.frame_id = self.robot_name
        msg.header.stamp = self.node_handle.get_clock().now().to_msg()

        model = self.pinocchioInterface_ptr.model_
        for joint_name in self.actuated_joints_name:
            if model.existJointName(joint_name):
                joint_id = model.getJointId(joint_name) - 2  # 根据C++代码的偏移
                msg.names.append(joint_name)
                msg.gain_p.append(actuator_commands.Kp[joint_id])
                msg.pos_des.append(actuator_commands.pos[joint_id])
                msg.gaid_d.append(actuator_commands.Kd[joint_id])
                msg.vel_des.append(actuator_commands.vel[joint_id])
                msg.feedforward_torque.append(actuator_commands.torque[joint_id])

        self.actuators_cmds_pub.publish(msg)

    def inner_loop(self):
        time.sleep(0.2)  # 初始等待
        loop_rate = 1.0 / self.freq
        print("TrajectorStabilization_loop_rate: ", loop_rate)
        timer = RepeatedTimer()

        percentage = 1.2
        qpos_start = np.zeros(len(self.actuated_joints_name))

        while rclpy.ok() and self.run_buffer.get():
            start_time = time.time()
            timer.start_timer()

            if (self.qpos_ptr_buffer.get() is None or
                self.qvel_ptr_buffer.get() is None or
                self.reference_buffer is None):
                time.sleep(loop_rate)
                continue

            elif percentage < 1.0:
                if percentage < 0.0:
                    qpos_start = self.qpos_ptr_buffer.get()[-len(self.actuated_joints_name):]
                    percentage = 0.0

                actuator_commands = ActuatorCommands()
                actuator_commands.set_zero(len(self.actuated_joints_name))

                model = self.pinocchioInterface_ptr.getModel()
                for i, joint_name in enumerate(self.actuated_joints_name):
                    if model.existJointName(joint_name):
                        joint_id = model.getJointId(joint_name) - 2
                        actuator_commands.Kp[joint_id] = 100.0
                        actuator_commands.Kd[joint_id] = 3.0
                        actuator_commands.pos[joint_id] = qpos_start[joint_id] * (1.0 - percentage) + percentage * self.joints_default_pos[i]
                        actuator_commands.vel[joint_id] = 0.0
                        actuator_commands.torque[joint_id] = 0.0

                percentage += 1.0 / (3.0 * self.freq)
                self.actuator_commands_buffer.push(actuator_commands)
                self.publish_cmds()

                if percentage > 1.0 - 1.0 / (3.0 * self.freq):
                    self.node_handle.get_logger().info("switch to WBC")

            elif self.reference_buffer.isReady():
                qpos_ptr = self.qpos_ptr_buffer.get()
                qvel_ptr = self.qvel_ptr_buffer.get()
                self.pinocchioInterface_ptr.updateRobotState(qpos_ptr, qvel_ptr)

                if qpos_ptr is not None and qvel_ptr is not None:
                    self.wbc.update_state(qpos_ptr, qvel_ptr)
                    self.wbc.update_reference_buffer(self.reference_buffer)
                    actuator_commands = self.wbc.optimize()
                    self.actuator_commands_buffer.push(actuator_commands)
                    self.publish_cmds()
            timer.end_timer()
            end_time = time.time()
            # print("end_time - start_time", end_time - start_time)
            if end_time - start_time < loop_rate:
                time.sleep(loop_rate - (end_time - start_time))


        print(
            f"[TrajectorStabilization] Max time {timer.get_max_interval_in_milliseconds()} ms, Average time {timer.get_average_in_milliseconds()} ms"
        )
