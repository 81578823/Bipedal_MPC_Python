# gait_schedule.py

import threading
import time
from typing import Optional, List, Dict, Tuple
import yaml
import rclpy
from rclpy.node import Node
from core.gait.mode_schedule import ModeSchedule

from core.gait.motion_phase_definition import string_to_mode_number
from core.misc.buffer import Buffer
from trans.srv import GaitSwitch
from .cycle_timer import CycleTimer


scalar_t = float

class GaitSchedule:
    """
    GaitSchedule 类用于管理步态的加载、切换和评估。
    """

    def __init__(self, node_handle: Node):
        """
        初始化GaitSchedule实例。

        Args:
            node_handle (Node): ROS 2节点句柄。
        """
        self.nodeHandle_ = node_handle

        # 读取配置文件路径
        config_file = self.nodeHandle_.get_parameter("/config_file").value
        with open(config_file, 'r') as file:
            config_ = yaml.safe_load(file)

        # 加载步态列表
        self.gait_list: List[str] = config_["gait"]["list"]
        self.robot_name: str = config_["model"]["name"]
        self.nodeHandle_.get_logger().info(f"Robot Name: {self.robot_name}")
        self.nodeHandle_.get_logger().info(f"Gait List: {self.gait_list}")

        # 加载所有步态
        self.gait_map: Dict[str, ModeSchedule] = {}
        for gaitName in self.gait_list:
            self.gait_map[gaitName] = self.loadGait(config_, gaitName)

        # 初始化当前步态
        if len(self.gait_list) < 2:
            raise ValueError("gait_list must contain at least two gait names.")
        self.current_gait_ = Buffer[str]()
        self.current_gait_.push(self.gait_list[1])

        # 初始化步态缓冲区
        self.gait_buffer_ = Buffer[str]()
        self.gait_buffer_.push(self.gait_list[1])

        # 初始化转换时间
        self.transition_time_ = Buffer[scalar_t]()
        self.transition_time_.push(self.nodeHandle_.get_clock().now().nanoseconds*1e-9)

        # 初始化转换相关标志
        self.check_ = Buffer[bool]()
        self.check_.push(True)
        self.in_transition_ = Buffer[bool]()
        self.in_transition_.push(False)

        # 创建服务
        topic_prefix = config_["global"]["topic_prefix"]
        self.gait_service_ = self.nodeHandle_.create_service(
            GaitSwitch,
            topic_prefix + "gait_switch",
            self.gaitSwitch
        )

        # 初始化CycleTimer
        current_gait_duration = self.gait_map[self.current_gait_.get()].duration()
        self.cycle_timer_ = CycleTimer(self.nodeHandle_, current_gait_duration)

        # 启动转换检查线程
        self.check_transition_thread_ = threading.Thread(target=self.checkGaitTransition, daemon=True)
        self.check_transition_thread_.start()

    def __del__(self):
        """
        析构函数，确保线程安全地停止转换检查线程。
        """
        self.check_.push(False)
        if self.check_transition_thread_.is_alive():
            self.check_transition_thread_.join()

    def loadGait(self, node: Dict, gait_name: str) -> ModeSchedule:
        """
        加载指定步态的配置并创建ModeSchedule实例。

        Args:
            node (Dict): 配置字典。
            gait_name (str): 步态名称。

        Returns:
            ModeSchedule: 步态的ModeSchedule实例。
        """
        eventPhases = node["gait"][gait_name]["switchingTimes"]
        modeSequenceString = node["gait"][gait_name]["modeSequence"]

        if not eventPhases or not modeSequenceString:
            raise ValueError(f"Failed to load gait: {gait_name}")

        # 将事件相位标准化到[0, 1]
        end_phase = eventPhases[-1]
        duration = end_phase
        # print(f"end_phase: {end_phase}")
        if not self.almost_eq(end_phase, 1.0) and end_phase > 1e-9:
            eventPhases = [phase / end_phase for phase in eventPhases]

        # 转换模式名称到模式编号
        modeSequence = [string_to_mode_number(modeName) for modeName in modeSequenceString]

        gait = ModeSchedule(duration, eventPhases, modeSequence)
        if not gait.is_valid_mode_sequence():
            raise ValueError(f"{gait_name} gait is not valid")

        return gait

    def gaitSwitch(self, request: GaitSwitch.Request, response: GaitSwitch.Response):
        """
        步态切换服务回调。

        Args:
            request (GaitSwitch.Request): 服务请求。
            response (GaitSwitch.Response): 服务响应。
        """
        if request.header.frame_id != self.robot_name:
            self.nodeHandle_.get_logger().warn(
                f"Gait switch request id: {request.header.frame_id}, "
                f"and the robot id: {self.robot_name}, not compatible"
            )
            response.is_success = False
            return

        gait_name = request.gait_name
        if gait_name in self.gait_list:
            self.nodeHandle_.get_logger().warn(f"Gait request: change to {gait_name}")
            if gait_name == self.current_gait_.get():
                self.nodeHandle_.get_logger().warn(f"It has been in {gait_name}")
            elif self.in_transition_.get():
                self.nodeHandle_.get_logger().warn(
                    f"It is in {self.gait_buffer_.get()} transition process, "
                    f"try call gait switch service latter"
                )
                response.is_success = False
                return
            else:
                current_gait_name = self.current_gait_.get()
                phase = self.cycle_timer_.getCycleTime() / self.gait_map[current_gait_name].duration
                time_left = self.gait_map[current_gait_name].timeLeftInModeSequence(phase)
                transition_time = self.nodeHandle_.get_clock().now().nanoseconds*1e-9 + time_left
                self.transition_time_.push(transition_time)
                self.gait_buffer_.push(gait_name)
                # 启动转换检查线程
                self.check_transition_thread_ = threading.Thread(target=self.checkGaitTransition, daemon=True)
                self.check_transition_thread_.start()
                self.nodeHandle_.get_logger().warn(
                    f"Gait {gait_name} will start at time {transition_time}"
                )
                response.is_success = True
        else:
            self.nodeHandle_.get_logger().warn(f"Not found gait {gait_name} in gait list")
            response.is_success = False

    def switchGait(self, gait_name: str):
        """
        外部调用方法，切换到指定步态。

        Args:
            gait_name (str): 目标步态名称。
        """
        if gait_name not in self.gait_list:
            self.nodeHandle_.get_logger().warn(f"Gait {gait_name} not found in gait list")
            return

        if gait_name == self.current_gait_.get() or self.in_transition_.get():
            self.nodeHandle_.get_logger().warn(
                f"Cannot switch to {gait_name}. Either already in {gait_name} or in transition."
            )
            return

        current_gait_name = self.current_gait_.get()
        phase = self.cycle_timer_.getCycleTime() / self.gait_map[current_gait_name].duration

        if current_gait_name == "stance":
            transition_time = self.nodeHandle_.get_clock().now().nanoseconds*1e-9 + 0.05
        elif gait_name == "stance":
            transition_time = (
                self.nodeHandle_.get_clock().now().nanoseconds*1e-9
                + self.gait_map[current_gait_name].time_left_in_mode_sequence(phase)
                + self.gait_map[current_gait_name].duration
            )
        else:
            transition_time = self.nodeHandle_.get_clock().now().nanoseconds*1e-9 + self.gait_map[current_gait_name].time_left_in_mode_sequence(phase)

        self.transition_time_.push(transition_time)
        self.gait_buffer_.push(gait_name)
        # 启动转换检查线程
        self.check_transition_thread_ = threading.Thread(target=self.checkGaitTransition, daemon=True)
        self.check_transition_thread_.start()
        self.nodeHandle_.get_logger().warn(
            f"Gait {gait_name} will start at time {transition_time}"
        )

    def currentMode(self) -> int:
        """
        获取当前模式编号。

        Returns:
            int: 当前模式编号。
        """
        current_gait_name = self.current_gait_.get()
        phase = self.cycle_timer_.getCycleTime() / self.gait_map[current_gait_name].duration
        return self.gait_map[current_gait_name].get_mode_from_phase(phase)

    def currentGaitCycle(self) -> scalar_t:
        """
        获取当前步态周期时间。

        Returns:
            scalar_t: 当前步态周期时间（秒）。
        """
        return self.gait_map[self.current_gait_.get()].duration()

    def getCurrentGaitName(self) -> str:
        """
        获取当前步态名称。

        Returns:
            str: 当前步态名称。
        """
        return self.current_gait_.get()

    def eval(self, time_period: scalar_t) -> Optional[ModeSchedule]:
        """
        评估给定时间段内的步态模式。

        Args:
            time_period (scalar_t): 评估时间段（秒）。

        Returns:
            Optional[ModeSchedule]: 评估后的ModeSchedule实例。
        """
        current_gait_name = self.current_gait_.get()
        duration = time_period
        gait_cur = self.gait_map[current_gait_name]
        gait_duration = gait_cur.duration()
        gait_seq = gait_cur.mode_sequence()
        gait_event_phase = gait_cur.event_phases()

        time_c = self.cycle_timer_.getCycleTime()
        phase_c = time_c / gait_duration
        idx = gait_cur.get_mode_index_from_phase(phase_c)

        eventPhases = [0.0]
        modeSequence = []

        for i in range(idx, len(gait_seq)):
            modeSequence.append(gait_seq[i])
            phase_i = (gait_event_phase[i + 1] * gait_duration - time_c) / time_period
            if phase_i < 1.0:
                eventPhases.append(phase_i)
            else:
                eventPhases.append(1.0)
                break

        time_l = time_period - (gait_duration - time_c)
        cycle_n = 1.0
        while time_l > 0:
            for i in range(len(gait_seq)):
                modeSequence.append(gait_seq[i])
                phase_i = ((gait_event_phase[i + 1] + cycle_n) * gait_duration - time_c) / time_period
                if phase_i < 1.0:
                    eventPhases.append(phase_i)
                else:
                    eventPhases.append(1.0)
                    break
            cycle_n += 1.0
            time_l -= gait_duration

        modeSchedule = ModeSchedule(duration, eventPhases, modeSequence, gait_duration)
        if not modeSchedule.is_valid_mode_sequence():
            self.nodeHandle_.get_logger().error("GaitSchedule::eval >>> modeSchedule is not valid")
            return None

        return modeSchedule

    def checkGaitTransition(self):
        """
        检查并执行步态转换。
        """
        self.in_transition_.push(True)

        if (self.transition_time_.get() < self.nodeHandle_.get_clock().now().seconds_nanoseconds()[0] or
            self.transition_time_.get() - self.nodeHandle_.get_clock().now().nanoseconds*1e-9 > 100.0):
            self.nodeHandle_.get_logger().error(
                f"Transition time slot: {self.transition_time_.get() - self.nodeHandle_.get_clock().now().nanoseconds*1e-9}s is not valid [0, 100]"
            )
            raise ValueError("Transition time slot is not valid [0, 100]")
        new_gait_name = self.current_gait_.get()
        # loop_rate = self.nodeHandle_.create_rate(1000)
        loop_rate = 1.0 / 1000
        while rclpy.ok() and self.check_.get() and self.gait_buffer_.get() != self.current_gait_.get():
            start_time = time.time()
            current_time = self.nodeHandle_.get_clock().now().nanoseconds*1e-9
            if current_time > self.transition_time_.get():
                # 切换步态
                new_gait_name = self.gait_buffer_.get()
                self.current_gait_.push(new_gait_name)
                # 重新初始化CycleTimer
                new_duration = self.gait_map[new_gait_name].duration
                self.cycle_timer_ = CycleTimer(self.nodeHandle_, new_duration)

            # loop_rate.sleep()  
            now = time.time()
            if now - start_time < loop_rate:
                time.sleep(loop_rate-(now - start_time))             
        self.nodeHandle_.get_logger().warn(f"Gait has been changed to {new_gait_name}")
        self.in_transition_.push(False)

    @staticmethod
    def almost_eq(a: float, b: float, epsilon: float = 1e-6) -> bool:
        """
        检查两个浮点数是否近似相等。

        Args:
            a (float): 第一个数。
            b (float): 第二个数。
            epsilon (float, optional): 允许的误差范围。 Defaults to 1e-6.

        Returns:
            bool: 如果近似相等，则返回True，否则返回False。
        """
        return abs(a - b) < epsilon
