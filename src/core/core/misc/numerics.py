# numerics.py

from typing import TypeVar
import math
import sys

# 定义类型变量，主要用于类型提示
SCALAR = TypeVar('SCALAR', bound=float)

def weak_epsilon() -> float:
    """
    返回一个较小的 epsilon 值，用于容差比较。
    类似于 C++ 中的 numeric_traits::weakEpsilon<SCALAR>()。
    
    Returns:
        float: 一个非常小的正数，默认为机器 epsilon。
    """
    return sys.float_info.epsilon

def almost_eq(x: float, y: float, prec: float = None) -> bool:
    """
    判断两个浮点数是否在给定的容差范围内近似相等。
    使用机器 epsilon 来缩放比较精度。
    
    Args:
        x (float): 第一个浮点数。
        y (float): 第二个浮点数。
        prec (float, optional): 比较精度。默认为弱 epsilon 值。
    
    Returns:
        bool: 如果 x 和 y 在容差范围内近似相等，则返回 True，否则返回 False。
    
    Raises:
        TypeError: 如果任意一个参数不是浮点数。
    """
    if not isinstance(x, float):
        raise TypeError("第一个参数必须是浮点数！")
    if not isinstance(y, float):
        raise TypeError("第二个参数必须是浮点数！")
    if prec is not None and not isinstance(prec, float):
        raise TypeError("比较精度参数必须是浮点数！")
    
    if prec is None:
        prec = weak_epsilon()
    
    abs_diff = abs(x - y)
    magnitude = min(abs(x), abs(y))
    
    # 检查是否在容差范围内，或是差值小于最小可表示值（处理子正常数）
    return abs_diff <= prec * magnitude or abs_diff < sys.float_info.min

def almost_le(x: float, y: float, prec: float = None) -> bool:
    """
    判断 x 是否几乎小于或等于 y。
    如果 x 小于 y，或者 x 和 y 在给定的容差范围内近似相等，则返回 True。
    
    Args:
        x (float): 第一个浮点数。
        y (float): 第二个浮点数。
        prec (float, optional): 比较精度。默认为弱 epsilon 值。
    
    Returns:
        bool: 如果 x <= y（考虑容差），则返回 True，否则返回 False。
    
    Raises:
        TypeError: 如果任意一个参数不是浮点数。
    """
    if prec is None:
        return x < y or almost_eq(x, y)
    else:
        return x < y or almost_eq(x, y, prec)

def almost_ge(x: float, y: float, prec: float = None) -> bool:
    """
    判断 x 是否几乎大于或等于 y。
    如果 x 大于 y，或者 x 和 y 在给定的容差范围内近似相等，则返回 True。
    
    Args:
        x (float): 第一个浮点数。
        y (float): 第二个浮点数。
        prec (float, optional): 比较精度。默认为弱 epsilon 值。
    
    Returns:
        bool: 如果 x >= y（考虑容差），则返回 True，否则返回 False。
    
    Raises:
        TypeError: 如果任意一个参数不是浮点数。
    """
    if prec is None:
        return x > y or almost_eq(x, y)
    else:
        return x > y or almost_eq(x, y, prec)

# 示例用法（可选）
if __name__ == "__main__":
    # 测试 almost_eq
    print("Testing almost_eq:")
    print(f"almost_eq(1.000000001, 1.0): {almost_eq(1.000000001, 1.0)}")  # 应为 True
    print(f"almost_eq(1.0001, 1.0): {almost_eq(1.0001, 1.0)}")            # 应为 False

    # 测试 almost_le
    print("\nTesting almost_le:")
    print(f"almost_le(1.0, 2.0): {almost_le(1.0, 2.0)}")  # True
    print(f"almost_le(2.0, 1.0): {almost_le(2.0, 1.0)}")  # False
    print(f"almost_le(1.000000001, 1.0): {almost_le(1.000000001, 1.0)}")  # True

    # 测试 almost_ge
    print("\nTesting almost_ge:")
    print(f"almost_ge(2.0, 1.0): {almost_ge(2.0, 1.0)}")  # True
    print(f"almost_ge(1.0, 2.0): {almost_ge(1.0, 2.0)}")  # False
    print(f"almost_ge(1.000000001, 1.0): {almost_ge(1.000000001, 1.0)}")  # True
