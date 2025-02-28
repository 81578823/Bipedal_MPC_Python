# leg_logic.py

from dataclasses import dataclass
from typing import List
from typing import Optional
# 假设 ModeSchedule 和 modeNumber2StanceLeg 在其他模块中定义
# 请根据实际情况修改导入路径
from .mode_schedule import ModeSchedule
from .motion_phase_definition import mode_number_to_stance_leg

# 类型别名，假设 scalar_t 为 float
scalar_t = float

@dataclass
class TimeInterval:
    start: scalar_t
    end: scalar_t



def get_time_of_next_touch_down(time_cur: scalar_t, mode_schedule: ModeSchedule) -> List[scalar_t]:
    td_time_array: List[scalar_t] = [time_cur + mode_schedule.duration() for _ in range(4)]

    if not mode_schedule.event_phases():
        return td_time_array

    first_phase = mode_schedule.event_phases()[0]
    contact_flag_last = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(first_phase))

    for i in range(2):
        for phase in mode_schedule.event_phases():
            contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase))
            if contact_flag[i] and not contact_flag_last[i]:
                td_time_array[i] = time_cur + phase * mode_schedule.duration()
                break
            contact_flag_last = contact_flag

    return td_time_array

def get_time_of_next_lift_off(time_cur: scalar_t, mode_schedule: ModeSchedule) -> List[scalar_t]:
    lift_time_array: List[scalar_t] = [time_cur + mode_schedule.duration() for _ in range(4)]

    if not mode_schedule.event_phases():
        return lift_time_array

    first_phase = mode_schedule.event_phases()[0]
    # print("first_phase",first_phase)
    contact_flag_last = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(first_phase))
    # print("contact_flag_last",contact_flag_last)


    for i in range(2):
        for phase in mode_schedule.event_phases():
            contact_flag = mode_number_to_stance_leg(mode_schedule.get_mode_from_phase(phase))
            # print("contact_flag",contact_flag)
            if not contact_flag[i] and contact_flag_last[i]:
                lift_time_array[i] = time_cur + phase * mode_schedule.duration()
                break
            contact_flag_last = contact_flag

    return lift_time_array
