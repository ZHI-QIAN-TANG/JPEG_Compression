# 差分編碼（Differential Pulse CodeModulation：DPCM），紀錄與上個DC值得差值，產生DC編碼
# 回傳值為陣列
def DPCM (blocks): #輸入所有8x8的圖塊
    DCs = []
    for i in range(len(blocks)):
        if i == 0:
            DCs.append(blocks[i])
        else: #紀錄DC值之間的差距
            DCs.append(blocks[i] - blocks[i-1])
    return DCs