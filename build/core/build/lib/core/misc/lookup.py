# lookup.py

from typing import List, TypeVar, Optional
import bisect
import math

# 类型别名，假设 SCALAR 为 float
SCALAR = TypeVar('SCALAR', bound=float)


def almost_eq(a: float, b: float, eps: float = 1e-9) -> bool:
    """
    判断两个浮点数是否在给定的容差范围内近似相等。

    Args:
        a (float): 第一个数。
        b (float): 第二个数。
        eps (float, optional): 容差。默认为1e-9。

    Returns:
        bool: 如果两个数的差的绝对值小于 eps，则返回 True，否则返回 False。
    """
    return math.isclose(a, b, abs_tol=eps)


def weak_epsilon() -> float:
    """
    返回一个较小的 epsilon 值，用于容差比较。

    Returns:
        float: 一个很小的正数。
    """
    return 1e-9


def find_first_index_within_tol(data_array: List[SCALAR], value: SCALAR, eps: float = None) -> int:
    """
    在已排序的 data_array 中查找第一个与 value 在 eps 容差范围内的元素的索引。

    Args:
        data_array (List[SCALAR]): 已排序的数据数组。
        value (SCALAR): 查询值。
        eps (float, optional): 容差。默认为 weak_epsilon() 的值。

    Returns:
        int: 匹配元素的索引。

    Raises:
        ValueError: 如果没有找到匹配的元素。
    """
    if eps is None:
        eps = weak_epsilon()

    for i, data in enumerate(data_array):
        if abs(data - value) < eps:
            return i

    # 如果未找到匹配项，抛出异常
    msg = (
        "[find_first_index_within_tol] Value not found within tolerance.\n"
        f"\tdataArray: {data_array}\n"
        f"\tvalue: {value}\n"
        f"\tepsilon: {eps}"
    )
    raise ValueError(msg)


def find_index_in_time_array(time_array: List[SCALAR], time: SCALAR) -> int:
    """
    在已排序的 time_array 中查找第一个大于或等于 time 的元素的索引。

    Args:
        time_array (List[SCALAR]): 已排序的时间数组。
        time (SCALAR): 查询时间。

    Returns:
        int: 插入点的索引，介于 [0, len(time_array)] 之间。
    """
    return bisect.bisect_left(time_array, time)


def find_interval_in_time_array(time_array: List[SCALAR], time: SCALAR) -> int:
    """
    在已排序的 time_array 中查找 time 所在的区间索引。

    区间索引的定义如下：
        ------ | ----- | ---  ... ---    | -----
              t0     t1              t(n-1)
        Interval -1       0      1   ...  (n-2)    (n-1)

    Args:
        time_array (List[SCALAR]): 已排序的时间数组。
        time (SCALAR): 查询时间。

    Returns:
        int: 区间索引，介于 [-1, len(time_array) - 1] 之间。
    """
    index = find_index_in_time_array(time_array, time)
    return index - 1


def find_active_interval_in_time_array(time_array: List[SCALAR], time: SCALAR) -> int:
    """
    与 find_interval_in_time_array 类似，但有一个额外规则：
    如果 time == t0，则返回 0 而不是 -1。

    这意味着任何查询 t_front <= t <= t_back 都会被分配到区间 [0, len(time_array) - 2]。

    Args:
        time_array (List[SCALAR]): 已排序的时间数组。
        time (SCALAR): 查询时间。

    Returns:
        int: 活动区间索引，介于 [-1, len(time_array) - 1] 之间。
    """
    if not time_array:
        return -1  # 空数组，返回 -1

    if almost_eq(time, time_array[0]):
        return 0
    else:
        return find_interval_in_time_array(time_array, time)


def find_bounded_active_interval_in_time_array(time_array: List[SCALAR], time: SCALAR) -> int:
    """
    包装 find_active_interval_in_time_array 并进行边界检查。
    如果 time 小于 time_array 的第一个元素或大于最后一个元素，则抛出异常。
    还会在 time_array 为空或只有一个元素时抛出异常。

    Args:
        time_array (List[SCALAR]): 已排序的时间数组。
        time (SCALAR): 查询时间。

    Returns:
        int: 活动区间索引，介于 [0, len(time_array) - 2] 之间。

    Raises:
        ValueError: 如果 time_array 为空，或者 time 超出范围，或者 time_array 只有一个元素。
    """
    if not time_array:
        raise ValueError("[find_bounded_active_interval_in_time_array] Time array is empty.")

    if len(time_array) == 1:
        raise ValueError("[find_bounded_active_interval_in_time_array] Time array must have at least two elements.")

    partition = find_active_interval_in_time_array(time_array, time)

    if partition < 0:
        msg = (
            "[find_bounded_active_interval_in_time_array] Given time is less than the start time "
            f"(givenTime: {time} < timeArray.front(): {time_array[0]})."
        )
        raise ValueError(msg)

    if partition >= len(time_array) - 1:
        msg = (
            "[find_bounded_active_interval_in_time_array] Given time is greater than the final time "
            f"(timeArray.back(): {time_array[-1]} < givenTime: {time})."
        )
        raise ValueError(msg)

    return partition


# 示例用法（可选）
if __name__ == "__main__":
    # 测试 find_first_index_within_tol
    data = [0.0, 1.0, 2.0, 3.0, 4.0]
    value = 2.000000001
    try:
        index = find_first_index_within_tol(data, value)
        print(f"find_first_index_within_tol: Value {value} found at index {index}.")
    except ValueError as e:
        print(e)

    # 测试 find_index_in_time_array
    time_array = [0.0, 1.0, 2.0, 3.0, 4.0]
    query_time = 2.5
    index = find_index_in_time_array(time_array, query_time)
    print(f"find_index_in_time_array: Query time {query_time} has index {index}.")

    # 测试 find_interval_in_time_array
    interval = find_interval_in_time_array(time_array, query_time)
    print(f"find_interval_in_time_array: Query time {query_time} is in interval {interval}.")

    # 测试 find_active_interval_in_time_array
    active_interval = find_active_interval_in_time_array(time_array, query_time)
    print(f"find_active_interval_in_time_array: Query time {query_time} is in active interval {active_interval}.")

    # 测试 find_bounded_active_interval_in_time_array
    try:
        bounded_interval = find_bounded_active_interval_in_time_array(time_array, query_time)
        print(f"find_bounded_active_interval_in_time_array: Query time {query_time} is in bounded interval {bounded_interval}.")
    except ValueError as e:
        print(e)

    # 测试边界情况
    boundary_time = 0.0
    active_interval = find_active_interval_in_time_array(time_array, boundary_time)
    print(f"find_active_interval_in_time_array: Query time {boundary_time} is in active interval {active_interval}.")

    try:
        bounded_interval = find_bounded_active_interval_in_time_array(time_array, boundary_time)
        print(f"find_bounded_active_interval_in_time_array: Query time {boundary_time} is in bounded interval {bounded_interval}.")
    except ValueError as e:
        print(e)

    # 测试超出范围的时间
    out_of_range_time = 5.0
    try:
        bounded_interval = find_bounded_active_interval_in_time_array(time_array, out_of_range_time)
        print(f"find_bounded_active_interval_in_time_array: Query time {out_of_range_time} is in bounded interval {bounded_interval}.")
    except ValueError as e:
        print(e)
