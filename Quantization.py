import numpy as np

# 量化(原訊號 / Qtable)，返回值為整數
# Y值量化
def YQuantization(Y):
    YQuantizationTable = np.array([[16, 11, 10, 16, 24, 41, 51, 61],
                                  [12, 12, 14, 19, 26, 58, 60, 55],
                                  [14, 13, 16, 24, 40, 67, 69, 56],
                                  [14, 17, 22, 29, 51, 87, 80, 62],
                                  [18, 22, 37, 56, 68, 109, 103, 77],
                                  [24, 35, 55, 64, 81, 104, 113, 92],
                                  [49, 64, 78, 87, 103, 121, 120, 101],
                                  [72, 92, 95, 98, 112, 100, 103, 99]], dtype=np.float32)
    return np.round(Y / YQuantizationTable).astype(int)

# CbCr值量化
def CbCrQuantization(CbCr):
    CbCrQuantizationTable = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                                      [18, 21, 26, 66, 99, 99, 99, 99],
                                      [24, 26, 56, 99, 99, 99, 99, 99],
                                      [47, 66, 99, 99, 99, 99, 99, 99],
                                      [99, 99, 99, 99, 99, 99, 99, 99],
                                      [99, 99, 99, 99, 99, 99, 99, 99],
                                      [99, 99, 99, 99, 99, 99, 99, 99],
                                      [99, 99, 99, 99, 99, 99, 99, 99]], dtype=np.float32)
    return np.round(CbCr / CbCrQuantizationTable).astype(int)
