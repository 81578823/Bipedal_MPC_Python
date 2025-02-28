# cubic_spline_trajectory.py

import numpy as np
from typing import List
from .trajectory_base import TrajectoryBase
from .cubic_spline_interpolation import CubicSplineInterpolation, BoundaryType, SplineType


class CubicSplineTrajectory(TrajectoryBase[np.ndarray, np.ndarray]):
    """
    CubicSplineTrajectory 类用于执行多维三次样条轨迹插值。
    它继承自 TrajectoryBase，并使用多个 CubicSplineInterpolation 实例来处理每个维度的插值。
    """

    def __init__(self, n_dim: int,
                 spline_type: SplineType = SplineType.CSPLINE,
                 monotonic: bool = False):
        """
        初始化 CubicSplineTrajectory 对象。

        Args:
            n_dim (int): 轨迹的维度。
            spline_type (SplineType, optional): 样条类型。默认为经典三次样条 (CSPLINE)。
            monotonic (bool, optional): 是否使轨迹单调。默认为 False。
        """
        super().__init__()
        self.n_dim_ = n_dim
        self.spline_type_ = spline_type
        self.monotonic_ = monotonic
        self.splines_array_: List[CubicSplineInterpolation] = []

    def set_boundary(self, left: BoundaryType, left_value: np.ndarray,
                    right: BoundaryType, right_value: np.ndarray) -> None:
        """
        设置每个维度的边界条件。

        Args:
            left (BoundaryType): 左边界条件类型。
            left_value (np.ndarray): 左边界条件值，形状应为 (n_dim,)。
            right (BoundaryType): 右边界条件类型。
            right_value (np.ndarray): 右边界条件值，形状应为 (n_dim,)。

        Raises:
            AssertionError: 如果左边界或右边界的值的维度不匹配。
        """
        assert left_value.shape[0] == self.n_dim_, "left_value 的维度必须与 n_dim_ 相同。"
        assert right_value.shape[0] == self.n_dim_, "right_value 的维度必须与 n_dim_ 相同。"

        if len(self.splines_array_) != self.n_dim_:
            self.splines_array_.clear()
            for _ in range(self.n_dim_):
                spline = CubicSplineInterpolation(spline_type=self.spline_type_,
                                                 monotonic=self.monotonic_)
                self.splines_array_.append(spline)
        
        for n in range(self.n_dim_):
            self.splines_array_[n].set_boundary(left, left_value[n],
                                               right, right_value[n])

    def fit(self, time: List[float], value: List[np.ndarray]) -> None:
        """
        拟合多维轨迹数据。

        Args:
            time (List[float]): 时间点列表。
            value (List[np.ndarray]): 轨迹值列表，每个元素是形状为 (n_dim,) 的数组。

        Raises:
            AssertionError: 如果轨迹值的维度不匹配。
        """

        # print("self.n_dim_",self.n_dim_)
        # print("value.shape[0]",value[0].shape[0])
        assert all(val.shape[0] == self.n_dim_ for val in value), \
            "所有轨迹值的维度必须与 n_dim_ 相同。"
        # for val in value:
            # print("val",val)
            # print("self.n_dim_",self.n_dim_)    


        if len(self.splines_array_) != self.n_dim_:
            self.splines_array_.clear()
            for _ in range(self.n_dim_):
                self.splines_array_.append(CubicSplineInterpolation(spline_type=self.spline_type_,
                                                                     monotonic=self.monotonic_))

        for n in range(self.n_dim_):
            y = list([float(val[n]) for val in value])
            # print("y",y)
            # print("time",time)
            self.splines_array_[n].set_points(time, y)
        
        self.set_time_interval(time[0], time[-1])

    def evaluate(self, time: float) -> np.ndarray:
        """
        在给定时间点评估多维轨迹。

        Args:
            time (float): 需要评估的时间点。

        Returns:
            np.ndarray: 轨迹在该时间点的值，形状为 (n_dim,)。
        """
        assert len(self.splines_array_) == self.n_dim_, "spline 数量与 n_dim_ 不匹配。"
        clamped_time = np.clip(time, self.ts(), self.tf())
        sample = np.zeros(self.n_dim_)
        for n in range(self.n_dim_):
            sample[n] = self.splines_array_[n].evaluate(clamped_time)
        return sample

    def evaluate_multiple(self, time_array: List[float]) -> List[np.ndarray]:
        """
        在给定时间数组中评估多维轨迹。

        Args:
            time_array (List[float]): 需要评估的时间点列表。

        Returns:
            List[np.ndarray]: 轨迹在每个时间点的值列表，形状为 (n_dim,)。
        """
        return [self.evaluate(t) for t in time_array]

    def derivative(self, time: float, n_order: int) -> np.ndarray:
        """
        在给定时间点计算多维轨迹的导数。

        Args:
            time (float): 需要计算导数的时间点。
            n_order (int): 导数的阶数（1 或 2）。

        Returns:
            np.ndarray: 轨迹在该时间点的导数，形状为 (n_dim,)。
        """
        assert len(self.splines_array_) == self.n_dim_, "spline 数量与 n_dim_ 不匹配。"
        assert n_order > 0, "导数阶数必须大于 0。"
        clamped_time = np.clip(time, self.ts(), self.tf())
        derivative_sample = np.zeros(self.n_dim_)
        for n in range(self.n_dim_):
            derivative_sample[n] = self.splines_array_[n].derivative(clamped_time, n_order)
        return derivative_sample

    def derivative_multiple(self, time_array: List[float], n_order: int) -> List[np.ndarray]:
        """
        在给定时间数组中计算多维轨迹的导数。

        Args:
            time_array (List[float]): 需要计算导数的时间点列表。
            n_order (int): 导数的阶数（1 或 2）。

        Returns:
            List[np.ndarray]: 轨迹在每个时间点的导数值列表，形状为 (n_dim,)。
        """
        return [self.derivative(t, n_order) for t in time_array]


# 示例用法（可选）
if __name__ == "__main__":
    # 导入必要的类和枚举
    from .cubic_spline_trajectory import CubicSplineTrajectory
    from .cubic_spline_interpolation import BoundaryType, SplineType

    # 创建一个3维的三次样条轨迹
    n_dim = 3
    spline_type = SplineType.CSPLINE
    monotonic = False
    trajectory = CubicSplineTrajectory(n_dim=n_dim, spline_type=spline_type, monotonic=monotonic)

    # 设置边界条件
    left_boundary = BoundaryType.SECOND_DERIV
    left_values = np.array([0.0, 0.0, 0.0])
    right_boundary = BoundaryType.SECOND_DERIV
    right_values = np.array([0.0, 0.0, 0.0])
    trajectory.set_boundary(left_boundary, left_values, right_boundary, right_values)

    # 拟合轨迹数据
    time_points = [0.0, 1.0, 2.0, 3.0, 4.0]
    value_points = [
        np.array([0.0, 0.0, 0.0]),
        np.array([1.0, 2.0, 3.0]),
        np.array([2.0, 4.0, 6.0]),
        np.array([3.0, 6.0, 9.0]),
        np.array([4.0, 8.0, 12.0])
    ]
    trajectory.fit(time_points, value_points)

    # 评估轨迹
    test_time = 2.5
    sample = trajectory.evaluate(test_time)
    print(f"Trajectory evaluated at time {test_time}: {sample}")

    # 评估多个时间点
    test_times = [0.5, 1.5, 2.5, 3.5]
    samples = trajectory.evaluate_multiple(test_times)
    for t, s in zip(test_times, samples):
        print(f"Trajectory evaluated at time {t}: {s}")

    # 计算导数
    n_order = 1
    derivative_sample = trajectory.derivative(test_time, n_order)
    print(f"First derivative at time {test_time}: {derivative_sample}")

    # 计算多个时间点的导数
    derivative_samples = trajectory.derivative_multiple(test_times, n_order)
    for t, ds in zip(test_times, derivative_samples):
        print(f"First derivative at time {t}: {ds}")
