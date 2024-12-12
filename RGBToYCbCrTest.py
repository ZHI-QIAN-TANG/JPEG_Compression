import numpy as np

def ConvertRGBToYCbCr(img):
# 加载图片并获取像素数据
    image = img  # img现在是一个numpy数组
    height, width, _ = image.shape

    # 初始化用于存储 Y, U, V 通道值的数组
    Y_channel = np.zeros((height, width), dtype=int)
    Cb_channel = np.zeros((height, width), dtype=int)
    Cr_channel = np.zeros((height, width), dtype=int)

    # RGB 到 YCbCr 转换公式
    for x in range(width):
        for y in range(height):
            r, g, b = image[y, x][:3]
            # print(r,g,b)
            # 计算 YCbCr 通道的值
            Y = 0.299 * r + 0.587 * g + 0.114 * b
            Cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 128
            Cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 128
            
            # 确保在 0-255 范围内
            Y_channel[y][x] = max(0, min(255, int(round(Y))))
            Y_channel[y][x] = Y_channel[y][x] - 128
            Cb_channel[y][x] = max(0, min(255, int(round(Cb))))
            Cb_channel[y][x] = Cb_channel[y][x] - 128
            Cr_channel[y][x] = max(0, min(255, int(round(Cr))))
            Cr_channel[y][x] = Cr_channel[y][x] - 128

    # 打印或保存 Y, U, V 通道值
    # 这里可以将 Y_channel, U_channel, V_channel 保存为文本文件或者以其他格式保存
    # 也可以直接输出一部分通道值来检查
    # print("Y channel:", Y_channel)  # 打印Y通道值
    # print("U channel:", Cb_channel[:5])  # 打印前5行U通道值
    # print("V channel:", Cr_channel[:5])  # 打印前5行V通道值
    return Y_channel, Cb_channel, Cr_channel