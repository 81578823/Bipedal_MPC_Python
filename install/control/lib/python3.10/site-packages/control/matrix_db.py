# matrix_db.py

import numpy as np
from typing import Dict, Tuple


class MatrixDB:
    """
    MatrixDB 类用于存储和操作矩阵和向量数据。
    它支持矩阵和向量的加法、标量乘法以及矩阵乘法。
    """

    def __init__(self, 
                 A: np.ndarray = None, 
                 b: np.ndarray = None, 
                 C: np.ndarray = None, 
                 lb: np.ndarray = None, 
                 ub: np.ndarray = None, 
                 name: str = "default"):
        """
        初始化 MatrixDB 对象。

        Args:
            A (np.ndarray, optional): 矩阵 A。默认为 None。
            b (np.ndarray, optional): 向量 b。默认为 None。
            C (np.ndarray, optional): 矩阵 C。默认为 None。
            lb (np.ndarray, optional): 向量 lb。默认为 None。
            ub (np.ndarray, optional): 向量 ub。默认为 None。
            name (str, optional): 名称。默认为 "default"。
        """
        self.A = A if A is not None else np.empty((0, 0))
        self.C = C if C is not None else np.empty((0, 0))
        self.b = b if b is not None else np.empty((0,))
        self.lb = lb if lb is not None else np.empty((0,))
        self.ub = ub if ub is not None else np.empty((0,))
        self._name = name

    def __add__(self, other: "MatrixDB") -> "MatrixDB":
        """
        重载加法运算符，用于将两个 MatrixDB 对象的矩阵和向量进行拼接。

        Args:
            other (MatrixDB): 另一个 MatrixDB 对象。

        Returns:
            MatrixDB: 拼接后的 MatrixDB 对象。

        Raises:
            ValueError: 如果矩阵 A 或 C 的列数不匹配。
        """
        if not isinstance(other, MatrixDB):
            raise TypeError("Unsupported operand type(s) for +: 'MatrixDB' and '{}'".format(type(other).__name__))

        A_concat = self.concatenate_matrices(self.A, other.A)
        b_concat = self.concatenate_vectors(self.b, other.b)
        C_concat = self.concatenate_matrices(self.C, other.C)
        lb_concat = self.concatenate_vectors(self.lb, other.lb)
        ub_concat = self.concatenate_vectors(self.ub, other.ub)
        name_concat = self._name + other._name

        return MatrixDB(A_concat, b_concat, C_concat, lb_concat, ub_concat, name_concat)

    def __mul__(self, other) -> 'MatrixDB':
        """
        重载乘法运算符，用于标量乘法或矩阵乘法。

        Args:
            other (float or np.ndarray): 标量或矩阵。

        Returns:
            MatrixDB: 乘法后的 MatrixDB 对象。

        Raises:
            ValueError: 如果矩阵乘法的维度不匹配。
            TypeError: 如果操作数类型不支持。
        """
        if isinstance(other, (int, float)):
            # 标量乘法
            A_new = other * self.A if self.A.size > 0 else self.A
            b_new = other * self.b if self.b.size > 0 else self.b
            C_new = other * self.C if self.C.size > 0 else self.C
            lb_new = other * self.lb if self.lb.size > 0 else self.lb
            ub_new = other * self.ub if self.ub.size > 0 else self.ub
            return MatrixDB(A_new, b_new, C_new, lb_new, ub_new, self._name)
        elif isinstance(other, np.ndarray):
            # 矩阵乘法
            if self.A.size > 0 and other.shape[1] != self.A.shape[1]:
                raise ValueError(f"{self._name}_MatrixDB: Matrix multiplication dimension mismatch.")
            A_new = other @ self.A if self.A.size > 0 else self.A
            b_new = other @ self.b if self.b.size > 0 else self.b
            # C, lb, ub 不变
            return MatrixDB(A_new, b_new, self.C, self.lb, self.ub, self._name)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'MatrixDB' and '{type(other).__name__}'")

    def concatenate_matrices(self, m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
        """
        纵向拼接两个矩阵。

        Args:
            m1 (np.ndarray): 第一个矩阵。
            m2 (np.ndarray): 第二个矩阵。

        Returns:
            np.ndarray: 拼接后的矩阵。

        Raises:
            ValueError: 如果两个矩阵的列数不匹配。
        """
        if len(m1) == 0:
            return m2.copy()
        if len(m2) == 0:
            return m1.copy()
        if m1.shape[1] != m2.shape[1]:
            raise ValueError(f"{self._name}_MatrixDB: concatenateMatrices --> m1.cols() != m2.cols()")
        return np.vstack((m1, m2))

    def concatenate_vectors(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """
        纵向拼接两个向量。

        Args:
            v1 (np.ndarray): 第一个向量。
            v2 (np.ndarray): 第二个向量。

        Returns:
            np.ndarray: 拼接后的向量。
        """
        if v1.size == 0:
            return v2.copy()
        if v2.size == 0:
            return v1.copy()
        return np.concatenate((v1, v2))

    def name(self) -> str:
        """
        获取 MatrixDB 对象的名称。

        Returns:
            str: 名称。
        """
        return self._name

    def __repr__(self) -> str:
        """
        返回 MatrixDB 对象的字符串表示。

        Returns:
            str: 字符串表示。
        """
        return (f"MatrixDB(name='{self._name}',\n"
                f"        A=\n{self.A},\n"
                f"        b={self.b},\n"
                f"        C=\n{self.C},\n"
                f"        lb={self.lb},\n"
                f"        ub={self.ub})")

