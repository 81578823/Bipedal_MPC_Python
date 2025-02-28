# core/types.py

import numpy as np
from typing import List
from dataclasses import dataclass, field
import scipy.linalg

# 类型别名
scalar_t = float
vector_t = np.ndarray  # 一维数组
vector3_t = np.ndarray  # 长度为3的一维数组
vector6_t = np.ndarray  # 长度为6的一维数组
vector12_t = np.ndarray  # 长度为12的一维数组
matrix_t = np.ndarray  # 二维数组
matrix3x_t = np.ndarray  # 3xN矩阵
matrix6x_t = np.ndarray  # 6xN矩阵
matrix3x3_t = np.ndarray  # 3x3矩阵
matrix6x6_t = np.ndarray  # 6x6矩阵

@dataclass
class ScalarFunctionLinearApproximation:
    dfdx: vector_t = field(default_factory=lambda: np.array([]))
    dfdu: vector_t = field(default_factory=lambda: np.array([]))
    f: scalar_t = 0.0

    def __iadd__(self, other: 'ScalarFunctionLinearApproximation') -> 'ScalarFunctionLinearApproximation':
        self.f += other.f
        self.dfdx += other.dfdx
        self.dfdu += other.dfdu
        return self

    def __imul__(self, scalar: scalar_t) -> 'ScalarFunctionLinearApproximation':
        self.f *= scalar
        self.dfdx *= scalar
        self.dfdu *= scalar
        return self

    def resize(self, nx: int, nu: int = -1):
        self.dfdx = np.zeros(nx)
        if nu >= 0:
            self.dfdu = np.zeros(nu)
        else:
            self.dfdu = np.array([])

    def set_zero(self, nx: int, nu: int = -1):
        self.f = 0.0
        self.dfdx = np.zeros(nx)
        if nu >= 0:
            self.dfdu = np.zeros(nu)
        else:
            self.dfdu = np.array([])

    @staticmethod
    def zero(nx: int, nu: int = -1) -> 'ScalarFunctionLinearApproximation':
        instance = ScalarFunctionLinearApproximation()
        instance.set_zero(nx, nu)
        return instance

@dataclass
class ScalarFunctionQuadraticApproximation:
    dfdxx: matrix_t = field(default_factory=lambda: np.array([[]]))
    dfdux: matrix_t = field(default_factory=lambda: np.array([[]]))
    dfduu: matrix_t = field(default_factory=lambda: np.array([[]]))
    dfdx: vector_t = field(default_factory=lambda: np.array([]))
    dfdu: vector_t = field(default_factory=lambda: np.array([]))
    f: scalar_t = 0.0

    def __iadd__(self, other: 'ScalarFunctionQuadraticApproximation') -> 'ScalarFunctionQuadraticApproximation':
        self.f += other.f
        self.dfdx += other.dfdx
        self.dfdu += other.dfdu
        self.dfdxx += other.dfdxx
        self.dfdux += other.dfdux
        self.dfduu += other.dfduu
        return self

    def __imul__(self, scalar: scalar_t) -> 'ScalarFunctionQuadraticApproximation':
        self.f *= scalar
        self.dfdx *= scalar
        self.dfdu *= scalar
        self.dfdxx *= scalar
        self.dfdux *= scalar
        self.dfduu *= scalar
        return self

    def resize(self, nx: int, nu: int = -1):
        self.dfdx = np.zeros(nx)
        self.dfdxx = np.zeros((nx, nx))
        if nu >= 0:
            self.dfdu = np.zeros(nu)
            self.dfdux = np.zeros((nu, nx))
            self.dfduu = np.zeros((nu, nu))
        else:
            self.dfdu = np.array([])
            self.dfdux = np.array([[]])
            self.dfduu = np.array([[]])

    def set_zero(self, nx: int, nu: int = -1):
        self.f = 0.0
        self.dfdx = np.zeros(nx)
        self.dfdxx = np.zeros((nx, nx))
        if nu >= 0:
            self.dfdu = np.zeros(nu)
            self.dfdux = np.zeros((nu, nx))
            self.dfduu = np.zeros((nu, nu))
        else:
            self.dfdu = np.array([])
            self.dfdux = np.array([[]])
            self.dfduu = np.array([[]])

    @staticmethod
    def zero(nx: int, nu: int = -1) -> 'ScalarFunctionQuadraticApproximation':
        instance = ScalarFunctionQuadraticApproximation()
        instance.set_zero(nx, nu)
        return instance

@dataclass
class VectorFunctionLinearApproximation:
    dfdx: matrix_t = field(default_factory=lambda: np.array([[]]))
    dfdu: matrix_t = field(default_factory=lambda: np.array([[]]))
    f: vector_t = field(default_factory=lambda: np.array([]))

    def resize(self, nv: int, nx: int, nu: int = -1):
        self.f = np.zeros(nv)
        self.dfdx = np.zeros((nv, nx))
        if nu >= 0:
            self.dfdu = np.zeros((nv, nu))
        else:
            self.dfdu = np.array([[]])

    def set_zero(self, nv: int, nx: int, nu: int = -1):
        self.f = np.zeros(nv)
        self.dfdx = np.zeros((nv, nx))
        if nu >= 0:
            self.dfdu = np.zeros((nv, nu))
        else:
            self.dfdu = np.array([[]])

    @staticmethod
    def zero(nv: int, nx: int, nu: int = -1) -> 'VectorFunctionLinearApproximation':
        instance = VectorFunctionLinearApproximation()
        instance.set_zero(nv, nx, nu)
        return instance

@dataclass
class VectorFunctionQuadraticApproximation:
    dfdxx: List[matrix_t] = field(default_factory=lambda: [])
    dfdux: List[matrix_t] = field(default_factory=lambda: [])
    dfduu: List[matrix_t] = field(default_factory=lambda: [])
    dfdx: matrix_t = field(default_factory=lambda: np.array([[]]))
    dfdu: matrix_t = field(default_factory=lambda: np.array([[]]))
    f: vector_t = field(default_factory=lambda: np.array([]))

    def resize(self, nv: int, nx: int, nu: int = -1):
        self.f = np.zeros(nv)
        self.dfdx = np.zeros((nv, nx))
        self.dfdxx = [np.zeros((nx, nx)) for _ in range(nv)]
        if nu >= 0:
            self.dfdu = np.zeros((nv, nu))
            self.dfdux = [np.zeros((nu, nx)) for _ in range(nv)]
            self.dfduu = [np.zeros((nu, nu)) for _ in range(nv)]
        else:
            self.dfdu = np.array([[]])
            self.dfdux = [np.array([[]]) for _ in range(nv)]
            self.dfduu = [np.array([[]]) for _ in range(nv)]

    def set_zero(self, nv: int, nx: int, nu: int = -1):
        self.f = np.zeros(nv)
        self.dfdx = np.zeros((nv, nx))
        self.dfdxx = [np.zeros((nx, nx)) for _ in range(nv)]
        if nu >= 0:
            self.dfdu = np.zeros((nv, nu))
            self.dfdux = [np.zeros((nu, nx)) for _ in range(nv)]
            self.dfduu = [np.zeros((nu, nu)) for _ in range(nv)]
        else:
            self.dfdu = np.array([[]])
            self.dfdux = [np.array([[]]) for _ in range(nv)]
            self.dfduu = [np.array([[]]) for _ in range(nv)]

    @staticmethod
    def zero(nv: int, nx: int, nu: int = -1) -> 'VectorFunctionQuadraticApproximation':
        instance = VectorFunctionQuadraticApproximation()
        instance.set_zero(nv, nx, nu)
        return instance

@dataclass
class InequalityConstraintsLinearApproximation:
    approx: VectorFunctionLinearApproximation = field(default_factory=lambda: VectorFunctionLinearApproximation())
    lb: vector_t = field(default_factory=lambda: np.array([]))
    ub: vector_t = field(default_factory=lambda: np.array([]))

    def resize(self, nv: int, nx: int, nu: int = -1):
        self.approx.resize(nv, nx, nu)
        self.lb = np.zeros(nv)
        self.ub = np.zeros(nv)

    def set_zero(self, nv: int, nx: int, nu: int = -1):
        self.approx.set_zero(nv, nx, nu)
        self.lb = np.zeros(nv)
        self.ub = np.zeros(nv)

    @staticmethod
    def zero(nv: int, nx: int, nu: int = -1) -> 'InequalityConstraintsLinearApproximation':
        instance = InequalityConstraintsLinearApproximation()
        instance.set_zero(nv, nx, nu)
        return instance

# 检查函数

def check_size_scalar_function_linear(state_dim: int, input_dim: int,
                                      data: ScalarFunctionLinearApproximation,
                                      data_name: str) -> str:
    error_description = ""
    if data.dfdx.size != state_dim:
        error_description += f"{data_name}.dfdx.size != {state_dim}\n"
    if input_dim >= 0 and data.dfdu.size != input_dim:
        error_description += f"{data_name}.dfdu.size != {input_dim}\n"
    return error_description

def check_size_scalar_function_quadratic(state_dim: int, input_dim: int,
                                         data: ScalarFunctionQuadraticApproximation,
                                         data_name: str) -> str:
    error_description = ""
    if data.dfdx.size != state_dim:
        error_description += f"{data_name}.dfdx.size != {state_dim}\n"
    if data.dfdxx.shape != (state_dim, state_dim):
        error_description += f"{data_name}.dfdxx.shape != ({state_dim}, {state_dim})\n"
    if input_dim >= 0 and data.dfdu.size != input_dim:
        error_description += f"{data_name}.dfdu.size != {input_dim}\n"
    if input_dim >= 0 and data.dfduu.shape != (input_dim, input_dim):
        error_description += f"{data_name}.dfduu.shape != ({input_dim}, {input_dim})\n"
    if input_dim >= 0 and data.dfdux.shape != (input_dim, state_dim):
        error_description += f"{data_name}.dfdux.shape != ({input_dim}, {state_dim})\n"
    return error_description

def check_being_psd(matrix: matrix_t, data_name: str) -> str:
    error_description = ""
    if matrix.size == 0:
        return error_description  # 空矩阵不检查
    if not np.all(np.isfinite(matrix)):
        error_description += f"{data_name} is not finite.\n"
    if matrix.shape[0] != matrix.shape[1]:
        error_description += f"{data_name} is not a square matrix.\n"
    else:
        if not np.allclose(matrix, matrix.T, atol=1e-6):
            error_description += f"{data_name} is not self-adjoint.\n"
        eigenvalues = np.linalg.eigvalsh(matrix)
        min_eigenvalue = eigenvalues.min()
        if min_eigenvalue < -np.finfo(scalar_t).eps:
            error_description += f"{data_name} is not PSD. It's smallest eigenvalue is {min_eigenvalue}.\n"
    return error_description

def check_being_psd_quadratic(data: ScalarFunctionQuadraticApproximation, data_name: str) -> str:
    error_description = ""
    if not np.isfinite(data.f):
        error_description += f"{data_name}.f is not finite.\n"
    if data.dfdx.size > 0 and not np.all(np.isfinite(data.dfdx)):
        error_description += f"{data_name}.dfdx is not finite.\n"
    if data.dfdu.size > 0 and not np.all(np.isfinite(data.dfdu)):
        error_description += f"{data_name}.dfdu is not finite.\n"
    if data.dfdux.size > 0 and not np.all(np.isfinite(data.dfdux)):
        error_description += f"{data_name}.dfdux is not finite.\n"
    if data.dfdxx.size > 0:
        error_description += check_being_psd(data.dfdxx, f"{data_name}.dfdxx")
    if data.dfduu.size > 0:
        error_description += check_being_psd(data.dfduu, f"{data_name}.dfduu")
    return error_description

def check_size_vector_function_linear(vector_dim: int, state_dim: int, input_dim: int,
                                     data: VectorFunctionLinearApproximation,
                                     data_name: str) -> str:
    error_description = ""
    if data.f.size != vector_dim:
        error_description += f"{data_name}.f.size != {vector_dim}\n"
    if vector_dim > 0 and data.dfdx.shape != (vector_dim, state_dim):
        error_description += f"{data_name}.dfdx.shape != ({vector_dim}, {state_dim})\n"
    if vector_dim > 0 and input_dim > 0 and data.dfdu.shape != (vector_dim, input_dim):
        error_description += f"{data_name}.dfdu.shape != ({vector_dim}, {input_dim})\n"
    return error_description

# 您可以根据需要继续实现其他检查函数，如 `check_size_vector_function_quadratic` 等

