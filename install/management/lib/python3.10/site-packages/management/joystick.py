# core/gait/joystick.py

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from core.types import scalar_t, vector3_t
from core.misc.buffer import Buffer
from threading import Lock

class JoyStick:
    """
    JoyStick 类用于处理来自摇杆的输入，生成线速度、偏航速度、高度命令，并检测紧急停止和启动按钮。
    """

    def __init__(self, node_handle: Node):
        """
        初始化 JoyStick 实例。

        Args:
            node_handle (Node): ROS 2 节点句柄。
        """
        self.node_handle = node_handle

        # 初始化缓冲区
        self.e_stop_ = Buffer[bool]()
        self.start_ = Buffer[bool]()
        self.joy_msg_ = Buffer[Joy]()

        # 初始化命令变量
        self.h_des_ = 0.0
        self.vel_cmd = np.zeros(3)

        # 初始化锁以确保线程安全
        self.lock = Lock()

        # 订阅 'joy' 主题
        self.joy_sub = self.node_handle.create_subscription(
            Joy,
            'joy',
            self.joy_cb,
            qos_profile=rclpy.qos.qos_profile_sensor_data
        )

        # 初始化缓冲区状态
        self.e_stop_.push(False)
        self.start_.push(False)

        # 日志信息
        self.node_handle.get_logger().info("JoyStick Initialized!")

    def joy_cb(self, joy_msg: Joy):
        """
        摇杆消息的回调函数，存储最新的Joy消息到缓冲区。

        Args:
            joy_msg (Joy): 接收到的Joy消息。
        """
        self.joy_msg_.push(joy_msg)

    def getLinearVelCmd(self) :
        """
        获取线速度命令，基于摇杆输入并进行平滑处理。

        Returns:
            vector3_t: 线速度命令向量。
        """
        msg = self.joy_msg_.get()
        if msg is None:
            # print("msg is None")
            return np.array([0, 0, 0])
        else:
        # with self.lock:
            # 根据摇杆轴的不同，生成不同的速度命令
            if msg.axes[5] < 0.9:
                vel_cmd_t = np.array([0.4, 0.0, 0.0])
                self.vel_cmd = 0.999 * self.vel_cmd + 0.001 * vel_cmd_t
            elif msg.axes[2] < 0.9:
                vel_cmd_t = np.array([-0.4, 0.0, 0.0])
                self.vel_cmd = 0.999 * self.vel_cmd + 0.001 * vel_cmd_t
            else:
                vel_cmd_t = np.array([
                    0.3 * msg.axes[1],
                    0.1 * msg.axes[0],
                    0.0
                ])
                self.vel_cmd = 0.995 * self.vel_cmd + 0.005 * vel_cmd_t
            print("self.vel_cmd",self.vel_cmd)
        return np.array(self.vel_cmd)

    def getYawVelCmd(self) -> scalar_t:
        """
        获取偏航速度命令，基于摇杆输入。

        Returns:
            scalar_t: 偏航速度命令。
        """
        angular_velocity_factor = 0.3
        msg = self.joy_msg_.get()
        if msg is None:
            return 0.0
        else:
        # with self.lock:
            return angular_velocity_factor * msg.axes[3]

    def eStop(self) -> bool:
        """
        检测紧急停止按钮是否被按下。

        Returns:
            bool: 如果按下紧急停止按钮，则返回True，否则返回False。
        """
        msg = self.joy_msg_.get()
        if msg is None:
            return False
        else:
            # with self.lock:
            return msg.buttons[7] > 0

    def isStart(self) -> bool:
        """
        检测启动按钮是否被按下。

        Returns:
            bool: 如果按下启动按钮，则返回True，否则返回False。
        """
        msg = self.joy_msg_.get()
        if msg is not None:
            if not self.start_.get() and msg.buttons[5] > 0:
                self.start_.push(True)
        return self.start_.get()
