# motion_phase_definition.py

from enum import Enum
from typing import List
import math

# 类型别名，假设 scalar_t 为 float
scalar_t = float

class ModeNumber(Enum):
    """
    枚举类型，用于表示不同的模式编号。
    """
    FLY = 0
    LF = 1
    RF = 2
    STANCE = 3

def mode_number_to_stance_leg(mode_number: int) -> List[bool]:
    """
    将模式编号转换为支撑腿标志。
    
    返回一个包含两个布尔值的列表，表示左腿和右腿的支撑状态。
    
    Args:
        mode_number (int): 模式编号（0 到 3）。
    
    Returns:
        List[bool]: 支撑腿标志列表 [左腿, 右腿]。
    """
    if mode_number == ModeNumber.FLY.value:
        return [False, False]
    elif mode_number == ModeNumber.LF.value:
        return [True, False]
    elif mode_number == ModeNumber.RF.value:
        return [False, True]
    elif mode_number == ModeNumber.STANCE.value:
        return [True, True]
    else:
        raise ValueError(f"无效的 mode_number: {mode_number}")

def stance_leg_to_mode_number(stance_legs: List[bool]) -> int:
    """
    将支撑腿标志转换为模式编号。
    
    Args:
        stance_legs (List[bool]): 支撑腿标志列表 [左腿, 右腿]。
    
    Returns:
        int: 对应的模式编号。
    """
    if len(stance_legs) != 2:
        raise ValueError("stance_legs 必须包含两个布尔值 [左腿, 右腿]。")
    
    left, right = stance_legs
    return int(left) + 2 * int(right)

def mode_number_to_string(mode_number: int) -> str:
    """
    将模式编号转换为对应的字符串表示。
    
    Args:
        mode_number (int): 模式编号（0 到 3）。
    
    Returns:
        str: 对应的模式名称。
    """
    mode_to_name = {
        ModeNumber.FLY.value: "FLY",
        ModeNumber.LF.value: "LF",
        ModeNumber.RF.value: "RF",
        ModeNumber.STANCE.value: "STANCE",
    }
    if mode_number in mode_to_name:
        return mode_to_name[mode_number]
    else:
        raise ValueError(f"无效的 mode_number: {mode_number}")

def string_to_mode_number(mode_string: str) -> int:
    """
    将模式名称字符串转换为对应的模式编号。
    
    Args:
        mode_string (str): 模式名称（"FLY", "LF", "RF", "STANCE"）。
    
    Returns:
        int: 对应的模式编号。
    """
    name_to_mode = {
        "FLY": ModeNumber.FLY.value,
        "LF": ModeNumber.LF.value,
        "RF": ModeNumber.RF.value,
        "STANCE": ModeNumber.STANCE.value,
    }
    if mode_string in name_to_mode:
        return name_to_mode[mode_string]
    else:
        raise ValueError(f"无效的 mode_string: {mode_string}")

# 以下是类型别名的占位符，如果需要可以根据实际需求进行实现
# from typing import Tuple
# import numpy as np
# vector3_t = np.ndarray  # 或者其他合适的类型
# matrix3_t = np.ndarray
# quaternion_t = np.quaternion  # 需要安装 numpy-quaternion 或其他库

# 示例用法（可选）
if __name__ == "__main__":
    # 测试 mode_number_to_stance_leg
    for mode in ModeNumber:
        stance = mode_number_to_stance_leg(mode.value)
        print(f"Mode {mode.name} ({mode.value}): Stance Legs = {stance}")
    
    # 测试 stance_leg_to_mode_number
    test_stances = [
        [False, False],
        [True, False],
        [False, True],
        [True, True],
    ]
    for stance in test_stances:
        mode = stance_leg_to_mode_number(stance)
        print(f"Stance Legs {stance}: Mode Number = {mode}")
    
    # 测试 mode_number_to_string 和 string_to_mode_number
    for mode in ModeNumber:
        mode_str = mode_number_to_string(mode.value)
        mode_num = string_to_mode_number(mode_str)
        print(f"Mode Number {mode.value}: Mode String = {mode_str}, Converted Back = {mode_num}")
