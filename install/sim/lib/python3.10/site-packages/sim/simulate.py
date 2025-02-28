# core/sim/simulate.py

import mujoco
import threading
import mujoco.viewer
import numpy as np
from collections import deque
from threading import Lock
import time
import rclpy

class Simulate:
    """
    Simulate 类用于管理MuJoCo仿真，包括加载模型、初始化数据等。
    """
    def __init__(self, run=False, busywait=False, ctrl_noise_std=0.0, ctrl_noise_rate=0.0, percent_real_time=None, refresh_rate=0.1):
        self.run = run
        self.busywait = busywait
        self.ctrl_noise_std = ctrl_noise_std
        self.ctrl_noise_rate = ctrl_noise_rate
        self.percent_real_time = percent_real_time if percent_real_time else [100]  # for simplicity
        self.refresh_rate = refresh_rate
        self.mtx = Lock()
        self.droploadrequest = threading.Event()
        self.uiloadrequest = threading.Event()
        self.exitrequest = threading.Event()
        self.m = None
        self.d = None
        self.ctrlnoise = None
        self.syncMisalign = 0.1
        self.syncSim = 0
        self.syncCPU = None
        self.speed_changed = False
        self.measured_slowdown = None
        self.real_time_index = 0
        self.viewer = None  # 添加 Viewer 实例
        self.sim_publisher = None  # 将在 main_sim.py 中设置
        self.actuator_cmds_buffer = None  # 将在 main_sim.py 中设置
        self.iter_=0


    def load_model(self, model_path: str):
        """
        加载MuJoCo模型。

        Args:
            model_path (str): 模型文件的路径。
        """
        try:
            self.m_ = mujoco.MjModel.from_xml_path(model_path)
            self.d_ = mujoco.MjData(self.m_)
            self.load_error = ""
            print(f"Model loaded successfully from {model_path}")


        except Exception as e:
            self.load_error = str(e)
            self.m_ = None
            self.d_ = None
        """
        初始化 MuJoCo Viewer，以便可视化仿真场景。
        """
        # >>>> 仅在正确加载 model 和 data 后才初始化
        if self.m_ is not None and self.d_ is not None:
            try:
                if self.viewer is None:
                     # 使用实时渲染并启动可交互的Viewer窗口
                    self.viewer = mujoco.viewer.launch_passive(self.m_, self.d_)

                print("Viewer initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize viewer: {e}")
                self.viewer = None
        else:
            print("Viewer initialization skipped due to missing model or data.")


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
        执行单步仿真，并应用控制命令。
        """
        # self.m_.opt.timestep = 0.001
        # 执行仿真步进
        with self.mtx:
            if self.run and (self.m_ is not None) and (self.d_ is not None):
                step_start = time.time()
                # 应用控制命令
                mujoco.mj_step(self.m_, self.d_)
                # mujoco.mj_forward(self.m_, self.d_)

                # 同步 Viewer
                if self.viewer and self.viewer.is_running():
                    try:
                        if self.iter_ % 10 == 0: 
                            self.viewer.sync()
                        self.iter_ += 1
                        time_until_next_step = self.m_.opt.timestep - (time.time() - step_start)
                        if time_until_next_step > 0:
                            time.sleep(time_until_next_step)
                        # 确保每一步都更新显示
                    except Exception as e:
                        print(f"Viewer sync failed: {e}")
                else:
                    self.exitrequest.set()
                    self.run = False
                    rclpy.shutdown()
