# linear_algebra.py

import numpy as np
from scipy import sparse
from scipy.linalg import eigh, cholesky, qr, lu, LinAlgError
from typing import Tuple
from dataclasses import dataclass

from numeric_traits import limit_epsilon, weak_epsilon
from numerics import almost_eq
from lookup import find_first_index_within_tol, find_index_in_time_array
from typing import TypeVar

# 类型别名
matrix_t = np.ndarray
vector_t = np.ndarray

@dataclass
class VectorFunctionLinearApproximation:
    dfdx: matrix_t
    dfdu: matrix_t
    f: vector_t

def set_triangular_minimum_eigenvalues(Lr: matrix_t, min_eigen_value: float = weak_epsilon()) -> None:
    """
    将三角矩阵的特征值设置为最小幅度（保持符号）。
    
    Args:
        Lr (np.ndarray): 三角矩阵，需为下三角或上三角。
        min_eigen_value (float, optional): 最小特征值。默认为 weak_epsilon()。
    """
    for i in range(Lr.shape[0]):
        eigen_value = Lr[i, i]
        if eigen_value < 0.0:
            Lr[i, i] = min(-min_eigen_value, eigen_value)
        else:
            Lr[i, i] = max(min_eigen_value, eigen_value)

def make_psd_eigenvalue(square_matrix: matrix_t, min_eigenvalue: float = limit_epsilon()) -> None:
    """
    使用特征值分解将输入矩阵转换为正半定矩阵（PSD）。
    
    Args:
        square_matrix (np.ndarray): 要转换为 PSD 的方阵。
        min_eigenvalue (float, optional): 最小特征值。默认为 limit_epsilon()。
    
    Raises:
        ValueError: 如果输入矩阵不是方阵。
    """
    if square_matrix.shape[0] != square_matrix.shape[1]:
        raise ValueError("输入矩阵必须是方阵。")
    
    # 确保矩阵是对称的
    square_matrix = 0.5 * (square_matrix + square_matrix.T)
    
    # 计算特征值和特征向量
    eigenvalues, eigenvectors = eigh(square_matrix)
    
    # 检查是否有特征值小于最小特征值
    has_negative_eigenvalue = False
    eigenvalues_modified = eigenvalues.copy()
    for j in range(len(eigenvalues)):
        if eigenvalues[j] < min_eigenvalue:
            has_negative_eigenvalue = True
            eigenvalues_modified[j] = min_eigenvalue
    
    if has_negative_eigenvalue:
        # 重构矩阵
        square_matrix[:] = eigenvectors @ np.diag(eigenvalues_modified) @ np.linalg.inv(eigenvectors)
    else:
        # 确保矩阵是对称的
        square_matrix[:] = 0.5 * (square_matrix + square_matrix.T)

def make_psd_gershgorin(square_matrix: matrix_t, min_eigenvalue: float = limit_epsilon()) -> None:
    """
    基于 Gershgorin 圆定理将输入矩阵转换为正半定矩阵（PSD）。
    
    Args:
        square_matrix (np.ndarray): 要转换为 PSD 的方阵。
        min_eigenvalue (float, optional): 最小特征值。默认为 limit_epsilon()。
    
    Raises:
        ValueError: 如果输入矩阵不是方阵。
    """
    if square_matrix.shape[0] != square_matrix.shape[1]:
        raise ValueError("输入矩阵必须是方阵。")
    
    # 确保矩阵是对称的
    square_matrix = 0.5 * (square_matrix + square_matrix.T)
    
    for i in range(square_matrix.shape[0]):
        # Gershgorin 半径：由于矩阵是对称的，我们使用列和
        Ri = np.sum(np.abs(square_matrix[:, i])) - np.abs(square_matrix[i, i])
        square_matrix[i, i] = max(square_matrix[i, i], Ri + min_eigenvalue)

def make_psd_cholesky(A: matrix_t, min_eigenvalue: float = limit_epsilon()) -> None:
    """
    基于修改的 Cholesky 分解将输入矩阵转换为正半定矩阵（PSD）。
    
    Args:
        A (np.ndarray): 要转换为 PSD 的方阵。
        min_eigenvalue (float, optional): 最小特征值。默认为 limit_epsilon()。
    
    Raises:
        ValueError: 如果输入矩阵不是方阵或 Cholesky 分解失败。
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("输入矩阵必须是方阵。")
    
    try:
        # 确保矩阵是对称的
        A[:] = 0.5 * (A + A.T)
        
        # 尝试进行 Cholesky 分解
        chol = cholesky(A, lower=True)
        
    except LinAlgError:
        # 如果 Cholesky 分解失败，则调整对角线元素
        for i in range(A.shape[0]):
            A[i, i] += min_eigenvalue
        try:
            chol = cholesky(A, lower=True)
        except LinAlgError as e:
            raise ValueError("无法将矩阵转换为正半定矩阵。") from e

def compute_inverse_matrix_uut(Am: np.ndarray, AmInvUmUmT: np.ndarray):
    """
    计算 inv(U)，其中 Am = L * L.T，U = L.T。
    
    Args:
        Am (np.ndarray): 输入矩阵，假设为对称正定矩阵。
        AmInvUmUmT (np.ndarray): 输出矩阵，用于存储 inv(U)。必须与 Am 形状相同。
    
    Returns:
        None: 结果直接存储在 AmInvUmUmT 中。
    """
    # 检查输入矩阵是否为方阵
    if Am.shape[0] != Am.shape[1]:
        raise ValueError("Input matrix Am must be square.")
    
    # 检查输出矩阵形状是否匹配
    if AmInvUmUmT.shape != Am.shape:
        raise ValueError("Output matrix AmInvUmUmT must have the same shape as Am.")
    
    # 执行 Cholesky 分解，Am = L * L.T
    try:
        L = np.linalg.cholesky(Am)  # L 是下三角矩阵
    except np.linalg.LinAlgError as e:
        raise ValueError("Cholesky decomposition failed. Ensure that Am is symmetric positive definite.") from e
    
    # U = L.T，是上三角矩阵
    U = L.T
    
    # 创建单位矩阵
    identity = np.eye(U.shape[0], U.shape[1])
    
    # 解方程 U * X = I，得到 X = inv(U)
    # 使用 np.linalg.solve 而不是显式求逆，数值更稳定
    AmInvUmUmT[:] = np.linalg.solve(U, identity)

def compute_constraint_projection(Dm: matrix_t, Rm_inv_Um_UmT: matrix_t) -> Tuple[matrix_t, matrix_t, matrix_t, matrix_t]:
    """
    计算线性约束 C*x + D*u - e = 0 的约束投影，带权重 inv(Rm)。
    
    Args:
        Dm (np.ndarray): 全秩约束矩阵。
        Rm_inv_Um_UmT (np.ndarray): 与 inv(Rm) 矩阵的 UUT 分解相关的上三角矩阵。
    
    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
            DmDagger, 
            DmDaggerTRmDmDaggerUUT, 
            RmInvConstrainedUUT
    """
    num_constraints, num_inputs = Dm.shape
    
    # 计算 QR 分解
    RmDT = Rm_inv_Um_UmT.T @ Dm.T
    Q, R = np.linalg.qr(RmDT, mode='reduced')
    
    # 设置 R 的对角线元素为最小特征值
    set_triangular_minimum_eigenvalues(R)
    
    # 计算 DmDaggerTRmDmDaggerUUT
    DmDaggerTRmDmDaggerUUT = np.linalg.inv(R)
    
    # 计算 Q 的左和右部分
    Qc = Q[:, :num_constraints]
    Qu = Q[:, num_constraints:]
    
    # 计算 DmDagger
    DmDagger = Rm_inv_Um_UmT @ (Qc @ DmDaggerTRmDmDaggerUUT.T)
    
    # 计算 RmInvConstrainedUUT
    RmInvConstrainedUUT = Rm_inv_Um_UmT @ Qu
    
    return DmDagger, DmDaggerTRmDmDaggerUUT, RmInvConstrainedUUT

def qr_constraint_projection(constraint: VectorFunctionLinearApproximation) -> Tuple[VectorFunctionLinearApproximation, matrix_t]:
    """
    计算基于 QR 分解的线性约束投影。
    
    Args:
        constraint (VectorFunctionLinearApproximation): 约束条件，包含 dfdx, dfdu 和 f。
    
    Returns:
        Tuple[VectorFunctionLinearApproximation, np.ndarray]: 
            Projection terms (dfdx, dfdu, f),
            Pseudo-inverse matrix.
    """
    Dfdu = constraint.dfdu
    dfdx = constraint.dfdx
    f = constraint.f
    num_constraints, num_inputs = Dfdu.shape
    
    # QR 分解
    Q, R = np.linalg.qr(Dfdu.T, mode='reduced')
    
    # 计算 pseudo-inverse
    try:
        pseudo_inverse = np.linalg.solve(R, Q.T[:num_constraints])
    except LinAlgError as e:
        raise ValueError("无法计算 QR 分解的解。") from e
    
    # 计算投影项
    Pu = Q[:, num_constraints:]
    Px = -pseudo_inverse.T @ dfdx
    Pe = -pseudo_inverse.T @ f
    
    projection_terms = VectorFunctionLinearApproximation(dfdx=Px, dfdu=Pu, f=Pe)
    
    return projection_terms, pseudo_inverse

def lu_constraint_projection(constraint: VectorFunctionLinearApproximation, extract_pseudo_inverse: bool = False) -> Tuple[VectorFunctionLinearApproximation, matrix_t]:
    """
    计算基于 LU 分解的线性约束投影。
    
    Args:
        constraint (VectorFunctionLinearApproximation): 约束条件，包含 dfdx, dfdu 和 f。
        extract_pseudo_inverse (bool, optional): 如果为 True，则返回 DmDagger^T 的左伪逆。默认为 False。
    
    Returns:
        Tuple[VectorFunctionLinearApproximation, np.ndarray]: 
            Projection terms (dfdx, dfdu, f),
            Pseudo-inverse matrix（如果 extract_pseudo_inverse 为 True，否则返回空矩阵）。
    """
    Dfdu = constraint.dfdu
    dfdx = constraint.dfdx
    f = constraint.f
    num_constraints, num_inputs = Dfdu.shape
    
    try:
        # LU 分解
        P, L, U = lu(Dfdu)
        
        # 解方程
        DmDagger = np.linalg.solve(U, L)
        Px = -DmDagger.T @ dfdx
        Pe = -DmDagger.T @ f
        
        projection_terms = VectorFunctionLinearApproximation(dfdx=Px, dfdu=DmDagger.T, f=Pe)
        
        if extract_pseudo_inverse:
            # 计算左伪逆
            pseudo_inverse = np.linalg.solve(U, L).T
        else:
            pseudo_inverse = np.zeros((0, 0))
        
        return projection_terms, pseudo_inverse
    except LinAlgError as e:
        raise ValueError("LU 分解失败。") from e

def rank(A: matrix_t) -> int:
    """
    计算矩阵的秩。
    
    Args:
        A (np.ndarray): 输入矩阵。
    
    Returns:
        int: 矩阵的秩。
    """
    return np.linalg.matrix_rank(A)

def eigenvalues_func(A: matrix_t) -> np.ndarray:
    """
    计算矩阵的特征值。
    
    Args:
        A (np.ndarray): 输入矩阵。
    
    Returns:
        np.ndarray: 特征值。
    """
    return np.linalg.eigvals(A)

def symmetric_eigenvalues(A: matrix_t) -> np.ndarray:
    """
    计算对称矩阵的特征值。
    
    Args:
        A (np.ndarray): 输入的对称矩阵。
    
    Returns:
        np.ndarray: 特征值。
    """
    if not np.allclose(A, A.T, atol=1e-8):
        raise ValueError("输入矩阵必须是对称的。")
    return eigh(A, eigvals_only=True)

# 示例用法（可选）
if __name__ == "__main__":
    # 测试 set_triangular_minimum_eigenvalues
    Lr = np.array([[0.5, 0.0], [0.0, -0.3]])
    print("Before set_triangular_minimum_eigenvalues:")
    print(Lr)
    set_triangular_minimum_eigenvalues(Lr, min_eigen_value=1e-6)
    print("After set_triangular_minimum_eigenvalues:")
    print(Lr)
    
    # 测试 make_psd_eigenvalue
    A = np.array([[2.0, -1.0], [-1.0, 2.0]])
    print("\nBefore make_psd_eigenvalue:")
    print(A)
    make_psd_eigenvalue(A, min_eigenvalue=1e-6)
    print("After make_psd_eigenvalue:")
    print(A)
    
    # 测试 make_psd_gershgorin
    B = np.array([[1.0, 2.0], [2.0, 1.0]])
    print("\nBefore make_psd_gershgorin:")
    print(B)
    make_psd_gershgorin(B, min_eigenvalue=1e-6)
    print("After make_psd_gershgorin:")
    print(B)
    
    # 测试 make_psd_cholesky
    C = np.array([[4.0, 2.0], [2.0, 3.0]])
    print("\nBefore make_psd_cholesky:")
    print(C)
    make_psd_cholesky(C, min_eigenvalue=1e-6)
    print("After make_psd_cholesky:")
    print(C)
    
    # 测试 compute_inverse_matrix_uut
    Am = np.array([[4.0, 2.0], [2.0, 3.0]])
    print("\nAm:")
    print(Am)
    AmInvUmUmT=np.identity(Am.shape[0])
    compute_inverse_matrix_uut(Am,AmInvUmUmT)
    print("AmInvUmUmT (U):")
    print(AmInvUmUmT)
    
    # 测试 compute_constraint_projection
    Dm = np.array([[1.0, 2.0], [3.0, 4.0]])
    Rm_inv_Um_UmT = np.array([[1.0, 0.0], [0.0, 1.0]])
    DmDagger, DmDaggerTRmDmDaggerUUT, RmInvConstrainedUUT = compute_constraint_projection(Dm, Rm_inv_Um_UmT)
    print("\nDmDagger:")
    print(DmDagger)
    print("DmDaggerTRmDmDaggerUUT:")
    print(DmDaggerTRmDmDaggerUUT)
    print("RmInvConstrainedUUT:")
    print(RmInvConstrainedUUT)
    
    # 测试 qr_constraint_projection
    constraint = VectorFunctionLinearApproximation(
        dfdx=np.array([[1.0, 0.0], [0.0, 1.0]]),
        dfdu=np.array([[1.0, 2.0], [3.0, 4.0]]),
        f=np.array([1.0, 1.0])
    )
    projection_terms, pseudo_inverse = qr_constraint_projection(constraint)
    print("\nQR Constraint Projection Terms:")
    print("Px:")
    print(projection_terms.dfdx)
    print("Pu:")
    print(projection_terms.dfdu)
    print("Pe:")
    print(projection_terms.f)
    print("Pseudo-inverse:")
    print(pseudo_inverse)
    
    # 测试 lu_constraint_projection
    projection_terms_lu, pseudo_inverse_lu = lu_constraint_projection(constraint, extract_pseudo_inverse=True)
    print("\nLU Constraint Projection Terms:")
    print("Px:")
    print(projection_terms_lu.dfdx)
    print("Pu:")
    print(projection_terms_lu.dfdu)
    print("Pe:")
    print(projection_terms_lu.f)
    print("Pseudo-inverse LU:")
    print(pseudo_inverse_lu)
    
    # 测试 rank
    print("\nRank of Dm:", rank(Dm))
    
    # 测试 eigenvalues_func
    print("Eigenvalues of Am:", eigenvalues_func(Am))
    
    # 测试 symmetric_eigenvalues
    sym_A = np.array([[2.0, 1.0], [1.0, 2.0]])
    print("Symmetric Eigenvalues of sym_A:", symmetric_eigenvalues(sym_A))
