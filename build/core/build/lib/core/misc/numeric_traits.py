# numeric_traits.py

from typing import TypeVar
import sys

# 定义类型变量，主要用于类型提示
T = TypeVar('T', bound=float)

def limit_epsilon() -> float:
    """
    如果一个浮点数 v 在 w 的 limit_epsilon 近似范围内，则认为 v 接近 w。
    这个 limit_epsilon 值应该大于 weak_epsilon 值。

    Returns:
        float: limit epsilon 值，默认为 1e-6。
    """
    return 1e-6

def weak_epsilon() -> float:
    """
    定义比较时的精度。

    Returns:
        float: weak epsilon 值，默认为 1e-9。
    """
    return 1e-9

# 示例用法（可选）
if __name__ == "__main__":
    print("limit_epsilon():", limit_epsilon())
    print("weak_epsilon():", weak_epsilon())
