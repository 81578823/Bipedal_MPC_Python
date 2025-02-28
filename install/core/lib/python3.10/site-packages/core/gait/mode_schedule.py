# mode_schedule.py

from dataclasses import dataclass
from typing import List
import math

# 假设 scalar_t 为 float
scalar_t = float

# 定义一个小的 epsilon，用于近似比较
EPSILON = 1e-9

def almost_eq(a: scalar_t, b: scalar_t, epsilon: scalar_t = EPSILON) -> bool:
    """判断两个浮点数是否近似相等。"""
    return math.isclose(a, b, abs_tol=epsilon)

def limit_epsilon() -> scalar_t:
    """返回一个很小的正数，表示 epsilon。"""
    return EPSILON

class ModeSchedule:
    """
    ModeSchedule 类，用于管理步态模式的调度。
    """
    def __init__(self, duration: scalar_t, event_phases: List[scalar_t],
                 mode_sequence: List[int], gait_cycle: scalar_t = 1.0):
        self.duration_ = duration
        self.event_phases_ = event_phases
        self.mode_sequence_ = mode_sequence
        self.gait_cycle_ = gait_cycle

    def duration(self) -> scalar_t:
        return self.duration_

    def gait_cycle(self) -> scalar_t:
        return self.gait_cycle_

    def event_phases(self) -> List[scalar_t]:
        return self.event_phases_

    def mode_sequence(self) -> List[int]:
        return self.mode_sequence_

    def is_valid_mode_sequence(self) -> bool:
        valid_gait = True
        valid_gait &= self.duration_ > 0.0
        if not self.event_phases_:
            return False
        valid_gait &= almost_eq(self.event_phases_[0], 0.0)
        valid_gait &= almost_eq(self.event_phases_[-1], 1.0)
        valid_gait &= all(
            -limit_epsilon() < phase < 1.0 + limit_epsilon()
            for phase in self.event_phases_
        )
        valid_gait &= self.event_phases_ == sorted(self.event_phases_)
        valid_gait &= len(self.event_phases_) - 1 == len(self.mode_sequence_)
        return valid_gait

    def get_event_phase_from_mode_index(self, mode_idx: int) -> scalar_t:
        event_phase = 0.0
        for k, mode in enumerate(self.mode_sequence_):
            if mode == mode_idx:
                event_phase = self.event_phases_[k]
        return event_phase

    def is_valid_phase(self, phase: scalar_t) -> bool:
        return 0.0 <= phase <= 1.0

    def wrap_phase(self, phase: scalar_t) -> scalar_t:
        phase = math.fmod(phase, 1.0)
        if phase < 0.0:
            phase += 1.0
        return phase

    def get_mode_index_from_phase(self, phase: scalar_t) -> int:
        assert self.is_valid_phase(phase), "Phase is not valid."
        assert self.is_valid_mode_sequence(), "Mode sequence is not valid."
        # 找到第一个大于 phase 的 event_phase
        first_larger = next((i for i, p in enumerate(self.event_phases_) if p > phase), len(self.event_phases_))
        if first_larger != len(self.event_phases_):
            return max(first_larger - 1, 0)
        else:
            return len(self.mode_sequence_) - 1

    def get_mode_from_phase(self, phase: scalar_t) -> int:
        assert self.is_valid_phase(phase), "Phase is not valid."
        assert self.is_valid_mode_sequence(), "Mode sequence is not valid."
        mode_index = self.get_mode_index_from_phase(phase)
        return self.mode_sequence_[mode_index]

    def time_left_in_mode_sequence(self, phase: scalar_t) -> scalar_t:
        assert self.is_valid_phase(phase), "Phase is not valid."
        assert self.is_valid_mode_sequence(), "Mode sequence is not valid."
        return (1.0 - phase) * self.duration_

    def time_left_in_mode(self, phase: scalar_t) -> scalar_t:
        assert self.is_valid_phase(phase), "Phase is not valid."
        assert self.is_valid_mode_sequence(), "Mode sequence is not valid."
        mode_index = self.get_mode_index_from_phase(phase)
        if mode_index < len(self.event_phases_) - 1:
            return (self.event_phases_[mode_index + 1] - phase) * self.duration_
        else:
            return self.time_left_in_mode_sequence(phase)

    def print(self) -> None:
        print(f"#### Duration:       {self.duration_}")
        print("#### Event phases:  {", end='')
        print(", ".join(map(str, self.event_phases_)), end='}\n')
        print("#### Mode sequence: {", end='')
        print(", ".join(map(str, self.mode_sequence_)), end='}\n')
