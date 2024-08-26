import numpy as np
import DCT_pro as old_dct

def dct_1d(x):#一維DCT公式
    N = len(x)
    answer = np.zeros(N)
    factor = np.pi / (2 * N)
    for k in range(N):
        sum_val = 0.0
        for n in range(N):
            sum_val += x[n] * np.cos(factor * (2 * n + 1) * k)
        if k == 0:
            sum_val *= np.sqrt(1 / N)
        else:
            sum_val *= np.sqrt(2 / N)
        answer[k] = int(sum_val)
    return answer


def DCT(matrix):#主要呼叫的函式:dct_2d
    M, N = matrix.shape
    dct_matrix = np.zeros((M, N))
    
    # 對每一列進行一維DCT
    for i in range(M):
        dct_matrix[i, :] = dct_1d(matrix[i, :])
    
    # 對每一行進行一維DCT
    for j in range(N):
        dct_matrix[:, j] = dct_1d(dct_matrix[:, j])
    
    return dct_matrix

'''
#確認答案的部分
from scipy.fftpack import dct, idct

def TDCT(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def IDCT(dct_matrix):
    return idct(idct(dct_matrix.T, norm='ortho').T, norm='ortho')
# 示例矩陣
matrix = np.array([
    [52, 55, 61, 66, 70, 61, 64, 73],
    [63, 59, 55, 90, 109, 85, 69, 72],
    [62, 59, 68, 113, 144, 104, 66, 73],
    [63, 58, 71, 122, 154, 106, 70, 69],
    [67, 61, 68, 104, 126, 88, 68, 70],
    [79, 65, 60, 70, 77, 68, 58, 75],
    [85, 71, 64, 59, 55, 61, 65, 83],
    [87, 79, 69, 68, 65, 76, 78, 94]
])
# 計算二維DCT
dct_result = DCT(matrix)
print(dct_result)
print("-----------")
print(TDCT(matrix))
'''