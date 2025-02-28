# core/pinocchio_interface.py

import pinocchio as pin
import numpy as np
from typing import List, Dict
import threading

# 假设在 core.types 模块中定义了如下类型别名
from core.types import scalar_t, vector_t, matrix_t, vector3_t, matrix3x_t, matrix6x_t, vector6_t

class PinocchioInterface:
    """
    PinocchioInterface 类用于封装Pinocchio库的功能，提供方便的接口来获取机器人模型的状态和动力学信息。
    """

    def __init__(self, urdf_name: str):
        """
        初始化PinocchioInterface实例。

        Args:
            urdf_name (str): 机器人URDF文件的路径。
        """
        # 加载URDF模型
        self.model_=pin.buildModelFromUrdf(urdf_name, pin.JointModelFreeFlyer())

        # 初始化数据结构
        self.data_ = self.model_.createData()

        # 初始化关节位置和速度
        self.qpos_ = np.zeros(self.model_.nq)
        self.qvel_ = np.zeros(self.model_.nv)

        # 初始化接触点信息
        self.contact_mask_: List[bool] = []
        self.contact_points_: List[str] = []

        # 线程锁，确保线程安全
        self.lock = threading.Lock()

    def setContactPoints(self, contact_points: List[str]):
        """
        设置接触点的名称。

        Args:
            contact_points (List[str]): 接触点名称列表。
        """
        with self.lock:
            self.contact_points_ = contact_points
            self.contact_mask_ = [False] * len(contact_points)

    def getModel(self) -> pin.Model:
        """
        获取Pinocchio模型。

        Returns:
            pin.Model: Pinocchio模型。
        """
        return self.model_

    def getData(self) -> pin.Data:
        """
        获取Pinocchio数据结构。

        Returns:
            pin.Data: Pinocchio数据结构。
        """
        return self.data_

    def updateRobotState(self, qpos: np.ndarray, qvel: np.ndarray):
        """
        更新机器人的关节状态（位置和速度）。

        Args:
            qpos (np.ndarray): 关节位置向量。
            qvel (np.ndarray): 关节速度向量。
        """
        with self.lock:
            self.qpos_ = np.array(qpos, copy=True)
            self.qvel_ = np.array(qvel, copy=True)

            # 规范化关节位置
            pin.normalize(self.model_, self.qpos_)

            # 计算所有动力学项
            pin.computeAllTerms(self.model_, self.data_, self.qpos_, self.qvel_)

            # 计算质心动量时间变化率
            pin.computeCentroidalMomentumTimeVariation(
                self.model_, self.data_, self.qpos_, self.qvel_, np.zeros(self.model_.nv)
            )

            # 计算惯性矩阵和其他动力学量
            pin.ccrba(self.model_, self.data_, self.qpos_, self.qvel_)

            # 计算惯性矩阵的逆
            pin.computeMinverse(self.model_, self.data_, self.qpos_)

            # 更新框架的位置
            pin.updateFramePlacements(self.model_, self.data_)

            # 计算质心的位置、速度和加速度
            pin.centerOfMass(
                self.model_, self.data_, self.qpos_, self.qvel_, np.zeros(self.model_.nv)
            )

            # 对称化惯性矩阵和其逆
            self.data_.M = np.triu(self.data_.M) + np.triu(self.data_.M, 1).T
            self.data_.Minv = np.triu(self.data_.Minv) + np.triu(self.data_.Minv, 1).T

    def total_mass(self) -> scalar_t:
        """
        计算机器人的总质量。

        Returns:
            scalar_t: 总质量。
        """
        return pin.computeTotalMass(self.model_)

    def getCoMPos(self) -> vector3_t:
        """
        获取质心位置。

        Returns:
            vector3_t: 质心位置向量。
        """
        return self.data_.com[0]

    def getCoMVel(self) -> vector3_t:
        """
        获取质心速度。

        Returns:
            vector3_t: 质心速度向量。
        """
        return self.data_.vcom[0]

    def getCoMAcc(self) -> vector3_t:
        """
        获取质心加速度。

        Returns:
            vector3_t: 质心加速度向量。
        """
        return self.data_.acom[0]

    def getJacobia_CoM(self) -> matrix3x_t:
        """
        获取质心雅可比矩阵。

        Returns:
            matrix3x_t: 质心雅可比矩阵。
        """
        return self.data_.Jcom

    def getJacobia_local(self, frame_name: str) -> matrix6x_t:
        """
        获取指定框架在本地坐标系下的雅可比矩阵。

        Args:
            frame_name (str): 框架名称。

        Returns:
            matrix6x_t: 雅可比矩阵。
        """
        # J = np.zeros((6, self.model_.nv))
        J = pin.getFrameJacobian(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL)
        return J

    def getJacobia_world(self, frame_name: str) -> matrix6x_t:
        """
        获取指定框架在世界坐标系下的雅可比矩阵。

        Args:
            frame_name (str): 框架名称。

        Returns:
            matrix6x_t: 雅可比矩阵。
        """
        # J = np.zeros((6, self.model_.nv))
        J = pin.getFrameJacobian(self.model_, self.data_, self.getFrameID(frame_name), pin.WORLD)
        return J

    def getJacobia_localWorldAligned(self, frame_name: str) -> matrix6x_t:
        """
        获取指定框架在本地世界对齐坐标系下的雅可比矩阵。

        Args:
            frame_name (str): 框架名称。

        Returns:
            matrix6x_t: 雅可比矩阵。
        """
        # J = np.zeros((6, self.model_.nv))
        J = pin.getFrameJacobian(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL_WORLD_ALIGNED)
        return J

    def getContactPointJacobia_localWorldAligned(self, idx: int) -> matrix6x_t:
        """
        获取指定接触点在本地世界对齐坐标系下的雅可比矩阵。

        Args:
            idx (int): 接触点索引。

        Returns:
            matrix6x_t: 雅可比矩阵。
        """
        if idx >= self.nc():
            raise IndexError("[PinocchioInterface::getContactPointJacobia_localWorldAligned]: idx >= nc()")
        frame_name = self.contact_points_[idx]
        return self.getJacobia_localWorldAligned(frame_name)

    def getFrameID(self, frame_name: str) -> int:
        """
        获取指定框架的索引ID。

        Args:
            frame_name (str): 框架名称。

        Returns:
            int: 框架ID。
        """
        if not self.model_.existFrame(frame_name):
            raise ValueError(f"[PinocchioInterface::getFrameID]: {frame_name} does not exist")
        return self.model_.getFrameId(frame_name)

    def getFramePose(self, frame_name: str) -> pin.SE3:
        """
        获取指定框架在世界坐标系下的位姿。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.SE3: 位姿。
        """
        return self.data_.oMf[self.getFrameID(frame_name)]

    def getFrame6dVel_local(self, frame_name: str) -> pin.Motion:
        """
        获取指定框架在本地坐标系下的6D速度。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.Motion: 6D速度。
        """
        return pin.getFrameVelocity(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL)

    def getFrame6dVel_localWorldAligned(self, frame_name: str) -> pin.Motion:
        """
        获取指定框架在本地世界对齐坐标系下的6D速度。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.Motion: 6D速度。
        """
        return pin.getFrameVelocity(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL_WORLD_ALIGNED)

    def getFrame6dAcc_local(self, frame_name: str) -> pin.Motion:
        """
        获取指定框架在本地坐标系下的6D加速度。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.Motion: 6D加速度。
        """
        return pin.getFrameAcceleration(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL)

    def getFrame6dAcc_world(self, frame_name: str) -> pin.Motion:
        """
        获取指定框架在世界坐标系下的6D加速度。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.Motion: 6D加速度。
        """
        return pin.getFrameAcceleration(self.model_, self.data_, self.getFrameID(frame_name), pin.WORLD)

    def getFrame6dAcc_localWorldAligned(self, frame_name: str) -> pin.Motion:
        """
        获取指定框架在本地世界对齐坐标系下的6D加速度。

        Args:
            frame_name (str): 框架名称。

        Returns:
            pin.Motion: 6D加速度。
        """
        return pin.getFrameAcceleration(self.model_, self.data_, self.getFrameID(frame_name), pin.LOCAL_WORLD_ALIGNED)

    def nq(self) -> int:
        """
        获取关节位置向量的维度。

        Returns:
            int: 关节位置向量的维度。
        """
        return self.model_.nq

    def nv(self) -> int:
        """
        获取关节速度向量的维度。

        Returns:
            int: 关节速度向量的维度。
        """
        return self.model_.nv

    def na(self) -> int:
        """
        获取无约束关节的数量。

        Returns:
            int: 无约束关节的数量。
        """
        return self.model_.nv - 6  # 假设前6个自由度是自由基（FreeFlyer）

    def nc(self) -> int:
        """
        获取接触点的数量。

        Returns:
            int: 接触点的数量。
        """
        return len(self.contact_points_)

    def qpos(self) -> np.ndarray:
        """
        获取关节位置向量的引用。

        Returns:
            np.ndarray: 关节位置向量。
        """
        return self.qpos_

    def qvel(self) -> np.ndarray:
        """
        获取关节速度向量的引用。

        Returns:
            np.ndarray: 关节速度向量。
        """
        return self.qvel_

    def getMomentumJacobia(self) -> matrix6x_t:
        """
        获取动量雅可比矩阵。

        Returns:
            matrix6x_t: 动量雅可比矩阵。
        """
        return self.data_.Ag

    def getMomentumTimeVariation(self) -> vector6_t:
        """
        获取动量时间变化率。

        Returns:
            vector6_t: 动量时间变化率向量。
        """
        return pin.computeCentroidalMomentumTimeVariation(self.model_, self.data_).toVector()

    def setContactMask(self, mask: List[bool]):
        """
        设置接触点的掩码（是否接触）。

        Args:
            mask (List[bool]): 接触点掩码列表。

        Raises:
            ValueError: 如果掩码长度与接触点数量不一致。
        """
        if len(mask) != self.nc():
            raise ValueError("[PinocchioInterface::setContactMask]: mask size does not match number of contact points")
        with self.lock:
            self.contact_mask_ = mask.copy()

    def getContactMask(self) -> List[bool]:
        """
        获取接触点的掩码。

        Returns:
            List[bool]: 接触点掩码列表。

        Raises:
            ValueError: 如果掩码长度与接触点数量不一致。
        """
        if len(self.contact_mask_) != self.nc():
            raise ValueError("[PinocchioInterface::getContactMask]: contact_mask_ size does not match number of contact points")
        return self.contact_mask_

    def getContactPoints(self) -> List[str]:
        """
        获取接触点的名称列表。

        Returns:
            List[str]: 接触点名称列表。
        """
        return self.contact_points_
