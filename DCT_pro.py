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


#確認答案的部分
from scipy.fftpack import dct, idct

def DCT(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')

def IDCT(dct_matrix):
    return idct(idct(dct_matrix.T, norm='ortho').T, norm='ortho')

'''
#版本2
import numpy as np
import math
import crop 

"""
    只要呼叫DCT()就好，其餘是計算過程        
"""

def DCT_process(matrix, i, j):#DCT公式
    width = matrix.shape[1]
    height = matrix.shape[0]
    value = 0.
    for col in range(height):
       for row in range(width):
           save = matrix[col, row] 
           save *= math.cos(math.pi * (2 * col + 1) * i / (2. * height))
           save *= math.cos(math.pi * (2 * row + 1) * j / (2. * width))
           value += save
    c = 1.
    if i == 0:
        c /= np.sqrt(2)
    if j == 0:
        c /= np.sqrt(2)

    return (2. / np.sqrt(height * width)) * c * value

def DCT(matrix):#主要被呼叫的DCT函式
    width = matrix.shape[1]
    height = matrix.shape[0]
    dct = np.zeros_like(matrix)

    for col in range(height):
        for row in range(width):
           dct[col, row] = DCT_process(matrix, col, row)
    
    return dct

def IDCT_process(dct, i, j):#逆DCT公式
   width = dct.shape[1]
   height = dct.shape[0]
   value = 0

   for col in range(height):
       for row in range(width):
           save = dct[col, row] 
           if col == 0:
               save /= np.sqrt(2)
           if row == 0:
               save /= np.sqrt(2)
           save *= math.cos(math.pi * (2 * i + 1) * col / (2. * height))
           save *= math.cos(math.pi * (2 * j + 1) * row / (2. * width))
           value += save

   return (2. / np.sqrt(height * width)) * value

def IDCT(dct):#逆DCT函式
   width = dct.shape[1]
   height = dct.shape[0]
   matrix = np.zeros_like(dct)

   for col in range(height):
       for row in range(width):
           matrix[col, row] = IDCT_process(dct, col, row)
   return matrix
'''