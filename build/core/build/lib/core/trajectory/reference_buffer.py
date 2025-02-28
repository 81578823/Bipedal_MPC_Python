# reference_buffer.py

from typing import Dict, Optional, Tuple
import numpy as np
from ..misc.buffer import Buffer
from .cubic_spline_trajectory import CubicSplineTrajectory
from ..gait.mode_schedule import ModeSchedule  
from enum import Enum

# 定义类型别名
scalar_t = float
vector_t = np.ndarray
vector3_t = np.ndarray

class ReferenceBuffer:
    """
    ReferenceBuffer 类用于存储和管理多种三次样条轨迹以及其他相关数据。
    """

    def __init__(self):
        # 初始化各类 Buffer 实例
        self.integ_base_rpy_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.integ_base_pos_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()

        self.lip_base_pos_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.lip_base_vel_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.lip_foot_pos_buffer_ = Buffer[Optional[Dict[str, CubicSplineTrajectory]]]()

        self.optimized_base_pos_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.optimized_base_rpy_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.optimized_base_vel_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.optimized_base_omega_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()
        self.optimized_force_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()

        self.foot_rpy_buffer_ = Buffer[Optional[Dict[str, CubicSplineTrajectory]]]()
        self.foot_pos_buffer_ = Buffer[Optional[Dict[str, CubicSplineTrajectory]]]()
        self.joints_pos_buffer_ = Buffer[Optional[CubicSplineTrajectory]]()

        self.footholds_buffer_ = Buffer[Optional[Dict[str, Tuple[scalar_t, vector3_t]]]]()
        self.mode_schedule_buffer_ = Buffer[Optional[ModeSchedule]]()

    def clearAll(self) -> None:
        """
        清除所有缓冲区中的数据。
        """
        self.integ_base_rpy_buffer_.clear()
        self.integ_base_pos_buffer_.clear()

        self.lip_base_pos_buffer_.clear()
        self.lip_base_vel_buffer_.clear()
        self.lip_foot_pos_buffer_.clear()

        self.optimized_base_pos_buffer_.clear()
        self.optimized_base_rpy_buffer_.clear()
        self.optimized_base_vel_buffer_.clear()
        self.optimized_base_omega_buffer_.clear()
        self.optimized_force_buffer_.clear()

        self.foot_rpy_buffer_.clear()
        self.foot_pos_buffer_.clear()
        self.joints_pos_buffer_.clear()

        self.footholds_buffer_.clear()
        self.mode_schedule_buffer_.clear()

    def isReady(self) -> bool:
        """
        检查所有缓冲区是否已准备好（即所有必需的缓冲区都已填充）。
        
        Returns:
            bool: 如果所有必需的缓冲区都已填充，则返回 True，否则返回 False。
        """
        is_ready = True
        is_ready &= self.integ_base_rpy_buffer_.get() is not None
        # is_ready &= self.lip_base_pos_buffer_.get() is not None
        # is_ready &= self.lip_base_vel_buffer_.get() is not None
        is_ready &= self.optimized_base_pos_buffer_.get() is not None
        is_ready &= self.optimized_base_rpy_buffer_.get() is not None
        is_ready &= self.optimized_base_vel_buffer_.get() is not None
        is_ready &= self.optimized_base_omega_buffer_.get() is not None
        is_ready &= self.mode_schedule_buffer_.get() is not None

        # 检查 foot_pos_buffer_, lip_foot_pos_buffer_, footholds_buffer_ 是否不为空
        foot_pos = self.foot_pos_buffer_.get()
        # lip_foot_pos = self.lip_foot_pos_buffer_.get()
        footholds = self.footholds_buffer_.get()

        is_ready &= foot_pos is not None and len(foot_pos) > 0
        # is_ready &= lip_foot_pos is not None and len(lip_foot_pos) > 0
        is_ready &= footholds is not None and len(footholds) > 0

        return is_ready

    # 获取方法

    def getIntegratedBaseRpyTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.integ_base_rpy_buffer_.get()

    def getIntegratedBasePosTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.integ_base_pos_buffer_.get()

    def getLipBasePosTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.lip_base_pos_buffer_.get()

    def getLipBaseVelTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.lip_base_vel_buffer_.get()

    def getOptimizedBasePosTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.optimized_base_pos_buffer_.get()

    def getOptimizedBaseRpyTraj(self) -> Optional[CubicSplineTrajectory]:
        optimized_base_rpy = self.optimized_base_rpy_buffer_.get()
        return optimized_base_rpy if optimized_base_rpy is not None else self.getIntegratedBaseRpyTraj()

    def getOptimizedBaseVelTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.optimized_base_vel_buffer_.get()

    def getOptimizedBaseOmegaTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.optimized_base_omega_buffer_.get()

    def getOptimizedForceTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.optimized_force_buffer_.get()

    def getFootRpyTraj(self) -> Optional[Dict[str, CubicSplineTrajectory]]:
        return self.foot_rpy_buffer_.get()

    def getFootPosTraj(self) -> Optional[Dict[str, CubicSplineTrajectory]]:
        return self.foot_pos_buffer_.get()

    def getLipFootPosTraj(self) -> Optional[Dict[str, CubicSplineTrajectory]]:
        return self.lip_foot_pos_buffer_.get()

    def getJointsPosTraj(self) -> Optional[CubicSplineTrajectory]:
        return self.joints_pos_buffer_.get()

    def getFootholds(self) -> Optional[Dict[str, Tuple[scalar_t, vector3_t]]]:
        return self.footholds_buffer_.get()

    def getModeSchedule(self) -> Optional[ModeSchedule]:
        return self.mode_schedule_buffer_.get()

    # 设置方法

    def setIntegratedBaseRpyTraj(self, base_rpy_traj: CubicSplineTrajectory) -> None:
        self.integ_base_rpy_buffer_.push(base_rpy_traj)

    def setIntegratedBasePosTraj(self, base_pos_traj: CubicSplineTrajectory) -> None:
        self.integ_base_pos_buffer_.push(base_pos_traj)

    def setLipBasePosTraj(self, base_pos_traj: CubicSplineTrajectory) -> None:
        self.lip_base_pos_buffer_.push(base_pos_traj)

    def setLipBaseVelTraj(self, base_vel_traj: CubicSplineTrajectory) -> None:
        self.lip_base_vel_buffer_.push(base_vel_traj)

    def setOptimizedBasePosTraj(self, base_pos_traj: CubicSplineTrajectory) -> None:
        self.optimized_base_pos_buffer_.push(base_pos_traj)

    def setOptimizedBaseRpyTraj(self, base_rpy_traj: CubicSplineTrajectory) -> None:
        self.optimized_base_rpy_buffer_.push(base_rpy_traj)

    def setOptimizedBaseVelTraj(self, base_vel_traj: CubicSplineTrajectory) -> None:
        self.optimized_base_vel_buffer_.push(base_vel_traj)

    def setOptimizedBaseOmegaTraj(self, base_omega_traj: CubicSplineTrajectory) -> None:
        self.optimized_base_omega_buffer_.push(base_omega_traj)

    def setOptimizedForceTraj(self, force_traj: CubicSplineTrajectory) -> None:
        self.optimized_force_buffer_.push(force_traj)

    def setFootRpyTraj(self, foot_rpy_traj: Dict[str, CubicSplineTrajectory]) -> None:
        self.foot_rpy_buffer_.push(foot_rpy_traj)

    def setFootPosTraj(self, foot_pos_traj: Dict[str, CubicSplineTrajectory]) -> None:
        self.foot_pos_buffer_.push(foot_pos_traj)

    def setLipFootPosTraj(self, foot_pos_traj: Dict[str, CubicSplineTrajectory]) -> None:
        self.lip_foot_pos_buffer_.push(foot_pos_traj)

    def setJointsPosTraj(self, joints_pos_traj: CubicSplineTrajectory) -> None:
        self.joints_pos_buffer_.push(joints_pos_traj)

    def setFootholds(self, footholds: Dict[str, Tuple[scalar_t, vector3_t]]) -> None:
        self.footholds_buffer_.push(footholds)

    def setModeSchedule(self, mode_schedule: ModeSchedule) -> None:
        self.mode_schedule_buffer_.push(mode_schedule)
