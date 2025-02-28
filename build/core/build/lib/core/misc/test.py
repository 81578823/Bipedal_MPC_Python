import numpy as np

# 假设 Q 是一个 NumPy 二维数组
Q = np.array([
    [1, 2, 3, 4, 5, 6],
    [7, 8, 9, 10, 11, 12],
    [13, 14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24]
], dtype=float)

numConstraints = 4
numInputs = 6

# 方法1: 使用负索引提取最后 (numInputs - numConstraints) 列
Qu1 = Q[:, -(numInputs - numConstraints):]

# 方法2: 计算起始列索引并切片
start_col = numConstraints
Qu2 = Q[:, start_col:]

print("Qu1:")
print(Qu1)

print("\nQu2:")
print(Qu2)
