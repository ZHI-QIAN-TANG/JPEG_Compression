# 將二維數據轉成一維數據
# 透過斜線掃描方式，針對每行斜線用索引值轉換方向，單數向左下，雙數往右上
# 將掃描到的數值依序填入一維陣列中，形成一維資料

def Zigzag(block):
    # 寬高皆為 8
    h = 8
    w = 8
    result = []
    
    bound = h + w - 1 # 總共15條斜線
    for i in range(bound):
        if i % 2 == 0:
            x = min(i, h - 1)
            y = i - x
            while x >= 0 and y < w:
                result.append(block[x][y])
                x -= 1
                y += 1
        else:
            y = min(i, w - 1)
            x = i - y
            while y >= 0 and x < h:
                result.append(block[x][y])
                y -= 1
                x += 1
    
    return result

# 對量化後的 8x8 區塊進行 Zigzag 掃描