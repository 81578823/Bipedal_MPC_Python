# types.py

from typing import List, Optional
from dataclasses import dataclass, field
import numpy as np

# 定义标量类型
scalar_t = float

# Type Aliases

# size_t 轨迹类型
size_array_t = List[int]
# size_t 轨迹的数组类型
size_array2_t = List[size_array_t]

# 标量轨迹类型
scalar_array_t = List[scalar_t]
# 标量轨迹的数组类型
scalar_array2_t = List[scalar_array_t]
# 标量轨迹数组的数组类型
scalar_array3_t = List[scalar_array2_t]

# 四元数类型
# 注意：Python 标准库没有内置的四元数类型，可以使用 numpy 数组表示，形状为 (4,)
quaternion_t = np.ndarray  # Shape (4,)

# 向量类型
vector2_t = np.ndarray   # Shape (2,)
vector3_t = np.ndarray   # Shape (3,)
vector4_t = np.ndarray   # Shape (4,)
vector6_t = np.ndarray   # Shape (6,)
vector12_t = np.ndarray  # Shape (12,)
# 动态大小向量类型
vector_t = np.ndarray     # Shape (n,)
# 动态向量轨迹类型
vector_array_t = List[vector_t]
# 动态向量轨迹的数组类型
vector_array2_t = List[vector_array_t]
# 动态向量轨迹数组的数组类型
vector_array3_t = List[vector_array2_t]

# 行向量类型
row_vector_t = np.ndarray  # Shape (1, n) 或 (n,)

# 矩阵类型
matrix3_t = np.ndarray     # Shape (3, 3)
matrix4_t = np.ndarray     # Shape (4, 4)
matrix6_t = np.ndarray     # Shape (6, 6)
matrix3x_t = np.ndarray    # Shape (3, n)
matrix4x_t = np.ndarray    # Shape (4, n)
matrix6x_t = np.ndarray    # Shape (6, n)
# 动态大小矩阵类型
matrix_t = np.ndarray      # Shape (n, m)
# 动态矩阵轨迹类型
matrix_array_t = List[matrix_t]
# 动态矩阵轨迹的数组类型
matrix_array2_t = List[matrix_array_t]
# 动态矩阵轨迹数组的数组类型
matrix_array3_t = List[matrix_array2_t]


def almost_eq(a: scalar_t, b: scalar_t, eps: scalar_t = 1e-9) -> bool:
    """
    检查两个浮点数是否在容差范围内近似相等。

    Args:
        a (float): 第一个浮点数。
        b (float): 第二个浮点数。
        eps (float, optional): 容差。默认为 1e-9。

    Returns:
        bool: 如果两个数在容差范围内近似相等，返回 True，否则返回 False。
    """
    return abs(a - b) < eps


@dataclass
class ScalarFunctionLinearApproximation:
    """标量函数的线性近似 f(x,u) = dfdx' dx + dfdu' du + f"""
    dfdx: Optional[vector_t] = field(default=None)
    dfdu: Optional[vector_t] = field(default=None)
    f: scalar_t = 0.0

    def __init__(self, nx: int, nu: int = -1):
        """
        构造函数并调整成员大小。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nx, nu)

    def __iadd__(self, rhs: 'ScalarFunctionLinearApproximation') -> 'ScalarFunctionLinearApproximation':
        """复合加法赋值运算符"""
        if self.dfdx is not None and rhs.dfdx is not None:
            self.dfdx += rhs.dfdx
        if self.dfdu is not None and rhs.dfdu is not None:
            self.dfdu += rhs.dfdu
        self.f += rhs.f
        return self

    def __imul__(self, scalar: scalar_t) -> 'ScalarFunctionLinearApproximation':
        """复合标量乘法赋值运算符"""
        if self.dfdx is not None:
            self.dfdx *= scalar
        if self.dfdu is not None:
            self.dfdu *= scalar
        self.f *= scalar
        return self

    def resize(self, nx: int, nu: int = -1) -> 'ScalarFunctionLinearApproximation':
        """
        调整成员大小。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.dfdx = np.zeros(nx)
        self.dfdu = np.zeros(nu) if nu != -1 else None
        return self

    def set_zero(self, nx: int, nu: int = -1) -> 'ScalarFunctionLinearApproximation':
        """
        调整成员大小并将所有系数设为零。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nx, nu)
        self.f = 0.0
        if self.dfdx is not None:
            self.dfdx.fill(0.0)
        if self.dfdu is not None:
            self.dfdu.fill(0.0)
        return self

    @classmethod
    def Zero(cls, nx: int, nu: int = -1) -> 'ScalarFunctionLinearApproximation':
        """
        工厂函数，创建一个零初始化的对象。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        :return: 给定大小的零初始化对象。
        """
        obj = cls(nx, nu)
        obj.set_zero(nx, nu)
        return obj

    def __str__(self):
        return f"ScalarFunctionLinearApproximation(dfdx={self.dfdx}, dfdu={self.dfdu}, f={self.f})"


def checkSize(stateDim: int, inputDim: int,
             data: ScalarFunctionLinearApproximation,
             dataName: str) -> str:
    """
    检查给定线性近似的大小。
    :param stateDim: 状态数量
    :param inputDim: 输入数量。
    :param data: 给定的线性近似。
    :param dataName: 数据名称，用于错误消息中。
    :return: 错误描述。如果没有错误，返回空字符串。
    """
    errors = []
    if data.dfdx is None or data.dfdx.size != stateDim:
        errors.append(f"{dataName}.dfdx 大小 {data.dfdx.size if data.dfdx is not None else 'None'} 不等于 stateDim {stateDim}。")
    if inputDim != -1:
        if data.dfdu is None or data.dfdu.size != inputDim:
            errors.append(f"{dataName}.dfdu 大小 {data.dfdu.size if data.dfdu is not None else 'None'} 不等于 inputDim {inputDim}。")
    if errors:
        return " ".join(errors)
    return ""


def checkBeingPSD(data: matrix_t, dataName: str) -> str:
    """
    检查给定矩阵是否有效、自伴和正半定（PSD）。
    :param data: 给定的矩阵。
    :param dataName: 数据名称，用于错误消息中。
    :return: 错误描述。如果没有错误，返回空字符串。
    """
    errors = []
    if not np.allclose(data, data.T, atol=1e-8):
        errors.append(f"{dataName} 不是对称的。")
    eigenvalues = np.linalg.eigvalsh(data)
    if np.any(eigenvalues < -1e-8):
        errors.append(f"{dataName} 不是正半定的。")
    return " ".join(errors)


@dataclass
class ScalarFunctionQuadraticApproximation:
    """标量函数的二次近似
    f(x,u) = 1/2 dx' dfdxx dx + du' dfdux dx + 1/2 du' dfduu du + dfdx' dx +
             dfdu' du + f
    """
    dfdxx: Optional[matrix_t] = field(default=None)
    dfdux: Optional[matrix_t] = field(default=None)
    dfduu: Optional[matrix_t] = field(default=None)
    dfdx: Optional[vector_t] = field(default=None)
    dfdu: Optional[vector_t] = field(default=None)
    f: scalar_t = 0.0

    def __init__(self, nx: int, nu: int = -1):
        """
        构造函数并调整成员大小。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nx, nu)

    def __iadd__(self, rhs: 'ScalarFunctionQuadraticApproximation') -> 'ScalarFunctionQuadraticApproximation':
        """复合加法赋值运算符"""
        if self.dfdxx is not None and rhs.dfdxx is not None:
            self.dfdxx += rhs.dfdxx
        if self.dfdux is not None and rhs.dfdux is not None:
            self.dfdux += rhs.dfdux
        if self.dfduu is not None and rhs.dfduu is not None:
            self.dfduu += rhs.dfduu
        if self.dfdx is not None and rhs.dfdx is not None:
            self.dfdx += rhs.dfdx
        if self.dfdu is not None and rhs.dfdu is not None:
            self.dfdu += rhs.dfdu
        self.f += rhs.f
        return self

    def __imul__(self, scalar: scalar_t) -> 'ScalarFunctionQuadraticApproximation':
        """复合标量乘法赋值运算符"""
        if self.dfdxx is not None:
            self.dfdxx *= scalar
        if self.dfdux is not None:
            self.dfdux *= scalar
        if self.dfduu is not None:
            self.dfduu *= scalar
        if self.dfdx is not None:
            self.dfdx *= scalar
        if self.dfdu is not None:
            self.dfdu *= scalar
        self.f *= scalar
        return self

    def resize(self, nx: int, nu: int = -1) -> 'ScalarFunctionQuadraticApproximation':
        """
        调整成员大小。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.dfdxx = np.zeros((nx, nx))
        if nu != -1:
            self.dfdux = np.zeros((nu, nx))
            self.dfduu = np.zeros((nu, nu))
        else:
            self.dfdux = None
            self.dfduu = None
        self.dfdx = np.zeros(nx)
        self.dfdu = np.zeros(nu) if nu != -1 else None
        return self

    def set_zero(self, nx: int, nu: int = -1) -> 'ScalarFunctionQuadraticApproximation':
        """
        调整成员大小并将所有系数设为零。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nx, nu)
        self.f = 0.0
        self.dfdxx.fill(0.0)
        if self.dfdux is not None:
            self.dfdux.fill(0.0)
        if self.dfduu is not None:
            self.dfduu.fill(0.0)
        if self.dfdx is not None:
            self.dfdx.fill(0.0)
        if self.dfdu is not None:
            self.dfdu.fill(0.0)
        return self

    @classmethod
    def Zero(cls, nx: int, nu: int = -1) -> 'ScalarFunctionQuadraticApproximation':
        """
        工厂函数，创建一个零初始化的对象。
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        :return: 给定大小的零初始化对象。
        """
        obj = cls(nx, nu)
        obj.set_zero(nx, nu)
        return obj

    def __str__(self):
        return (f"ScalarFunctionQuadraticApproximation(dfdxx={self.dfdxx}, "
                f"dfdux={self.dfdux}, dfduu={self.dfduu}, "
                f"dfdx={self.dfdx}, dfdu={self.dfdu}, f={self.f})")


def checkSizeQuadratic(stateDim: int, inputDim: int,
                      data: ScalarFunctionQuadraticApproximation,
                      dataName: str) -> str:
    """
    检查给定二次近似的大小。
    :param stateDim: 状态数量
    :param inputDim: 输入数量
    :param data: 给定的二次近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    if data.dfdxx is None or data.dfdxx.shape != (stateDim, stateDim):
        errors.append(f"{dataName}.dfdxx 形状 {data.dfdxx.shape if data.dfdxx is not None else 'None'} 不等于 ({stateDim}, {stateDim})。")
    if inputDim != -1:
        if data.dfdux is None or data.dfdux.shape != (inputDim, stateDim):
            errors.append(f"{dataName}.dfdux 形状 {data.dfdux.shape if data.dfdux is not None else 'None'} 不等于 ({inputDim}, {stateDim})。")
        if data.dfduu is None or data.dfduu.shape != (inputDim, inputDim):
            errors.append(f"{dataName}.dfduu 形状 {data.dfduu.shape if data.dfduu is not None else 'None'} 不等于 ({inputDim}, {inputDim})。")
    if data.dfdx is None or data.dfdx.size != stateDim:
        errors.append(f"{dataName}.dfdx 大小 {data.dfdx.size if data.dfdx is not None else 'None'} 不等于 stateDim {stateDim}。")
    if inputDim != -1:
        if data.dfdu is None or data.dfdu.size != inputDim:
            errors.append(f"{dataName}.dfdu 大小 {data.dfdu.size if data.dfdu is not None else 'None'} 不等于 inputDim {inputDim}。")
    if errors:
        return " ".join(errors)
    return ""


def checkBeingPSDQuadratic(data: ScalarFunctionQuadraticApproximation, dataName: str) -> str:
    """
    检查给定的二次近似是否有效、自伴和正半定（PSD）。
    :param data: 给定的二次近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    if data.dfdxx is not None:
        if not np.allclose(data.dfdxx, data.dfdxx.T, atol=1e-8):
            errors.append(f"{dataName}.dfdxx 不是对称的。")
        eigenvalues = np.linalg.eigvalsh(data.dfdxx)
        if np.any(eigenvalues < -1e-8):
            errors.append(f"{dataName}.dfdxx 不是正半定的。")
    if data.dfduu is not None:
        if not np.allclose(data.dfduu, data.dfduu.T, atol=1e-8):
            errors.append(f"{dataName}.dfduu 不是对称的。")
        eigenvalues = np.linalg.eigvalsh(data.dfduu)
        if np.any(eigenvalues < -1e-8):
            errors.append(f"{dataName}.dfduu 不是正半定的。")
    return " ".join(errors)


@dataclass
class VectorFunctionLinearApproximation:
    """向量值函数的线性模型 f(x,u) = dfdx dx + dfdu du + f"""
    dfdx: Optional[matrix_t] = field(default=None)
    dfdu: Optional[matrix_t] = field(default=None)
    f: Optional[vector_t] = field(default=None)

    def __init__(self, nv: int, nx: int, nu: int = -1):
        """
        构造函数并调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nv, nx, nu)

    def resize(self, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionLinearApproximation':
        """
        调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.dfdx = np.zeros((nv, nx))
        self.dfdu = np.zeros((nv, nu)) if nu != -1 else None
        self.f = np.zeros(nv)
        return self

    def set_zero(self, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionLinearApproximation':
        """
        调整成员大小并将所有系数设为零。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nv, nx, nu)
        if self.dfdx is not None:
            self.dfdx.fill(0.0)
        if self.dfdu is not None:
            self.dfdu.fill(0.0)
        if self.f is not None:
            self.f.fill(0.0)
        return self

    @classmethod
    def Zero(cls, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionLinearApproximation':
        """
        工厂函数，创建一个零初始化的对象。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        :return: 给定大小的零初始化对象。
        """
        obj = cls(nv, nx, nu)
        obj.set_zero(nv, nx, nu)
        return obj

    def __str__(self):
        return f"VectorFunctionLinearApproximation(dfdx={self.dfdx}, dfdu={self.dfdu}, f={self.f})"


def checkSizeVectorFunction(vectorDim: int, stateDim: int, inputDim: int,
                           data: VectorFunctionLinearApproximation,
                           dataName: str) -> str:
    """
    检查给定向量函数线性近似的大小。
    :param vectorDim: 向量函数维度
    :param stateDim: 状态数量
    :param inputDim: 输入数量
    :param data: 给定的线性近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    if data.dfdx is None or data.dfdx.shape != (vectorDim, stateDim):
        errors.append(f"{dataName}.dfdx 形状 {data.dfdx.shape if data.dfdx is not None else 'None'} 不等于 ({vectorDim}, {stateDim})。")
    if inputDim != -1:
        if data.dfdu is None or data.dfdu.shape != (vectorDim, inputDim):
            errors.append(f"{dataName}.dfdu 形状 {data.dfdu.shape if data.dfdu is not None else 'None'} 不等于 ({vectorDim}, {inputDim})。")
    if data.f is None or data.f.size != vectorDim:
        errors.append(f"{dataName}.f 大小 {data.f.size if data.f is not None else 'None'} 不等于 vectorDim {vectorDim}。")
    if errors:
        return " ".join(errors)
    return ""


@dataclass
class VectorFunctionQuadraticApproximation:
    """向量值函数的二次近似
    f[i](x,u) = 1/2 dx' dfdxx[i] dx + du' dfdux[i] dx + 1/2 du' dfduu[i] du +
               dfdx[i,:] dx + dfdu[i,:] du + f[i]
    """
    dfdxx: Optional[matrix_array_t] = field(default=None)
    dfdux: Optional[matrix_array_t] = field(default=None)
    dfduu: Optional[matrix_array_t] = field(default=None)
    dfdx: Optional[matrix_t] = field(default=None)
    dfdu: Optional[matrix_t] = field(default=None)
    f: Optional[vector_t] = field(default=None)

    def __init__(self, nv: int, nx: int, nu: int = -1):
        """
        构造函数并调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nv, nx, nu)

    def __iadd__(self, rhs: 'VectorFunctionQuadraticApproximation') -> 'VectorFunctionQuadraticApproximation':
        """复合加法赋值运算符"""
        if self.dfdxx is not None and rhs.dfdxx is not None:
            self.dfdxx = [a + b for a, b in zip(self.dfdxx, rhs.dfdxx)]
        if self.dfdux is not None and rhs.dfdux is not None:
            self.dfdux = [a + b for a, b in zip(self.dfdux, rhs.dfdux)]
        if self.dfduu is not None and rhs.dfduu is not None:
            self.dfduu = [a + b for a, b in zip(self.dfduu, rhs.dfduu)]
        if self.dfdx is not None and rhs.dfdx is not None:
            self.dfdx += rhs.dfdx
        if self.dfdu is not None and rhs.dfdu is not None:
            self.dfdu += rhs.dfdu
        if self.f is not None and rhs.f is not None:
            self.f += rhs.f
        return self

    def __imul__(self, scalar: scalar_t) -> 'VectorFunctionQuadraticApproximation':
        """复合标量乘法赋值运算符"""
        if self.dfdxx is not None:
            self.dfdxx = [a * scalar for a in self.dfdxx]
        if self.dfdux is not None:
            self.dfdux = [a * scalar for a in self.dfdux]
        if self.dfduu is not None:
            self.dfduu = [a * scalar for a in self.dfduu]
        if self.dfdx is not None:
            self.dfdx *= scalar
        if self.dfdu is not None:
            self.dfdu *= scalar
        if self.f is not None:
            self.f *= scalar
        return self

    def resize(self, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionQuadraticApproximation':
        """
        调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.dfdxx = [np.zeros((nx, nx)) for _ in range(nv)]
        if nu != -1:
            self.dfdux = [np.zeros((nu, nx)) for _ in range(nv)]
            self.dfduu = [np.zeros((nu, nu)) for _ in range(nv)]
        else:
            self.dfdux = None
            self.dfduu = None
        self.dfdx = np.zeros((nv, nx))
        self.dfdu = np.zeros((nv, nu)) if nu != -1 else None
        self.f = np.zeros(nv)
        return self

    def set_zero(self, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionQuadraticApproximation':
        """
        调整成员大小并将所有系数设为零。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nv, nx, nu)
        for matrix in self.dfdxx:
            matrix.fill(0.0)
        if self.dfdux is not None:
            for matrix in self.dfdux:
                matrix.fill(0.0)
        if self.dfduu is not None:
            for matrix in self.dfduu:
                matrix.fill(0.0)
        if self.dfdx is not None:
            self.dfdx.fill(0.0)
        if self.dfdu is not None:
            self.dfdu.fill(0.0)
        if self.f is not None:
            self.f.fill(0.0)
        return self

    @classmethod
    def Zero(cls, nv: int, nx: int, nu: int = -1) -> 'VectorFunctionQuadraticApproximation':
        """
        工厂函数，创建一个零初始化的对象。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        :return: 给定大小的零初始化对象。
        """
        obj = cls(nv, nx, nu)
        obj.set_zero(nv, nx, nu)
        return obj

    def __str__(self):
        return (f"VectorFunctionQuadraticApproximation(dfdxx={self.dfdxx}, "
                f"dfdux={self.dfdux}, dfduu={self.dfduu}, "
                f"dfdx={self.dfdx}, dfdu={self.dfdu}, f={self.f})")


def checkSizeVectorFunctionQuadratic(vectorDim: int, stateDim: int, inputDim: int,
                                    data: VectorFunctionQuadraticApproximation,
                                    dataName: str) -> str:
    """
    检查给定向量函数二次近似的大小。
    :param vectorDim: 向量函数维度
    :param stateDim: 状态数量
    :param inputDim: 输入数量
    :param data: 给定的二次近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    if data.dfdxx is None or len(data.dfdxx) != vectorDim:
        errors.append(f"{dataName}.dfdxx 长度 {len(data.dfdxx) if data.dfdxx is not None else 'None'} 不等于 vectorDim {vectorDim}。")
    else:
        for i, mat in enumerate(data.dfdxx):
            if mat.shape != (stateDim, stateDim):
                errors.append(f"{dataName}.dfdxx[{i}] 形状 {mat.shape} 不等于 ({stateDim}, {stateDim})。")
    if inputDim != -1:
        if data.dfdux is None or len(data.dfdux) != vectorDim:
            errors.append(f"{dataName}.dfdux 长度 {len(data.dfdux) if data.dfdux is not None else 'None'} 不等于 vectorDim {vectorDim}。")
        else:
            for i, mat in enumerate(data.dfdux):
                if mat.shape != (inputDim, stateDim):
                    errors.append(f"{dataName}.dfdux[{i}] 形状 {mat.shape} 不等于 ({inputDim}, {stateDim})。")
        if data.dfduu is None or len(data.dfduu) != vectorDim:
            errors.append(f"{dataName}.dfduu 长度 {len(data.dfduu) if data.dfduu is not None else 'None'} 不等于 vectorDim {vectorDim}。")
        else:
            for i, mat in enumerate(data.dfduu):
                if mat.shape != (inputDim, inputDim):
                    errors.append(f"{dataName}.dfduu[{i}] 形状 {mat.shape} 不等于 ({inputDim}, {inputDim})。")
    if data.dfdx is None or data.dfdx.shape != (vectorDim, stateDim):
        errors.append(f"{dataName}.dfdx 形状 {data.dfdx.shape if data.dfdx is not None else 'None'} 不等于 ({vectorDim}, {stateDim})。")
    if inputDim != -1:
        if data.dfdu is None or data.dfdu.shape != (vectorDim, inputDim):
            errors.append(f"{dataName}.dfdu 形状 {data.dfdu.shape if data.dfdu is not None else 'None'} 不等于 ({vectorDim}, {inputDim})。")
    if data.f is None or data.f.size != vectorDim:
        errors.append(f"{dataName}.f 大小 {data.f.size if data.f is not None else 'None'} 不等于 vectorDim {vectorDim}。")
    if errors:
        return " ".join(errors)
    return ""


def checkBeingPSDVectorFunctionQuadratic(data: VectorFunctionQuadraticApproximation, dataName: str) -> str:
    """
    检查给定的向量函数二次近似是否有效、自伴和正半定（PSD）。
    :param data: 给定的向量函数二次近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    for i, mat in enumerate(data.dfdxx):
        if not np.allclose(mat, mat.T, atol=1e-8):
            errors.append(f"{dataName}.dfdxx[{i}] 不是对称的。")
        eigenvalues = np.linalg.eigvalsh(mat)
        if np.any(eigenvalues < -1e-8):
            errors.append(f"{dataName}.dfdxx[{i}] 不是正半定的。")
    if data.dfduu is not None:
        for i, mat in enumerate(data.dfduu):
            if not np.allclose(mat, mat.T, atol=1e-8):
                errors.append(f"{dataName}.dfduu[{i}] 不是对称的。")
            eigenvalues = np.linalg.eigvalsh(mat)
            if np.any(eigenvalues < -1e-8):
                errors.append(f"{dataName}.dfduu[{i}] 不是正半定的。")
    return " ".join(errors)


@dataclass
class InequalityConstraintsLinearApproximation:
    """不等式约束的线性近似"""
    approx: VectorFunctionLinearApproximation = field(default_factory=VectorFunctionLinearApproximation)
    lb: Optional[vector_t] = field(default=None)
    ub: Optional[vector_t] = field(default=None)

    def __init__(self, nv: int, nx: int, nu: int = -1):
        """
        构造函数并调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.approx = VectorFunctionLinearApproximation(nv, nx, nu)
        self.lb = np.zeros(nv)
        self.ub = np.zeros(nv)

    def resize(self, nv: int, nx: int, nu: int = -1) -> 'InequalityConstraintsLinearApproximation':
        """
        调整成员大小。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.approx.resize(nv, nx, nu)
        self.lb = np.zeros(nv)
        self.ub = np.zeros(nv)
        return self

    def set_zero(self, nv: int, nx: int, nu: int = -1) -> 'InequalityConstraintsLinearApproximation':
        """
        调整成员大小并将所有系数设为零。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        """
        self.resize(nv, nx, nu)
        self.approx.set_zero(nv, nx, nu)
        if self.lb is not None:
            self.lb.fill(0.0)
        if self.ub is not None:
            self.ub.fill(0.0)
        return self

    @classmethod
    def Zero(cls, nv: int, nx: int, nu: int = -1) -> 'InequalityConstraintsLinearApproximation':
        """
        工厂函数，创建一个零初始化的对象。
        :param nv: 向量维度
        :param nx: 状态维度
        :param nu: 输入维度（传递 nu = -1 表示无输入）
        :return: 给定大小的零初始化对象。
        """
        obj = cls(nv, nx, nu)
        obj.set_zero(nv, nx, nu)
        return obj

    def __str__(self):
        return f"InequalityConstraintsLinearApproximation(approx={self.approx}, lb={self.lb}, ub={self.ub})"


def checkSizeInequalityConstraintsLinear(nv: int, nx: int, inputDim: int,
                                        data: InequalityConstraintsLinearApproximation,
                                        dataName: str) -> str:
    """
    检查给定不等式约束线性近似的大小。
    :param nv: 向量维度
    :param nx: 状态维度
    :param inputDim: 输入数量
    :param data: 给定的不等式约束线性近似
    :param dataName: 数据名称，用于错误消息中
    :return: 错误描述。如果没有错误，返回空字符串
    """
    errors = []
    size_errors = checkSizeVectorFunction(nv, nx, inputDim, data.approx, f"{dataName}.approx")
    if size_errors:
        errors.append(size_errors)
    if data.lb is None or data.lb.size != nv:
        errors.append(f"{dataName}.lb 大小 {data.lb.size if data.lb is not None else 'None'} 不等于 nv {nv}。")
    if data.ub is None or data.ub.size != nv:
        errors.append(f"{dataName}.ub 大小 {data.ub.size if data.ub is not None else 'None'} 不等于 nv {nv}。")
    if errors:
        return " ".join(errors)
    return ""
