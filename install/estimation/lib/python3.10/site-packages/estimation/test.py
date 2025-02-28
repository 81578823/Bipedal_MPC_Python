import pinocchio as pin
import numpy as np

class PinocchioInterface:
    def __init__(self, model):
        """
        初始化PinocchioInterface类。

        参数:
        - model: Pinocchio的模型对象
        """
        self.model = model
        self.data = pin.Data(model)
        self.qpos_ = np.zeros(model.nq)
        self.qvel_ = np.zeros(model.nv)

    def update_robot_state(self, qpos, qvel):
        """
        更新机器人状态。

        参数:
        - qpos: 关节位置向量 (numpy数组)
        - qvel: 关节速度向量 (numpy数组)
        """
        # 使用输入的关节位置和速度更新内部状态
        self.qpos_ = np.copy(qpos)
        self.qvel_ = np.copy(qvel)

        # 规范化关节位置（例如，将四元数标准化）
        pin.normalize(self.model, self.qpos_)

        # 计算所有动力学项
        pin.computeAllTerms(self.model, self.data, self.qpos_, self.qvel_)

        # 计算质心动量时间变化
        pin.computeCentroidalMomentumTimeVariation(
            self.model,
            self.data,
            self.qpos_,
            self.qvel_,
            np.zeros(self.model.nv)
        )

        # CCRBA（控制关联惯性矩阵）的计算
        pin.ccrba(self.model, self.data, self.qpos_, self.qvel_)

        # 计算惯性矩阵的逆
        pin.computeMinverse(self.model, self.data, self.qpos_)

        # 更新所有帧的位置
        pin.updateFramePlacements(self.model, self.data)

        # 计算质心位置和相关动力学量
        pin.centerOfMass(
            self.model,
            self.data,
            self.qpos_,
            self.qvel_,
            np.zeros(self.model.nv)
        )

        # 确保惯性矩阵是对称的（将下三角部分设置为转置的上三角部分）
        self.data.M = self.data.M + self.data.M.T - np.diag(self.data.M.diagonal())
        self.data.Minv = self.data.Minv + self.data.Minv.T - np.diag(self.data.Minv.diagonal())

# 示例用法
if __name__ == "__main__":
    # 加载机器人模型（例如从URDF文件）

    model = pin.buildModelFromUrdf("/home/wbb/ros2_ws/src/assets/p1/PF_A.urdf")
    print("模型加载成功。")

    # 初始化接口
    interface = PinocchioInterface(model)
    
    # 定义关节位置和速度（示例值）
    qpos = np.random.rand(model.nq)
    qvel = np.random.rand(model.nv)
    
    # 更新机器人状态
    interface.update_robot_state(qpos, qvel)
    
    # 现在，interface.data 包含更新后的动力学信息
    print("qpos:",qpos)
    print("qvel:",qvel)
