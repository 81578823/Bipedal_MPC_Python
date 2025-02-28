# core/sim/simulate.py

import mujoco
import threading

class Simulate:
    """
    Simulate 类用于管理MuJoCo仿真，包括加载模型、初始化数据等。
    """
    def __init__(self):
        self.m_ = None  # mujoco.MjModel 实例
        self.d_ = None  # mujoco.MjData 实例
        self.mtx = threading.RLock()
        self.uiloadrequest = 0
        self.filename = b''  # 模型文件路径，bytes类型
        self.load_error = ""
        self.run = True
        self.exitrequest = threading.Event()
        self.droploadrequest = threading.Event()
        self.dropfilename = ""
        self.speed_changed = False
        self.ctrl_noise_std = 0.0
        self.ctrl_noise_rate = 0.0
        self.percentRealTime = [100.0]  # 默认实时百分比
        self.real_time_index = 0
        self.measured_slowdown = 1.0

    def load_model(self, model_path: str):
        """
        加载MuJoCo模型。

        Args:
            model_path (str): 模型文件的路径。
        """
        with self.mtx:
            try:
                self.m_ = mujoco.MjModel.from_xml_path(model_path)
                self.d_ = mujoco.MjData(self.m_)
                self.load_error = ""
            except Exception as e:
                self.load_error = str(e)
                self.m_ = None
                self.d_ = None

    def reset_data(self, base_pose, joint_state):
        """
        重置仿真数据。

        Args:
            base_pose (geometry_msgs.msg.Pose): 基座姿态。
            joint_state (sensor_msgs.msg.JointState): 关节状态。
        """
        with self.mtx:
            if self.m_ is None or self.d_ is None:
                return False
            try:
                mujoco.mj_resetData(self.m_, self.d_)
                # 设置基座位置和姿态
                self.d_.qpos[0] = base_pose.position.x
                self.d_.qpos[1] = base_pose.position.y
                self.d_.qpos[2] = base_pose.position.z
                self.d_.qpos[3] = base_pose.orientation.w
                self.d_.qpos[4] = base_pose.orientation.x
                self.d_.qpos[5] = base_pose.orientation.y
                self.d_.qpos[6] = base_pose.orientation.z

                # 设置关节位置
                for i in range(len(joint_state.position)):
                    joint_name = joint_state.name[i]
                    joint_id = mujoco.mj_name2id(self.m_, mujoco.mjtObj.mjOBJ_JOINT, joint_name.encode('utf-8'))
                    if joint_id > -1:
                        qposadr = self.m_.jnt_qposadr[joint_id]
                        self.d_.qpos[qposadr] = joint_state.position[i]
                    else:
                        # 可以记录日志或处理未知关节
                        pass

                # 重置执行器命令（假设由SimPublisher处理）
                return True
            except Exception as e:
                self.load_error = str(e)
                return False

    def step(self):
        """
        执行单步仿真。
        """
        with self.mtx:
            if self.m_ is not None and self.d_ is not None:
                mujoco.mj_step(self.m_, self.d_)
