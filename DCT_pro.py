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

def DCT_process2(matrix):#處理陣列問題
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

def IDCT(dct):#處理陣列問題
   width = dct.shape[1]
   height = dct.shape[0]
   matrix = np.zeros_like(dct)

   for col in range(height):
       for row in range(width):
           matrix[col, row] = IDCT_process(dct, col, row)
   return matrix

def DCT(list):#主要DCT，處理資料傳接

    matrix = np.array(list)
    matrix = matrix.astype(int)
    dct_array = []
    '''
    for y in range(0,np.size(matrix,0)):
        for x in range(0,np.size(matrix,1)):
            dct_array.append(DCT_process2(matrix[y][x]))
    dct_array_np = [np.array(item) for item in dct_array]
    '''
    for y in range(0,np.size(matrix,0)):
        dct_array.append(DCT_process2(matrix[y]))
    dct_array_np = [np.array(item) for item in dct_array]
    return dct_array_np