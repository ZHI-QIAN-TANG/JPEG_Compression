from PIL import Image
import numpy as np # 用於數值處理

def crop_image_into_8x8_blocks(padded_image, height, width): # 將圖片分割成8*8的小塊
    img = Image.fromarray(padded_image) # 將補零後的 numpy 陣列轉回 PIL 圖片格式
    cropped_blocks = [] #用於存儲切割完的圖片
    for y in range(0, height, 8): #高 每8格為一數
        for x in range(0, width, 8): #寬 每8格為一數
            box = (x, y, x + 8, y + 8 )#圖片左上和右下頂點的座標(可鎖定切割範圍)
            cropped_block = img.crop(box) #透過crop函式切割圖片
            cropped_blocks.append(cropped_block) #將切割完的圖片加入陣列中存儲
    cropped_blocks_np = [np.array(block) for block in cropped_blocks]#將所有圖片轉為numpy的array形式，後續才可做資料處理
    return cropped_blocks_np
