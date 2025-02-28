# cycle_timer.py

import threading
import time
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration

# 假设 Buffer 类已经存在
from core.misc.buffer import Buffer
from core.misc.numeric_traits import weak_epsilon  # 需要定义此函数或变量


class CycleTimer:
    """
    CycleTimer 类用于定时器管理，记录每个周期的开始时间和当前周期时间。
    """

    def __init__(self, node_handle: Node, cycle_duration: float):
        """
        初始化 CycleTimer 对象。

        Args:
            node_handle (Node): ROS 2 节点句柄。
            cycle_duration (float): 周期持续时间（秒）。
        """
        self.node_handle_ = node_handle
        self.cycle_duration_ = cycle_duration

        if self.cycle_duration_ < weak_epsilon():
            raise ValueError("cycle_duration less than epsilon")

        self.cycle_start_point_ = Buffer[float]()
        self.current_cycle_time_ = Buffer[float]()

        # 初始化周期开始时间为当前时间
        current_time = self.node_handle_.get_clock().now().nanoseconds*1e-9
        self.cycle_start_point_.push(current_time)
        self.current_cycle_time_.push(0.0)

        # 运行标志
        self.run_ = Buffer[bool]()
        self.run_.push(True)

        # 启动内部循环线程
        self.inner_loop_thread_ = threading.Thread(target=self.innerLoop)
        self.inner_loop_thread_.start()

    def __del__(self):
        """
        析构函数，用于停止线程和清理资源。
        """
        self.run_.push(False)
        if self.inner_loop_thread_.is_alive():
            self.inner_loop_thread_.join()

    def innerLoop(self):
        """
        内部循环，用于定期更新周期时间。
        """
        # 使用 ROS 2 的 Rate 功能进行循环控制
        # loop_rate = self.node_handle_.create_rate(10000.0)  # 10,000 
        loop_rate = 1.0/10000

        while rclpy.ok() and self.run_.get():
            start_time = time.time()
            current_time = self.node_handle_.get_clock().now().nanoseconds*1e-9

            # 更新周期开始点
            while self.cycle_start_point_.get() < (current_time - self.cycle_duration_):
                new_start = self.cycle_start_point_.get() + self.cycle_duration_
                self.cycle_start_point_.push(new_start)

            if self.cycle_start_point_.get() > current_time:
                self.cycle_start_point_.push(current_time)

            # 计算当前周期时间
            cycle_time = current_time - self.cycle_start_point_.get()
            self.current_cycle_time_.push(cycle_time)

            now = time.time()
            if now - start_time < loop_rate:
                time.sleep(loop_rate - (now - start_time))

            # loop_rate.sleep()

    def timerReset(self):
        """
        重置定时器，将周期开始点设为当前时间。
        """
        current_time = self.node_handle_.get_clock().now().nanoseconds*1e-9
        self.cycle_start_point_.push(current_time)

    def getCycleTime(self) -> float:
        """
        获取当前周期时间。

        Returns:
            float: 当前周期时间（秒）。
        """
        return self.current_cycle_time_.get()
