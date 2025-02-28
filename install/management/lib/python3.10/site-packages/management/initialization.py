# core/gait/initialization.py

import yaml
from typing import List

import rclpy
from rclpy.node import Node
from rclpy.qos import  QoSHistoryPolicy, QoSReliabilityPolicy

from core.types import scalar_t
from generation.pinocchio_interface import PinocchioInterface

# 假设trans/srv/SimulationReset.srv已正确定义并编译
from trans.srv import SimulationReset

class Initialization:
    """
    Initialization 类用于初始化和重置机器人仿真状态。
    """

    def __init__(self, node_handle: Node):
        """
        初始化 Initialization 实例。

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

        # 加载配置文件
        try:
            with open(self.config_file, 'r') as file:
                self.config_ = yaml.safe_load(file)
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to load config file: {e}")
            raise e

        # 获取模型包和URDF路径
        try:
            model_package = self.config_["model"]["package"]
            urdf_relative_path = self.config_["model"]["urdf"]
            # print(f"Model package: {model_package}")
            # print(f"URDF relative path: {urdf_relative_path}")
            from ament_index_python.packages import get_package_share_directory
            urdf_path = get_package_share_directory(model_package) + urdf_relative_path
            self.node_handle.get_logger().info(f"Model file: {urdf_path}")
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to load URDF path: {e}")
            raise e

        # 初始化 PinocchioInterface
        self.pinocchio_interface = PinocchioInterface(urdf_path)

        # 初始化其他配置
        self.joints_name: List[str] = self.config_["model"]["actuated_joints_name"]
        self.robot_name: str = self.config_["model"]["name"]

        # 创建服务客户端
        topic_prefix = self.config_["global"]["topic_prefix"]
        self.reset_state_client = self.node_handle.create_client(SimulationReset, f"{topic_prefix}sim_reset")

    def load_config(self, config_file: str):
        """
        设置配置文件路径。

        Args:
            config_file (str): 配置文件路径。
        """
        self.config_file = config_file

    def reset_simulation(self):
        """
        重置仿真状态，通过调用SimulationReset服务。
        """
        # 从配置中获取默认状态
        try:
            joints_name = self.config_["model"]["actuated_joints_name"]
            joint_pos = self.config_["model"]["default"]["joint_pos"]
            base_pos = self.config_["model"]["default"]["base_pos"]
            base_quat = self.config_["model"]["default"]["base_quat"]
            frame_id = self.config_["model"]["name"]
        except KeyError as e:
            self.node_handle.get_logger().error(f"Missing key in config file: {e}")
            return

        # 创建请求
        request = SimulationReset.Request()
        request.header.frame_id = frame_id
        request.base_pose.position.x = base_pos[0]
        request.base_pose.position.y = base_pos[1]
        request.base_pose.position.z = base_pos[2]
        request.base_pose.orientation.w = base_quat[0]
        request.base_pose.orientation.x = base_quat[1]
        request.base_pose.orientation.y = base_quat[2]
        request.base_pose.orientation.z = base_quat[3]

        request.joint_state.name = joints_name
        request.joint_state.position = joint_pos

        self.node_handle.get_logger().info(f"Waiting for service {self.reset_state_client.srv_name} ...")

        # 等待服务可用
        while not self.reset_state_client.wait_for_service(timeout_sec=0.02):
            if not rclpy.ok():
                self.node_handle.get_logger().error("Interrupted while waiting for the service. Exiting.")
                return
            self.node_handle.get_logger().info("Service not available, waiting...")

        # 发送请求
        future = self.reset_state_client.call_async(request)

        # 等待结果
        rclpy.spin_until_future_complete(self.node_handle, future)

        if future.done():
            try:
                response = future.result()
                if response.is_success:
                    self.node_handle.get_logger().info("Simulation reset successfully.")
                else:
                    self.node_handle.get_logger().error("Failed to reset simulation.")
            except Exception as e:
                self.node_handle.get_logger().error(f"Service call failed: {e}")
        else:
            self.node_handle.get_logger().error("Service call did not complete.")

