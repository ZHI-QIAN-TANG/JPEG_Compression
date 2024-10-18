import numpy as np
def Padding8x8(image): # 將輸入進來的圖片大小一律擴充成8的倍數
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image_array = np.array(image)
    height, width, channels = image_array.shape
    
    # 計算補零所需的大小
    pad_height = (8 - (height % 8)) % 8
    pad_width = (8 - (width % 8)) % 8

    # 建立補零後的新陣列 (填充為0)
    new_height = height + pad_height
    new_width = width + pad_width
    padded_image = np.zeros((new_height, new_width, channels), dtype=np.uint8)

    # 將原始圖片的像素資料複製到新陣列中
    for h in range(height):
        for w in range(width):
            for c in range(channels):
                padded_image[h, w, c] = image_array[h, w, c]

    return padded_image, new_height, new_width

