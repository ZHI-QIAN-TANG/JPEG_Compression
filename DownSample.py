import numpy as np

def downsample_8x8_to_4x4(matrix):
    # 初始化一個 4x4 矩陣
    result = [[0] * 4 for _ in range(4)]

    # 將 8x8 區塊的 2x2 小區域取平均後填入 4x4 區塊
    for i in range(4):
        for j in range(4):
            # 計算對應的 2x2 小區域的起始位置
            r, c = i * 2, j * 2
            
            # 取 2x2 小區域的平均值
            avg = (matrix[r][c] + matrix[r][c + 1] +
                   matrix[r + 1][c] + matrix[r + 1][c + 1]) // 4
            
            result[i][j] = avg

    return result

def merge_4x4_to_8x8(block1, block2, block3, block4):
    # 初始化一個 8x8 矩陣
    result = np.zeros((8, 8), dtype=int)

    # 將 4 個 4x4 區塊依照位置填入 8x8 矩陣
    result[:4, :4] = block1  # 左上
    result[:4, 4:] = block2  # 右上
    result[4:, :4] = block3  # 左下
    result[4:, 4:] = block4  # 右下

    return result



#note
#Z-zag 要加的東西:    w,h = block.shape    block = block.tolist()
#header 要加的東西: table_Y 和 table_C 要 np.array()
#main 要加的東西 : YAC = Z.Zigzag(QY.tolist()) 的 tolist要拔掉，因為 Z-zag 有了





'''
import numpy as np
from PIL import Image

# 1. 轉換 RGB 圖像為 YCbCr 色彩空間
def rgb_to_ycbcr(image):
    return image.convert('YCbCr')

# 2. 對色度通道 (Cb, Cr) 進行 4:2:0 降採樣
def downsample_420(ycbcr_image):
    # 取得 Y, Cb, Cr 三個通道
    y, cb, cr = ycbcr_image.split()

    # 將 Cb 和 Cr 通道降採樣 (4:2:0)
    cb = np.array(cb)
    cr = np.array(cr)
    print(cb)
    # Cb 和 Cr 每 2x2 區域降採樣，取上方左側像素的值
    cb_downsampled = cb[::2, ::2]
    cr_downsampled = cr[::2, ::2]
    print(cb_downsampled)
    return np.array(y), cb_downsampled, cr_downsampled

# 3. 將降採樣後的數據重新拼接
def upsample_and_merge(y, cb_downsampled, cr_downsampled):
    # 將 Cb 和 Cr 升採樣回原本大小
    cb_upsampled = np.repeat(np.repeat(cb_downsampled, 2, axis=0), 2, axis=1)
    cr_upsampled = np.repeat(np.repeat(cr_downsampled, 2, axis=0), 2, axis=1)

    # 拼接 Y, Cb, Cr 通道
    ycbcr_upsampled = np.stack([y, cb_upsampled, cr_upsampled], axis=-1)
    return ycbcr_upsampled

# 測試範例
if __name__ == "__main__":
    # 讀取圖像
    img = Image.open("test2.jpg")
    
    # 轉換為 YCbCr 色彩空間
    ycbcr_image = rgb_to_ycbcr(img)
    
    # 進行 4:2:0 降採樣
    y, cb_downsampled, cr_downsampled = downsample_420(ycbcr_image)
    
    # 將降採樣結果輸出
    print("Y channel shape:", y.shape)
    print("Cb channel shape (downsampled):", cb_downsampled.shape)
    print("Cr channel shape (downsampled):", cr_downsampled.shape)
    
    # 測試升採樣並重新合併
    ycbcr_upsampled = upsample_and_merge(y, cb_downsampled, cr_downsampled)
    print("YCbCr upsampled shape:", ycbcr_upsampled.shape)
'''