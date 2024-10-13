'''
#1
import numpy as np
import math

def DCT_process(matrix, i, j):  # DCT公式
    height, width = matrix.shape
    value = 0.0
    for col in range(height):
        for row in range(width):
            value += (matrix[col, row] *
                      math.cos(math.pi * (2 * col + 1) * i / (2. * height)) *
                      math.cos(math.pi * (2 * row + 1) * j / (2. * width)))

    c = 1.0
    if i == 0:
        c /= np.sqrt(2)
    if j == 0:
        c /= np.sqrt(2)

    return (2.0 / np.sqrt(height * width)) * c * value

def DCT(matrix):  # 主要被呼叫的DCT函式
    height, width = matrix.shape
    dct = np.zeros_like(matrix, dtype=float)

    for i in range(height):
        for j in range(width):
            dct[i, j] = DCT_process(matrix, i, j)

    return dct

def IDCT_process(dct, i, j):  # 逆DCT公式
    height, width = dct.shape
    value = 0.0

    for col in range(height):
        for row in range(width):
            c = 1.0
            if col == 0:
                c /= np.sqrt(2)
            if row == 0:
                c /= np.sqrt(2)
            value += (c * dct[col, row] *
                      math.cos(math.pi * (2 * i + 1) * col / (2. * height)) *
                      math.cos(math.pi * (2 * j + 1) * row / (2. * width)))

    return (2.0 / np.sqrt(height * width)) * value

def IDCT(dct):  # 逆DCT函式
    height, width = dct.shape
    matrix = np.zeros_like(dct, dtype=float)

    for i in range(height):
        for j in range(width):
            matrix[i, j] = IDCT_process(dct, i, j)

    return matrix
'''

'''
#確認答案的部分
from scipy.fftpack import dct, idct

def DCT(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def IDCT(dct_matrix):
    return idct(idct(dct_matrix.T, norm='ortho').T, norm='ortho')
'''

import numpy as np
import math

def dct_1d(vector):
    N = len(vector)
    result = np.zeros_like(vector, dtype=float)
    factor = math.pi / (2 * N)

    for k in range(N):
        if k == 0:
            c_k = 1 / math.sqrt(2)
        else:
            c_k = 1

        sum_value = 0
        for n in range(N):
            sum_value += vector[n] * math.cos((2 * n + 1) * k * factor)

        result[k] = c_k * sum_value * math.sqrt(2 / N)

    return result

def DCT(matrix):
    height, width = matrix.shape
    # Step 1: Apply DCT to each row
    temp = np.zeros_like(matrix, dtype=float)
    for i in range(height):
        temp[i, :] = dct_1d(matrix[i, :])
    
    # Step 2: Apply DCT to each column
    result = np.zeros_like(matrix, dtype=float)
    for j in range(width):
        result[:, j] = dct_1d(temp[:, j])
    
    return result

def idct_1d(vector):
    N = len(vector)
    result = np.zeros_like(vector, dtype=float)
    factor = math.pi / (2 * N)

    for n in range(N):
        sum_value = 0
        for k in range(N):
            if k == 0:
                c_k = 1 / math.sqrt(2)
            else:
                c_k = 1

            sum_value += c_k * vector[k] * math.cos((2 * n + 1) * k * factor)

        result[n] = sum_value * math.sqrt(2 / N)

    return result

def idct_2d(matrix):
    height, width = matrix.shape
    # Step 1: Apply IDCT to each column
    temp = np.zeros_like(matrix, dtype=float)
    for j in range(width):
        temp[:, j] = idct_1d(matrix[:, j])
    
    # Step 2: Apply IDCT to each row
    result = np.zeros_like(matrix, dtype=float)
    for i in range(height):
        result[i, :] = idct_1d(temp[i, :])
    
    return result

