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

# FDCT 1D for 8x8 block
def fdct_1d_8x8(src, stridea, strideb):
    v_0 = -0.785695
    v_1 =  0.275899
    v_2 =  0.461940
    v_3 =  0.785695
    v_4 =  0.191342
    v_5 =  0.707107
    v_6 =  1.175876
    v_7 =  0.353553
    v_8 =  1.387040

    out = np.zeros_like(src)

    for i in range(8):
        s_0 = src[0 * stridea]
        s_1 = src[1 * stridea]
        s_2 = src[2 * stridea]
        s_3 = src[3 * stridea]
        s_4 = src[4 * stridea]
        s_5 = src[5 * stridea]
        s_6 = src[6 * stridea]
        s_7 = src[7 * stridea]

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

        out[0 * stridea] = v_7 * (x_08 + x_09)
        out[1 * stridea] = v_7 * (x_0C + x_0D)
        out[2 * stridea] = v_2 * x_0A + v_4 * x_0B
        out[3 * stridea] = v_5 * (x_10 - x_11)
        out[4 * stridea] = v_7 * (x_08 - x_09)
        out[5 * stridea] = v_5 * (x_10 + x_11)
        out[6 * stridea] = v_4 * x_0A - v_2 * x_0B
        out[7 * stridea] = v_7 * (x_0E + x_0F)

        src = src[strideb:]
        out = out[strideb:]

    return out

# FDCT 8x8
def fdct_8x8(src):
    tmp = np.zeros((8, 8), dtype=np.float32)
    tmp = fdct_1d_8x8(src, 1, 8)
    return fdct_1d_8x8(tmp, 8, 1)

# IDCT 1D for 8x8 block
def idct_1d_8x8(src, stridea, strideb):
    v_0 = -0.785695
    v_1 =  0.275899
    v_2 =  1.414214
    v_3 =  1.306563
    v_4 =  0.785695
    v_5 = -0.275899
    v_6 =  0.707107
    v_7 =  0.541196
    v_8 =  1.175876
    v_9 =  0.5
    v_A =  0.25
    v_B =  0.353553
    v_C =  1.387040

    out = np.zeros_like(src)

    for i in range(8):
        s_0 = src[0 * stridea]
        s_1 = src[1 * stridea]
        s_2 = src[2 * stridea]
        s_3 = src[3 * stridea]
        s_4 = src[4 * stridea]
        s_5 = src[5 * stridea]
        s_6 = src[6 * stridea]
        s_7 = src[7 * stridea]

        x_00 = v_2 * s_0
        x_01 = v_C * s_1 + v_1 * s_7
        x_02 = v_3 * s_2 + v_7 * s_6
        x_03 = v_8 * s_3 + v_4 * s_5
        x_04 = v_2 * s_4
        x_05 = v_0 * s_3 + v_8 * s_5
        x_06 = v_7 * s_2 - v_3 * s_6
        x_07 = -v_1 * s_1 + v_C * s_7
        x_09 = x_00 + x_04
        x_0A = x_01 + x_03
        x_0B = v_2 * x_02
        x_0C = x_00 - x_04
        x_0D = x_01 - x_03
        x_0E = v_B * (x_09 - x_0B)
        x_0F = v_B * (x_0C + x_0D)
        x_10 = v_B * (x_0C - x_0D)
        x_11 = v_2 * x_06
        x_12 = x_05 + x_07
        x_13 = x_05 - x_07
        x_14 = v_B * (x_11 + x_12)
        x_15 = v_B * (x_11 - x_12)
        x_16 = v_9 * x_13
        x_08 = -x_15

        out[0 * stridea] = v_A * (x_09 + x_0B) + v_B * x_0A
        out[1 * stridea] = v_6 * (x_0F - x_08)
        out[2 * stridea] = v_6 * (x_0F + x_08)
        out[3 * stridea] = v_6 * (x_0E + x_16)
        out[4 * stridea] = v_6 * (x_0E - x_16)
        out[5 * stridea] = v_6 * (x_10 - x_14)
        out[6 * stridea] = v_6 * (x_10 + x_14)
        out[7 * stridea] = v_A * (x_09 + x_0B) - v_B * x_0A

        src = src[strideb:]
        out = out[strideb:]

    return out

# IDCT 8x8
def idct_8x8(src):
    tmp = np.zeros((8, 8), dtype=np.float32)
    tmp = idct_1d_8x8(src, 1, 8)
    return idct_1d_8x8(tmp, 8, 1)



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