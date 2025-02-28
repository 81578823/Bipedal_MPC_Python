# core/gait/trajector_generation.py

import yaml
import numpy as np
import threading
import time
from typing import Dict, Tuple, List
# import pinocchio as pin
from rclpy.node import Node
from core.types import scalar_t, vector3_t, vector_t
from .pinocchio_interface import PinocchioInterface
from core.trajectory.reference_buffer import ReferenceBuffer
from .foothold_optimization import FootholdOptimization
from .convex_mpc import ConvexMPC
from core.misc.buffer import Buffer
from core.misc.benchmark import RepeatedTimer
from core.misc.numeric_traits import limit_epsilon
from core.trajectory.cubic_spline_trajectory import CubicSplineTrajectory, CubicSplineInterpolation,SplineType,BoundaryType
from core.gait.mode_schedule import ModeSchedule
from core.gait.motion_phase_definition import mode_number_to_stance_leg
import rclpy

class TrajectorGeneration:
    """
    TrajectorGeneration 类用于生成和优化机器人的轨迹。
    """

    def __init__(self, node_handle: Node):
        """
        初始化 TrajectorGeneration 实例。

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

        # 初始化足部名称和基座名称
        self.foot_names = self.config_["model"]["foot_names"]
        self.base_name = self.config_["model"]["base_name"]
        self.node_handle.get_logger().info(f"[TrajectorGeneration] Base name: {self.base_name}")

        # 获取生成频率
        self.freq = self.config_["generation"]["frequency"]
        self.node_handle.get_logger().info(f"[TrajectorGeneration] Frequency: {self.freq}")

        # 初始化联系标志（假设有两个足部）
        self.contact_flag = [True, True]

        # 初始化 ReferenceBuffer
        self.reference_buffer = ReferenceBuffer()

        # 初始化 FootholdOptimization 和 ConvexMPC
        self.foothold_opt = FootholdOptimization(
            node_handle=self.node_handle,
            pinocchio_interface=self.pinocchio_interface,
            reference_buffer=self.reference_buffer
        )

        self.base_opt = ConvexMPC(
            nodeHandle=self.node_handle,
            pinocchioInterface_ptr=self.pinocchio_interface,
            referenceBuffer=self.reference_buffer
        )

        # 初始化缓冲区
        self.qpos_ptr_buffer = Buffer()
        self.qvel_ptr_buffer = Buffer()

        # 初始化线程控制
        self.run = Buffer[bool]()
        self.run.push(True)

        # 初始化步态起始和结束点
        self.xf_start: Dict[str, Tuple[scalar_t, vector3_t]] = {}
        self.xf_end: Dict[str, Tuple[scalar_t, vector3_t]] = {}

        # 启动内部循环线程
        self.inner_loop_thread = threading.Thread(target=self.inner_loop, daemon=True)
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

    def __del__(self):
        """
        析构函数。停止内部循环线程。
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

    def update_mode_schedule(self, mode_schedule: ModeSchedule):
        """
        更新步态模式调度。

        Args:
            mode_schedule (ModeSchedule): 步态模式调度实例。
        """
        self.reference_buffer.setModeSchedule(mode_schedule)

    def get_reference_buffer(self) -> ReferenceBuffer:
        """
        获取 ReferenceBuffer 实例。

        Returns:
            ReferenceBuffer: ReferenceBuffer 实例。
        """
        return self.reference_buffer

    def set_vel_cmd(self, vd: vector3_t, yawd: scalar_t):
        """
        设置基座速度命令。

        Args:
            vd (vector3_t): 线速度命令。
            yawd (scalar_t): 偏航角速度命令。
        """
        self.base_opt.setVelCmd(vd, yawd)

    def set_height_cmd(self, h: scalar_t):
        """
        设置基座高度命令。

        Args:
            h (scalar_t): 高度命令。
        """
        self.base_opt.setHeightCmd(h)

    def inner_loop(self):
        """
        内部循环，定期执行轨迹生成和优化。
        """
        time.sleep(0.2)  # 等待系统初始化

        timer = RepeatedTimer()
        loop_rate = 1.0 / self.freq
        print("TrajectorGeneration_loop_rate:",loop_rate)

        self.node_handle.get_logger().info("Start generation loop")

        while self.run.get() and rclpy.ok():
            start_time = time.time()
            timer.start_timer()

            if self.qpos_ptr_buffer.get() is None or self.qvel_ptr_buffer.get() is None or self.reference_buffer.getModeSchedule() is None:
                continue
            else:

                qpos_ptr = self.qpos_ptr_buffer.get()
                qvel_ptr = self.qvel_ptr_buffer.get()

                # 更新机器人状态
                self.pinocchio_interface.updateRobotState(qpos_ptr, qvel_ptr)

                # 生成基座轨迹参考
                self.base_opt.generateTrajRef() # 0.0008s

                # 优化足部位置
                self.foothold_opt.optimize()   # 0.00033s

                # 生成足部轨迹
                self.generate_foot_traj()   # 0.00016s

                # test_start = time.time()
                # 优化基座轨迹
                self.base_opt.optimize()  # 0.057s
                # test_end = time.time()
                # print("base_optimize_time",test_end-test_start)

            timer.end_timer()
            now = time.time()
            # print("now-start_time",now-start_time)
            if now - start_time < loop_rate:
                time.sleep(loop_rate-(now - start_time))
                
        # 记录计时信息
        print(
            f"[TrajectorGeneration] Max time {timer.get_max_interval_in_milliseconds()} ms, Average time {timer.get_average_in_milliseconds()} ms"
        )

    def generate_foot_traj(self):
        """
        生成足部的三次样条轨迹。
        """
        footholds = self.reference_buffer.getFootholds()
        t_now = self.node_handle.get_clock().now().nanoseconds*1e-9
        mode_schedule = self.reference_buffer.getModeSchedule()

        if not self.xf_start:
            for foot in self.foot_names:
                pos = self.pinocchio_interface.getFramePose(foot).translation.copy()
                self.xf_start[foot] = (t_now, pos)

        if not self.xf_end:
            for foot in self.foot_names:
                pos = self.pinocchio_interface.getFramePose(foot).translation.copy()
                self.xf_end[foot] = (t_now + mode_schedule.duration(), pos)

        foot_pos_traj: Dict[str, CubicSplineTrajectory] = {}
        contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(0.0))

        for idx, foot in enumerate(self.foot_names):
            pos = self.pinocchio_interface.getFramePose(foot).translation.copy()

            # 更新开始点
            if self.contact_flag[idx] != contact_flag[idx]:
                self.xf_start[foot] = (t_now - limit_epsilon(), pos.copy())

            # 更新结束点
            if contact_flag[idx]:
                if self.contact_flag[idx] != contact_flag[idx]:
                    self.xf_end[foot] = (t_now + mode_schedule.time_left_in_mode(0.0), pos.copy())
            else:
                self.xf_end[foot] = footholds.get(foot, (t_now, pos.copy()))[0], footholds.get(foot, (t_now, pos.copy()))[1].copy()

            # 确保起始时间合理
            if self.xf_start[foot][0] < self.xf_end[foot][0] - mode_schedule.duration():
                self.xf_start[foot] = (self.xf_end[foot][0] - mode_schedule.duration(), pos.copy())

            # 限制足部高度
            base_pos = self.pinocchio_interface.getFramePose(self.base_name).translation.copy()
            self.xf_start[foot][1][2] = min(self.xf_start[foot][1][2], base_pos[2] - 0.2)
            self.xf_end[foot][1][2] = min(self.xf_end[foot][1][2], base_pos[2] - 0.2)

            # 构建三次样条轨迹
            times = [
                self.xf_start[foot][0],
                0.5 * (self.xf_start[foot][0] + self.xf_end[foot][0]),
                self.xf_end[foot][0]
            ]
            positions = [
                self.xf_start[foot][1],
                0.5 * (self.xf_start[foot][1] + self.xf_end[foot][1]) + (0.0 if contact_flag[idx] else np.array([0.0, 0.0, 0.1])),
                self.xf_end[foot][1]
            ]

            cubicspline = CubicSplineTrajectory(
                n_dim=3,
                spline_type=SplineType.CSPLINE
            )
            cubicspline.set_boundary(
                left=BoundaryType.FIRST_DERIV,
                left_value=np.zeros(3),
                right=BoundaryType.FIRST_DERIV,
                right_value=np.zeros(3)
            )
            cubicspline.fit(times, positions)

            foot_pos_traj[foot] = cubicspline

        # 更新联系标志
        self.contact_flag = contact_flag

        # 设置足部轨迹
        self.reference_buffer.setFootPosTraj(foot_pos_traj)
