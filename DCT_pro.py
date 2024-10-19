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
import numpy as np

def DCT(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def IDCT(dct_matrix):
    return idct(idct(dct_matrix.T, norm='ortho').T, norm='ortho')
'''

import numpy as np

# 一維 DCT
def fdct_1d_8x8(src):
    v_0 = -0.785695
    v_1 =  0.275899
    v_2 =  0.461940
    v_3 =  0.785695
    v_4 =  0.191342
    v_5 =  0.707107
    v_6 =  1.175876
    v_7 =  0.353553
    v_8 =  1.387040
    
    out = np.zeros_like(src, dtype=float)

    for i in range(8):
        s_0 = src[i, 0]
        s_1 = src[i, 1]
        s_2 = src[i, 2]
        s_3 = src[i, 3]
        s_4 = src[i, 4]
        s_5 = src[i, 5]
        s_6 = src[i, 6]
        s_7 = src[i, 7]

        x_00 = s_0 + s_7
        x_01 = s_1 + s_6
        x_02 = s_2 + s_5
        x_03 = s_3 + s_4
        x_04 = s_0 - s_7
        x_05 = s_1 - s_6
        x_06 = s_2 - s_5
        x_07 = s_3 - s_4
        x_08 = x_00 + x_03
        x_09 = x_01 + x_02
        x_0A = x_00 - x_03
        x_0B = x_01 - x_02
        x_0C = v_8 * x_04 + v_1 * x_07
        x_0D = v_6 * x_05 + v_3 * x_06
        x_0E = v_0 * x_05 + v_6 * x_06
        x_0F = v_1 * x_04 - v_8 * x_07
        x_10 = v_7 * (x_0C - x_0D)
        x_11 = v_7 * (x_0E - x_0F)

        out[i, 0] = v_7 * (x_08 + x_09)
        out[i, 1] = v_7 * (x_0C + x_0D)
        out[i, 2] = v_2 * x_0A + v_4 * x_0B
        out[i, 3] = v_5 * (x_10 - x_11)
        out[i, 4] = v_7 * (x_08 - x_09)
        out[i, 5] = v_5 * (x_10 + x_11)
        out[i, 6] = v_4 * x_0A - v_2 * x_0B
        out[i, 7] = v_7 * (x_0E + x_0F)

    return out

# 二維 DCT
def DCT(src):
    tmp = fdct_1d_8x8(src)       # 一維DCT
    out = fdct_1d_8x8(tmp.T)     # 轉置後再做一次一維DCT
    return out.T

'''
# 測試輸出
src = np.random.randint(-128, 127, (8, 8))  # 隨機生成一個 8x8 矩陣作為測試
dct_result = fdct_8x8(src)



a = DCT(src)
b = IDCT(a)

print(src)
print("\nDCT:")
print(dct_result)

print("\n T DCT:")
print(a)
print("\n T IDCT:")
print(b)
'''