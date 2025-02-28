import numpy as np

A_block = np.concatenate([[5*k] for k in range(10)])

print(A_block.transpose())