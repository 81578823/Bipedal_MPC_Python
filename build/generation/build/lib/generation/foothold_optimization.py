# core/gait/foothold_optimization.py

import yaml
import numpy as np
from typing import Dict, Tuple, List
import pinocchio as pin
from rclpy.node import Node
from core.types import scalar_t, vector3_t, vector_t
from .pinocchio_interface import PinocchioInterface
from core.trajectory.reference_buffer import ReferenceBuffer
from core.gait.motion_phase_definition import mode_number_to_stance_leg
from core.gait.leg_logic import get_time_of_next_touch_down

class FootholdOptimization:
    """
    FootholdOptimization 类用于优化机器人的支撑足位置。
    """
    
    def __init__(self, node_handle: Node, 
                 pinocchio_interface: PinocchioInterface, 
                 reference_buffer: ReferenceBuffer):
        """
        初始化 FootholdOptimization 实例。

        Args:
            node_handle (Node): ROS 2 节点句柄。
            pinocchio_interface (PinocchioInterface): Pinocchio 接口实例。
            reference_buffer (ReferenceBuffer): 参考轨迹缓冲区实例。
        """
        self.node_handle = node_handle
        self.pinocchio_interface = pinocchio_interface
        self.reference_buffer = reference_buffer

        # 从参数服务器获取配置文件路径
        config_file = self.node_handle.get_parameter("/config_file").value
        self.load_config(config_file)

        # 初始化关节状态
        qpos = np.zeros(self.pinocchio_interface.nq())
        qvel = np.zeros(self.pinocchio_interface.nv())
        self.pinocchio_interface.updateRobotState(qpos, qvel)

        # 初始化 nominal footholds
        self.footholds_nominal_pos: Dict[str, vector3_t] = {}
        for foot in self.foot_names:
            frame_pose = self.pinocchio_interface.getFramePose(foot)
            nominal_pos = frame_pose.translation.copy()
            nominal_pos[2] = 0.0  # 设置 z 轴为 0
            nominal_pos[1] *= 0.8  # 缩放 y 轴
            self.footholds_nominal_pos[foot] = nominal_pos
            self.node_handle.get_logger().info(f"{foot}: {nominal_pos}")

        self.nf = len(self.foot_names)
        self.footholds: Dict[str, Tuple[scalar_t, vector3_t]] = {}
        self.nominal_dz = 0.0  # 根据需要初始化

    def load_config(self, config_file: str):
        """
        加载配置文件，初始化模型名称和足部名称。

        Args:
            config_file (str): 配置文件路径。
        """
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            self.foot_names = config['model']['foot_names']
            self.base_name = config['model']['base_name']
            # self.robot_name = config['model'].get('robot_name', 'robot')  # 可选字段
        except Exception as e:
            self.node_handle.get_logger().error(f"Failed to load config file: {e}")
            raise e

    def optimize(self):
        """
        执行足部位置优化。
        """
        self.footholds = {}
        base_pos_ref_traj = self.reference_buffer.getIntegratedBasePosTraj()
        base_rpy_traj = self.reference_buffer.getIntegratedBaseRpyTraj()
        mode_schedule = self.reference_buffer.getModeSchedule()

        if mode_schedule is None or base_pos_ref_traj is None or base_rpy_traj is None:
            self.reference_buffer.setFootholds(self.footholds)

        self.heuristic()
        self.reference_buffer.setFootholds(self.footholds)

    def heuristic(self):
        """
        基于启发式方法计算足部位置。
        """
        current_time = self.node_handle.get_clock().now().nanoseconds*1e-9

        base_pos_ref_traj = self.reference_buffer.getIntegratedBasePosTraj()
        base_rpy_traj = self.reference_buffer.getIntegratedBaseRpyTraj()
        mode_schedule = self.reference_buffer.getModeSchedule()

        base_pose = self.pinocchio_interface.getFramePose(self.base_name)
        base_twist = self.pinocchio_interface.getFrame6dVel_localWorldAligned(self.base_name)
        gait_cycle = mode_schedule.duration()

        phase = 0.0  # 固定为0.0，因为getModeFromPhase(0.0)在C++代码中使用
        contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase))
        # contact_flag 应该是一个布尔列表，表示每个足部是否处于支撑状态

        v_des = base_pos_ref_traj.derivative(current_time, 1)
        rpy_dot_des = base_rpy_traj.derivative(current_time, 1)

        ntc = get_time_of_next_touch_down(0, mode_schedule)

        p_rel_x_max = 0.5
        p_rel_y_max = 0.3

        for i, foot_name in enumerate(self.foot_names):
            swing_time_remain = 0.0 if contact_flag[i] else ntc[i]

            # 计算 yaw 修正后的 nominal 足部位置
            base_rpy_mid = base_rpy_traj.evaluate(current_time + gait_cycle / 2.0)
            R = self.to_rotation_matrix(base_rpy_mid)
            p_yaw_corrected = R @ self.footholds_nominal_pos[foot_name]

            # 计算相对偏移
            pfx_rel = (
                0.5 * gait_cycle * v_des[0] +
                0.4 * (base_twist.linear[0] - v_des[0]) +
                (0.5 * base_pose.translation[2] / 9.81) * (base_twist.linear[1] * rpy_dot_des[2])
            )
            pfy_rel = (
                0.5 * gait_cycle * v_des[1] +
                0.08 * (base_twist.linear[1] - v_des[1]) +
                (0.5 * base_pose.translation[2] / 9.81) * (-base_twist.linear[0] * rpy_dot_des[2])
            )

            # 限制偏移范围
            pfx_rel = np.clip(pfx_rel, -p_rel_x_max, p_rel_x_max)
            pfy_rel = np.clip(pfy_rel, -p_rel_y_max, p_rel_y_max)

            # 计算新的足部位置
            foothold_time = ntc[i] + current_time   # 用于计算足部位置的时间但是有以问题
            foothold_pos = base_pose.translation + p_yaw_corrected + max(0.0, swing_time_remain) * v_des
            foothold_pos[0] += pfx_rel
            foothold_pos[1] += pfy_rel
            foothold_pos[2] = 0.03  # 固定z轴高度

            self.footholds[foot_name] = (foothold_time, foothold_pos)

    @staticmethod
    def to_rotation_matrix(rpy: vector3_t) -> np.ndarray:
        roll, pitch, yaw = rpy
        R_roll = np.array([[1, 0, 0],
                        [0, np.cos(roll), -np.sin(roll)],
                        [0, np.sin(roll), np.cos(roll)]])
        R_pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                            [0, 1, 0],
                            [-np.sin(pitch), 0, np.cos(pitch)]])
        R_yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                        [np.sin(yaw), np.cos(yaw), 0],
                        [0, 0, 1]])

        return np.dot(R_yaw, np.dot(R_pitch, R_roll))

    def __del__(self):
        """
        析构函数。Python有垃圾回收机制，通常不需要显式实现。
        """
        pass

