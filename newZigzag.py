import numpy as np

def zigzag_scan(block):
    h, w = block.shape
    result = np.zeros(h * w)
    index = -1
    
    bound = h + w - 1
    for i in range(bound):
        if i % 2 == 0:
            x = min(i, h - 1)
            y = i - x
            while x >= 0 and y < w:
                index += 1
                result[index] = block[x, y]
                x -= 1
                y += 1
        else:
            y = min(i, w - 1)
            x = i - y
            while y >= 0 and x < h:
                index += 1
                result[index] = block[x, y]
                y -= 1
                x += 1
    
    return result

# 對量化後的 8x8 區塊進行 Zigzag 掃描
