# motion_phase_definition.py

from typing import Tuple
from enum import IntEnum
import numpy as np
from types import (
    scalar_t,
    almost_eq,
    vector3_t,
    matrix3_t,
    quaternion_t
)

# 定义 feet_array_t 和 contact_flag_t
FeetArray = Tuple[bool, bool, bool, bool]  # {LF, RF, LH, RH}
ContactFlag = FeetArray

class ModeNumber(IntEnum):
    """
    定义模式编号枚举，对应于四足机器人的不同支撑腿配置。
    """
    FLY = 0          # 0-leg-stance
    RH = 1           # RH
    LH = 2           # LH
    LH_RH = 3        # LH, RH
    RF = 4           # RF
    RF_RH = 5        # RF, RH
    RF_LH = 6        # RF, LH
    RF_LH_RH = 7     # RF, LH, RH
    LF = 8           # LF
    LF_RH = 9        # LF, RH
    LF_LH = 10       # LF, LH
    LF_LH_RH = 11    # LF, LH, RH
    LF_RF = 12       # LF, RF
    LF_RF_RH = 13    # LF, RF, RH
    LF_RF_LH = 14    # LF, RF, LH
    STANCE = 15      # 4-leg-stance

def mode_number_to_stance_leg(mode_number: int) -> ContactFlag:
    """
    根据给定的模式编号返回对应的支撑腿标志。

    Args:
        mode_number (int): 模式编号。

    Returns:
        ContactFlag: 一个包含四个布尔值的元组，表示 {LF, RF, LH, RH} 是否接触地面。

    Raises:
        ValueError: 如果模式编号无效。
    """
    if mode_number == ModeNumber.FLY:
        return (False, False, False, False)
    elif mode_number == ModeNumber.RH:
        return (False, False, False, True)
    elif mode_number == ModeNumber.LH:
        return (False, False, True, False)
    elif mode_number == ModeNumber.LH_RH:
        return (False, False, True, True)
    elif mode_number == ModeNumber.RF:
        return (False, True, False, False)
    elif mode_number == ModeNumber.RF_RH:
        return (False, True, False, True)
    elif mode_number == ModeNumber.RF_LH:
        return (False, True, True, False)
    elif mode_number == ModeNumber.RF_LH_RH:
        return (False, True, True, True)
    elif mode_number == ModeNumber.LF:
        return (True, False, False, False)
    elif mode_number == ModeNumber.LF_RH:
        return (True, False, False, True)
    elif mode_number == ModeNumber.LF_LH:
        return (True, False, True, False)
    elif mode_number == ModeNumber.LF_LH_RH:
        return (True, False, True, True)
    elif mode_number == ModeNumber.LF_RF:
        return (True, True, False, False)
    elif mode_number == ModeNumber.LF_RF_RH:
        return (True, True, False, True)
    elif mode_number == ModeNumber.LF_RF_LH:
        return (True, True, True, False)
    elif mode_number == ModeNumber.STANCE:
        return (True, True, True, True)
    else:
        raise ValueError(f"Invalid mode number: {mode_number}")

def stance_leg_to_mode_number(stance_leg: ContactFlag) -> int:
    """
    根据给定的支撑腿标志返回对应的模式编号。

    Args:
        stance_leg (ContactFlag): 一个包含四个布尔值的元组，表示 {LF, RF, LH, RH} 是否接触地面。

    Returns:
        int: 对应的模式编号。
    """
    lf, rf, lh, rh = stance_leg
    mode_number = int(rh) + 2 * int(lh) + 4 * int(rf) + 8 * int(lf)
    return mode_number

# 创建模式编号与字符串的映射
MODE_NUMBER_TO_STRING = {mode.value: mode.name for mode in ModeNumber}
STRING_TO_MODE_NUMBER = {mode.name: mode.value for mode in ModeNumber}

def mode_number_to_string(mode_number: int) -> str:
    """
    根据模式编号返回对应的字符串表示。

    Args:
        mode_number (int): 模式编号。

    Returns:
        str: 模式的字符串名称。如果模式编号无效，返回 "UNKNOWN_MODE"。
    """
    return MODE_NUMBER_TO_STRING.get(mode_number, "UNKNOWN_MODE")

def string_to_mode_number(mode_string: str) -> int:
    """
    根据模式字符串返回对应的模式编号。

    Args:
        mode_string (str): 模式的字符串名称。

    Returns:
        int: 对应的模式编号。

    Raises:
        ValueError: 如果模式字符串无效。
    """
    if mode_string in STRING_TO_MODE_NUMBER:
        return STRING_TO_MODE_NUMBER[mode_string]
    else:
        raise ValueError(f"Invalid mode string: {mode_string}")
