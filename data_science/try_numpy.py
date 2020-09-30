import numpy as np
from scipy import linalg

m = np.array([[2, 4, 0, 4, 1], [2, 4, 1, 1, 0], [1, 1, 1, 2, 2], [0, 1, 3, 2, 4], [2, 2, 2, 0, 2]])
m = linalg.inv(m)
m = m.diagonal()
print(m.sum())