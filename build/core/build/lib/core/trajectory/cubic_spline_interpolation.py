# cubic_spline_interpolation.py

import numpy as np
from enum import Enum
from typing import List
import math

class BoundaryType(Enum):
    FIRST_DERIV = 1
    SECOND_DERIV = 2
    NOT_A_KNOT = 3

class SplineType(Enum):
    LINEAR = 10
    CSPLINE = 30
    CSPLINE_HERMITE = 31

def get_eps() -> float:
    """
    获取机器精度。

    Returns:
        float: 机器精度。
    """
    return np.finfo(float).eps

def solve_cubic(a: float, b: float, c: float, d: float, newton_iter: int = 0) -> List[float]:
    """
    解一元三次方程 a + b*x + c*x^2 + d*x^3 = 0。

    Args:
        a (float): 常数项。
        b (float): 一次项系数。
        c (float): 二次项系数。
        d (float): 三次项系数。
        newton_iter (int, optional): 牛顿迭代步数，用于提高解的精度。默认为 0。

    Returns:
        List[float]: 方程的实数根列表。
    """
    if d == 0.0:
        # 退化为二次方程
        return solve_quadratic(a, b, c, newton_iter)

    # 归一化
    a /= d
    b /= d
    c /= d

    # 转换为抑郁三次方程 z^3 + p*z + q = 0
    p = (3.0 * c - b ** 2) / 3.0
    q = (2.0 * b ** 3 - 9.0 * b * c + 27.0 * a) / 27.0
    discriminant = (q / 2) ** 2 + (p / 3) ** 3

    roots = []

    if discriminant > 0:
        # 一个实根
        sqrt_disc = math.sqrt(discriminant)
        u = np.cbrt(-q / 2 + sqrt_disc)
        v = np.cbrt(-q / 2 - sqrt_disc)
        z = u + v
        roots.append(z - b / 3.0)
    elif discriminant == 0:
        # 多重根
        u = np.cbrt(-q / 2)
        z1 = 2 * u
        z2 = -u
        roots.append(z1 - b / 3.0)
        roots.append(z2 - b / 3.0)
    else:
        # 三个实根
        z = []
        r = math.sqrt(- (p ** 3) / 27.0)
        phi = math.acos(-q / (2 * r))
        z1 = 2 * math.cbrt(r) * math.cos(phi / 3.0) - b / 3.0
        z2 = 2 * math.cbrt(r) * math.cos((phi + 2 * math.pi) / 3.0) - b / 3.0
        z3 = 2 * math.cbrt(r) * math.cos((phi + 4 * math.pi) / 3.0) - b / 3.0
        roots.extend([z1, z2, z3])

    # 牛顿迭代提高精度
    for i in range(len(roots)):
        for _ in range(newton_iter):
            f = d * roots[i] ** 3 + c * roots[i] ** 2 + b * roots[i] + a
            df = 3 * d * roots[i] ** 2 + 2 * c * roots[i] + b
            if df == 0.0:
                break
            roots[i] -= f / df
    roots = sorted(roots)
    return roots

def solve_quadratic(a: float, b: float, c: float, newton_iter: int = 0) -> List[float]:
    """
    解一元二次方程 a + b*x + c*x^2 = 0。

    Args:
        a (float): 常数项。
        b (float): 一次项系数。
        c (float): 二次项系数。
        newton_iter (int, optional): 牛顿迭代步数，用于提高解的精度。默认为 0。

    Returns:
        List[float]: 方程的实数根列表。
    """
    if c == 0.0:
        if b == 0.0:
            if a == 0.0:
                return [0.0]  # 任意x均为解，选取x=0
            else:
                return []  # 无解
        else:
            return [-a / b]

    discriminant = b ** 2 - 4 * c * a
    roots = []
    if discriminant > 0:
        sqrt_disc = math.sqrt(discriminant)
        roots.extend([(-b + sqrt_disc) / (2 * c), (-b - sqrt_disc) / (2 * c)])
    elif discriminant == 0:
        roots.append(-b / (2 * c))
    else:
        # 无实数根
        pass

    # 牛顿迭代提高精度
    for i in range(len(roots)):
        for _ in range(newton_iter):
            f = c * roots[i] ** 2 + b * roots[i] + a
            df = 2 * c * roots[i] + b
            if df == 0.0:
                break
            roots[i] -= f / df
    roots = sorted(roots)
    return roots

class CubicSplineInterpolation:
    """
    三次样条插值类。

    支持线性插值、经典三次样条插值以及三次 Hermite 样条插值。
    还支持不同的边界条件，包括一阶导数、二阶导数和 not-a-knot 条件。
    """

    def __init__(self, spline_type: SplineType = SplineType.CSPLINE, monotonic: bool = False):
        self.spline_type = spline_type
        self.monotonic = monotonic
        self.boundary_left = BoundaryType.SECOND_DERIV
        self.boundary_right = BoundaryType.SECOND_DERIV
        self.boundary_left_value = 0.0
        self.boundary_right_value = 0.0
        self.made_monotonic = monotonic

        self.x = []
        self.y = []
        self.b = []
        self.c = []
        self.d = []
        self.c0 = 0.0

    def set_points(self, x: List[float], y: List[float]):
        """
        设置插值点。

        Args:
            x (List[float]): x 坐标列表。
            y (List[float]): y 坐标列表。
        """
        # print("x",x)
        # print("y",y)
        assert self.is_valid(x, y), "Invalid input points."

        if self.boundary_left == BoundaryType.NOT_A_KNOT or self.boundary_right == BoundaryType.NOT_A_KNOT:
            assert len(x) >= 4, "Not-a-knot boundary condition requires at least 4 points."

        self.x = x
        self.y = y
        n = len(x)
        for i in range(n - 1):
            assert self.x[i] < self.x[i + 1], "x values must be strictly increasing."

        if self.spline_type == SplineType.LINEAR:
            self.d = [0.0] * n
            self.c = [0.0] * n
            self.b = [(self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i]) for i in range(n - 1)]
            self.b.append(self.b[-1])
            self.c[-1] = 0.0
            self.d[-1] = 0.0
        elif self.spline_type == SplineType.CSPLINE:
            self.compute_cspline_coefficients()
        elif self.spline_type == SplineType.CSPLINE_HERMITE:
            self.compute_cspline_hermite_coefficients()
        else:
            raise ValueError("Unsupported spline type.")

        self.c0 = 0.0 if self.boundary_left == BoundaryType.FIRST_DERIV else self.c[0]

        if self.monotonic:
            self.make_monotonic()

    def set_boundary(self, left: BoundaryType, left_value: float, right: BoundaryType, right_value: float):
        """
        设置边界条件。

        Args:
            left (BoundaryType): 左边界条件类型。
            left_value (float): 左边界条件值。
            right (BoundaryType): 右边界条件类型。
            right_value (float): 右边界条件值。
        """
        assert len(self.x) == 0, "set_boundary() must be called before set_points()."
        self.boundary_left = left
        self.boundary_right = right
        self.boundary_left_value = left_value
        self.boundary_right_value = right_value

    def evaluate(self, x: float) -> float:
        """
        评估插值函数在 x 处的值。

        Args:
            x (float): 评估点。

        Returns:
            float: 插值函数在 x 处的值。
        """
        if not self.x:
            raise ValueError("No points have been set for interpolation.")

        n = len(self.x)
        idx = self.find_closest(x)

        h = x - self.x[idx]
        if x < self.x[0]:
            # 左外推
            return (self.c0 * h + self.b[0]) * h + self.y[0]
        elif x > self.x[-1]:
            # 右外推
            return (self.c[-1] * h + self.b[-1]) * h + self.y[-1]
        else:
            return ((self.d[idx] * h + self.c[idx]) * h + self.b[idx]) * h + self.y[idx]

    def derivative(self, x: float, order: int) -> float:
        """
        计算插值函数在 x 处的指定阶导数。

        Args:
            x (float): 计算点。
            order (int): 导数阶数（1 或 2）。

        Returns:
            float: 指定阶导数的值。
        """
        assert order > 0, "Derivative order must be positive."

        if not self.x:
            raise ValueError("No points have been set for interpolation.")

        n = len(self.x)
        idx = self.find_closest(x)
        h = x - self.x[idx]

        if x < self.x[0]:
            # 左外推
            if order == 1:
                return 2.0 * self.c0 * h + self.b[0]
            elif order == 2:
                return 2.0 * self.c0
            else:
                return 0.0
        elif x > self.x[-1]:
            # 右外推
            if order == 1:
                return 2.0 * self.c[-1] * h + self.b[-1]
            elif order == 2:
                return 2.0 * self.c[-1]
            else:
                return 0.0
        else:
            # 插值区间
            if order == 1:
                return (3.0 * self.d[idx] * h + 2.0 * self.c[idx]) * h + self.b[idx]
            elif order == 2:
                return 6.0 * self.d[idx] * h + 2.0 * self.c[idx]
            elif order == 3:
                return 6.0 * self.d[idx]
            else:
                return 0.0

    def info(self) -> str:
        """
        获取插值信息。

        Returns:
            str: 插值信息字符串。
        """
        info_str = f"type {self.spline_type.name}, left boundary {self.boundary_left.name} = {self.boundary_left_value}, "
        info_str += f"right boundary {self.boundary_right.name} = {self.boundary_right_value}\n"
        if self.monotonic:
            info_str += "(spline has been adjusted for piece-wise monotonicity)"
        return info_str

    def make_monotonic(self) -> bool:
        """
        调整样条以保证单调性。

        Returns:
            bool: 如果进行了调整则返回 True，否则 False。
        """
        assert len(self.x) == len(self.y) == len(self.b), "Invalid spline coefficients."
        assert len(self.x) > 2, "At least three points are required."

        modified = False
        n = len(self.x)

        for i in range(n):
            im1 = max(i - 1, 0)
            ip1 = min(i + 1, n - 1)
            if ((self.y[im1] <= self.y[i] <= self.y[ip1] and self.b[i] < 0.0) or
                (self.y[im1] >= self.y[i] >= self.y[ip1] and self.b[i] > 0.0)):
                modified = True
                self.b[i] = 0.0

        for i in range(n - 1):
            h = self.x[i + 1] - self.x[i]
            avg = (self.y[i + 1] - self.y[i]) / h
            if avg == 0.0 and (self.b[i] != 0.0 or self.b[i + 1] != 0.0):
                modified = True
                self.b[i] = 0.0
                self.b[i + 1] = 0.0
            elif ((self.b[i] >= 0.0 and self.b[i + 1] >= 0.0 and avg > 0.0) or
                  (self.b[i] <= 0.0 and self.b[i + 1] <= 0.0 and avg < 0.0)):
                r = math.sqrt(self.b[i] ** 2 + self.b[i + 1] ** 2) / abs(avg)
                if r > 3.0:
                    modified = True
                    self.b[i] *= (3.0 / r)
                    self.b[i + 1] *= (3.0 / r)

        if modified:
            self.set_coeffs_from_b()

        return modified

    def is_valid(self, x: List[float], y: List[float]) -> bool:
        """
        检查输入点是否有效。

        Args:
            x (List[float]): x 坐标列表。
            y (List[float]): y 坐标列表。

        Returns:
            bool: 如果有效则返回 True，否则 False。
        """
        return (len(x) == len(y)) and (len(x) > 2) and all(x[i] < x[i + 1] for i in range(len(x) - 1))
    
    def set_coeffs_from_b(self):
        """
        根据 b 系数计算 c 和 d 系数。
        """
        assert len(self.x) == len(self.y) == len(self.b) , "Invalid spline coefficients."
        assert len(self.x) > 2, "At least three points are required."

        n = len(self.b)
        if len(self.c) != n:
            self.c = [0.0] * n
        if len(self.d) != n:
            self.d = [0.0] * n

        for i in range(n - 1):
            h = self.x[i + 1] - self.x[i]
            self.c[i] = (3.0 * (self.y[i + 1] - self.y[i]) / h - (2.0 * self.b[i] + self.b[i + 1])) / h
            self.d[i] = ((self.b[i + 1] - self.b[i]) / (3.0 * h) - 2.0 / 3.0 * self.c[i]) / h

        # 左外推系数
        self.c0 = 0.0 if self.boundary_left == BoundaryType.FIRST_DERIV else self.c[0]

    def find_closest(self, x_val: float) -> int:
        """
        找到最接近 x_val 的区间索引。

        Args:
            x_val (float): 查询值。

        Returns:
            int: 最接近的索引。
        """
        idx = np.searchsorted(self.x, x_val) - 1
        idx = max(idx, 0)
        return idx

    def compute_cspline_coefficients(self):
        """
        计算经典三次样条的系数。
        """
        n = len(self.x)
        A = np.zeros((n, n))
        rhs = np.zeros(n)

        # 内部点方程
        for i in range(1, n - 1):
            A[i, i - 1] = (1.0 / 3.0) * (self.x[i] - self.x[i - 1])
            A[i, i] = (2.0 / 3.0) * (self.x[i + 1] - self.x[i - 1])
            A[i, i + 1] = (1.0 / 3.0) * (self.x[i + 1] - self.x[i])
            rhs[i] = (self.y[i + 1] - self.y[i]) / (self.x[i + 1] - self.x[i]) - \
                     (self.y[i] - self.y[i - 1]) / (self.x[i] - self.x[i - 1])

        # 左边界条件
        if self.boundary_left == BoundaryType.SECOND_DERIV:
            A[0, 0] = 2.0
            A[0, 1] = 0.0
            rhs[0] = self.boundary_left_value
        elif self.boundary_left == BoundaryType.FIRST_DERIV:
            h = self.x[1] - self.x[0]
            A[0, 0] = 2.0 * h
            A[0, 1] = h
            rhs[0] = 3.0 * ((self.y[1] - self.y[0]) / h - self.boundary_left_value)
        elif self.boundary_left == BoundaryType.NOT_A_KNOT:
            A[0, 0] = -(self.x[2] - self.x[1])
            A[0, 1] = self.x[2] - self.x[0]
            A[0, 2] = -(self.x[1] - self.x[0])
            rhs[0] = 0.0
        else:
            raise ValueError("Unsupported left boundary type.")

        # 右边界条件
        if self.boundary_right == BoundaryType.SECOND_DERIV:
            A[-1, -1] = 2.0
            A[-1, -2] = 0.0
            rhs[-1] = self.boundary_right_value
        elif self.boundary_right == BoundaryType.FIRST_DERIV:
            h = self.x[-1] - self.x[-2]
            A[-1, -1] = 2.0 * h
            A[-1, -2] = h
            rhs[-1] = 3.0 * (self.boundary_right_value - (self.y[-1] - self.y[-2]) / h)
        elif self.boundary_right == BoundaryType.NOT_A_KNOT:
            A[-1, -3] = -(self.x[-1] - self.x[-2])
            A[-1, -2] = self.x[-1] - self.x[-3]
            A[-1, -1] = -(self.x[-2] - self.x[-3])
            rhs[-1] = 0.0
        else:
            raise ValueError("Unsupported right boundary type.")

        # 解决线性方程组
        c = np.linalg.solve(A, rhs)
        self.c = c.tolist()

        # 计算 b 和 d
        self.b = []
        self.d = []
        for i in range(n - 1):
            h = self.x[i + 1] - self.x[i]
            bi = (self.y[i + 1] - self.y[i]) / h - (2.0 * self.c[i] + self.c[i + 1]) * h / 3.0
            self.b.append(bi)
            di = (self.c[i + 1] - self.c[i]) / (3.0 * h)
            self.d.append(di)
        q=self.x[n - 1] - self.x[n - 2]
        t=3.0*self.d[n-2]*q*q+2.0*self.c[n-2]*q+self.b[n-2]
        self.b.append(t)  # Extend b for the last point
        self.d.append(0.0)  # d for the last point

        if self.boundary_right==BoundaryType.FIRST_DERIV:
            self.c[n-1]=0.0

    def compute_cspline_hermite_coefficients(self):
        """
        计算三次 Hermite 样条的系数。
        """
        n = len(self.x)
        self.b = [0.0] * n
        self.c = [0.0] * n
        self.d = [0.0] * n

        for i in range(1, n - 1):
            h = self.x[i + 1] - self.x[i]
            hl = self.x[i] - self.x[i - 1]
            self.b[i] = (-h / (hl * (hl + h)) * self.y[i - 1] +
                        (h - hl) / (hl * h) * self.y[i] +
                        hl / (h * (hl + h)) * self.y[i + 1])

        # 左边界条件
        if self.boundary_left == BoundaryType.FIRST_DERIV:
            self.b[0] = self.boundary_left_value
        elif self.boundary_left == BoundaryType.SECOND_DERIV:
            h = self.x[1] - self.x[0]
            self.b[0] = 0.5 * (-self.b[1] - 0.5 * self.boundary_left_value * h +
                               3.0 * (self.y[1] - self.y[0]) / h)
        elif self.boundary_left == BoundaryType.NOT_A_KNOT:
            h0 = self.x[1] - self.x[0]
            h1 = self.x[2] - self.x[1]
            self.b[0] = (-self.b[1] + 2.0 * (self.y[1] - self.y[0]) / h0 +
                        (h0 ** 2) / (h1 ** 2) * (self.b[1] + self.b[2] - 2.0 * (self.y[2] - self.y[1]) / h1))
        else:
            raise ValueError("Unsupported left boundary type.")

        # 右边界条件
        if self.boundary_right == BoundaryType.FIRST_DERIV:
            self.b[-1] = self.boundary_right_value
            self.c[-1] = 0.0
        elif self.boundary_right == BoundaryType.SECOND_DERIV:
            h = self.x[-1] - self.x[-2]
            self.b[-1] = 0.5 * (-self.b[-2] + 0.5 * self.boundary_right_value * h +
                                3.0 * (self.y[-1] - self.y[-2]) / h)
            self.c[-1] = 0.5 * self.boundary_right_value
        elif self.boundary_right == BoundaryType.NOT_A_KNOT:
            h0 = self.x[-2] - self.x[-3]
            h1 = self.x[-1] - self.x[-2]
            self.b[-1] = (-self.b[-2] + 2.0 * (self.y[-1] - self.y[-2]) / h1 +
                          (h1 ** 2) / (h0 ** 2) * (self.b[-3] + self.b[-2] - 2.0 * (self.y[-2] - self.y[-3]) / h0))
            # Ensure second derivative continuity at the last point
            self.c[-1] = (self.b[-2] + 2.0 * self.b[-1]) / h1 - 3.0 * (self.y[-1] - self.y[-2]) / (h1 ** 2)
        else:
            raise ValueError("Unsupported right boundary type.")

        # d 系数为 0
        self.d = [0.0] * n

        # 计算系数
        self.set_coeffs_from_b()

    def solve(self, y_val: float, ignore_extrapolation: bool = True) -> List[float]:
        """
        解样条方程 spline(x) = y_val，找到所有 x 使得插值函数在 x 处等于 y_val。

        Args:
            y_val (float): 目标值。
            ignore_extrapolation (bool, optional): 是否忽略外推区间。默认为 True。

        Returns:
            List[float]: 满足条件的 x 值列表。
        """
        if not self.x or not self.b or not self.c or not self.d:
            raise ValueError("Spline coefficients are not set.")

        roots = []

        # 左外推
        if not ignore_extrapolation:
            z = solve_cubic(self.y[0] - y_val, self.b[0], self.c0, 0.0, newton_iter=1)
            for root in z:
                if root < 0.0:
                    roots.append(self.x[0] + root)

        # 检查每个分段的根
        for i in range(len(self.x) - 1):
            # 方程为 ((d*h + c)*h + b)*h + a = 0
            a = self.y[i] - y_val
            b = self.b[i]
            c = self.c[i]
            d = self.d[i]
            z = solve_cubic(a, b, c, d, newton_iter=1)
            for root in z:
                h = root
                if -get_eps() <= h < (self.x[i + 1] - self.x[i]):
                    new_root = self.x[i] + h
                    # 避免重复根
                    if roots and abs(roots[-1] - new_root) < get_eps():
                        roots[-1] = new_root
                    else:
                        roots.append(new_root)

        # 右外推
        if not ignore_extrapolation:
            z = solve_cubic(self.y[-1] - y_val, self.b[-1], self.c[-1], 0.0, newton_iter=1)
            for root in z:
                if root >= 0.0:
                    roots.append(self.x[-1] + root)

        return sorted(roots)
