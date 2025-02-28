# core/gait/motion_manager.py

import yaml
import threading
import time
from typing import Optional
import rclpy
from rclpy.node import Node

from core.types import scalar_t, vector3_t
from .initialization import Initialization
from .joystick import JoyStick
from estimation.state_estimation_lkf import StateEstimationLKF
from gait.gait_schedule import GaitSchedule
from generation.trajectory_generation import TrajectorGeneration
from control.trajectory_stabilization import TrajectoryStabilization
from .data_visualization import DataVisualization
from core.misc.buffer import Buffer

class MotionManager(Node):
    """
    MotionManager 类负责管理整个运动控制流程，包括状态估计、步态调度、轨迹生成与稳定、数据可视化以及初始化。
    """

    def __init__(self):
        """
        初始化 MotionManager 实例。
        """
        super().__init__('MotionManager')

        # 声明参数
        self.declare_parameter('/config_file', '')

        # 初始化缓冲区控制
        self.run_ = Buffer[bool]()
        self.run_.push(True)

        # 初始化其他指针
        self.estimator_ptr: Optional[StateEstimationLKF] = None
        self.gait_schedule_ptr: Optional[GaitSchedule] = None
        self.traj_gen_ptr: Optional[TrajectorGeneration] = None
        self.trajectory_stabilization_ptr: Optional[TrajectoryStabilization] = None
        self.vis_ptr: Optional[DataVisualization] = None
        self.initialization_ptr: Optional[Initialization] = None
        self.joy_stick_ptr: Optional[JoyStick] = None

        # 内部循环线程
        self.inner_loop_thread = threading.Thread(target=self.inner_loop, daemon=True)

        """
        初始化所有子模块，包括Initialization、JoyStick、StateEstimationLKF、GaitSchedule、TrajectorGeneration、
        TrajectoryStabilization、DataVisualization等。
        """
        # 创建Initialization实例
        self.initialization_ptr = Initialization(self)

        # 创建JoyStick实例
        self.joy_stick_ptr = JoyStick(self)

        # 等待启动按钮按下
        # self.get_logger().info("Waiting for start command...")
        # while not self.joy_stick_ptr.isStart() and rclpy.ok():
        #     rclpy.spin_once(self, timeout_sec=0.1)
        # self.get_logger().info("Start command received!")

        # 创建StateEstimationLKF实例
        self.estimator_ptr = StateEstimationLKF(self)
        self.get_logger().info("StateEstimationLKF Ready")

        # 创建GaitSchedule实例
        self.gait_schedule_ptr = GaitSchedule(self)
        self.get_logger().info("GaitSchedule Ready")

        # 创建TrajectorGeneration实例
        self.traj_gen_ptr = TrajectorGeneration(self)
        self.get_logger().info("TrajectorGeneration Ready")

        # 创建TrajectoryStabilization实例
        self.trajectory_stabilization_ptr = TrajectoryStabilization(self)
        self.get_logger().info("TrajectoryStabilization Ready")

        # 创建DataVisualization实例
        self.vis_ptr = DataVisualization(self)
        self.get_logger().info("DataVisualization Ready")

        # 加载配置文件
        try:
            config_file = self.get_parameter('/config_file').value
            with open(config_file, 'r') as file:
                self.config_ = yaml.safe_load(file)
        except Exception as e:
            self.get_logger().error(f"Failed to load config file: {e}")
            raise e

        # 启动内部循环线程
        self.inner_loop_thread.start()

    def inner_loop(self):
        """
        内部循环，定期执行运动控制逻辑，包括处理紧急停止、更新步态调度、轨迹生成与稳定等。
        """
        time.sleep(0.02)  # 等待系统初始化

        # next_time = time.time()  # 获取当前时间
        # iter_count = 0
        # loop_rate = rclpy.duration.Duration(seconds=1.0 / 1000)  # 1000 Hz (1ms per cycle)
        # loop_rate = 1.0 / 1000.0  # 1000 Hz (每次循环的时间间隔为 0.001 秒)

        self.get_logger().info("Start MotionManager inner loop")

        while self.run_.get() and rclpy.ok():
            start_time = time.time()
            # next_time += loop_rate

            # 检查紧急停止
            if self.joy_stick_ptr.eStop():
                self.get_logger().warn("Emergency Stop Activated!")
                # 重置关键模块
                self.traj_gen_ptr = None
                self.trajectory_stabilization_ptr = None
                self.vis_ptr = None
                break

            # 如果当前步态是“walk”，则设置速度命令
            if self.gait_schedule_ptr.getCurrentGaitName() == "walk":
                linear_vel_cmd = self.joy_stick_ptr.getLinearVelCmd()
                yaw_vel_cmd: scalar_t = self.joy_stick_ptr.getYawVelCmd()
                self.traj_gen_ptr.set_vel_cmd(linear_vel_cmd, yaw_vel_cmd)

            # 计算视野时间（horizon_time）
            current_cycle = self.gait_schedule_ptr.currentGaitCycle()
            horizon_time = min(2.0, max(0.3, current_cycle))

            # 评估步态调度
            mode_schedule_ptr = self.gait_schedule_ptr.eval(horizon_time)

            # 更新状态估计的步态调度
            self.estimator_ptr.updateModeSchedule(mode_schedule_ptr)

            # 更新轨迹生成模块的当前状态和步态调度
            self.traj_gen_ptr.update_current_state(
                self.estimator_ptr.getQpos(),
                self.estimator_ptr.getQvel()
            )
            self.traj_gen_ptr.update_mode_schedule(mode_schedule_ptr)

            # 更新轨迹稳定模块的当前状态和参考缓冲区
            self.trajectory_stabilization_ptr.update_current_state(
                self.estimator_ptr.getQpos(),
                self.estimator_ptr.getQvel()
            )
            self.trajectory_stabilization_ptr.update_reference_buffer(
                self.traj_gen_ptr.get_reference_buffer()
            )

            # 更新数据可视化模块的当前状态和参考缓冲区
            self.vis_ptr.update_current_state(
                self.estimator_ptr.getQpos(),
                self.estimator_ptr.getQvel()
            )
            self.vis_ptr.update_reference_buffer(
                self.traj_gen_ptr.get_reference_buffer()
            )


            now = time.time()
            if now - start_time < 0.001:
                time.sleep(0.001 - (now - start_time))
        


    def __del__(self):
        """
        析构函数，用于清理资源，类似于C++中的析构函数。
        """
        self.run_.push(False)
        if self.inner_loop_thread.is_alive():
            self.inner_loop_thread.join()
        self.get_logger().info("MotionManager has been destroyed.")

    def shutdown_callback(self):
        """
        清理资源的方法，确保线程安全退出。
        """
        self.run_.push(False)
        if self.inner_loop_thread.is_alive():
            self.inner_loop_thread.join()
        self.get_logger().info("MotionManager has been shut down.")

    def destroy_node(self):
        """
        重载父类的destroy_node方法，添加资源清理逻辑。
        """
        self.shutdown_callback()
        super().destroy_node()

