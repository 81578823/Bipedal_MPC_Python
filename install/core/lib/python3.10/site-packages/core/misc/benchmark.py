# benchmark.py

from dataclasses import dataclass
from typing import Optional
import time


# 类型别名，假设 scalar_t 为 float
scalar_t = float


class RepeatedTimer:
    """
    计时器类，可以重复启动和停止。会收集所有测量区间的统计数据。
    """

    def __init__(self):
        self.num_timed_intervals: int = 0
        self.total_time_ns: int = 0
        self.max_interval_time_ns: int = 0
        self.last_interval_time_ns: int = 0
        self.start_time_ns: int = time.perf_counter_ns()

    def reset(self) -> None:
        """
        重置计时器的统计数据。
        """
        self.num_timed_intervals = 0
        self.total_time_ns = 0
        self.max_interval_time_ns = 0
        self.last_interval_time_ns = 0
        self.start_time_ns = time.perf_counter_ns()

    def start_timer(self) -> None:
        """
        开始计时一个区间。
        """
        self.start_time_ns = time.perf_counter_ns()

    def end_timer(self) -> None:
        """
        停止计时一个区间，并更新统计数据。
        """
        end_time_ns = time.perf_counter_ns()
        interval_time_ns = end_time_ns - self.start_time_ns
        self.last_interval_time_ns = interval_time_ns
        if interval_time_ns > self.max_interval_time_ns:
            self.max_interval_time_ns = interval_time_ns
        self.total_time_ns += interval_time_ns
        self.num_timed_intervals += 1

    def get_num_timed_intervals(self) -> int:
        """
        @return 计时的区间数量
        """
        return self.num_timed_intervals

    def get_total_in_milliseconds(self) -> scalar_t:
        """
        @return 所有计时区间的总累积时间（毫秒）
        """
        return self.total_time_ns / 1e6

    def get_max_interval_in_milliseconds(self) -> scalar_t:
        """
        @return 单个区间的最大持续时间（毫秒）
        """
        return self.max_interval_time_ns / 1e6

    def get_last_interval_in_milliseconds(self) -> scalar_t:
        """
        @return 最近一次计时区间的持续时间（毫秒）
        """
        return self.last_interval_time_ns / 1e6

    def get_average_in_milliseconds(self) -> Optional[scalar_t]:
        """
        @return 所有计时区间的平均持续时间（毫秒）
                 如果没有计时区间，则返回 None
        """
        if self.num_timed_intervals == 0:
            return None
        return self.get_total_in_milliseconds() / self.num_timed_intervals

    def __str__(self) -> str:
        """
        返回计时器的统计信息字符串表示。
        """
        average = self.get_average_in_milliseconds()
        average_str = f"{average:.6f} ms" if average is not None else "N/A"
        return (
            f"RepeatedTimer Statistics:\n"
            f"  Number of Timed Intervals: {self.num_timed_intervals}\n"
            f"  Total Time: {self.get_total_in_milliseconds():.6f} ms\n"
            f"  Max Interval Time: {self.get_max_interval_in_milliseconds():.6f} ms\n"
            f"  Last Interval Time: {self.get_last_interval_in_milliseconds():.6f} ms\n"
            f"  Average Interval Time: {average_str}"
        )


# 示例用法（可选）
if __name__ == "__main__":
    import random

    # 创建 RepeatedTimer 实例
    timer = RepeatedTimer()

    # 模拟多次计时
    for _ in range(5):
        timer.start_timer()
        # 模拟一些工作负载
        time.sleep(random.uniform(0.01, 0.05))  # 10ms 到 50ms
        timer.end_timer()

    # 打印统计信息
    print(timer)
