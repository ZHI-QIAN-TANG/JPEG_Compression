def DPCM (blocks): #輸入所有8x8的圖塊，能產出DC編碼
    DCs = []
    for i in range(len(blocks)):
        if i == 0:
            DCs.append(blocks[i][0][0])
        else: #紀錄DC值之間的差距
            DCs.append(blocks[i][0][0] - blocks[i-1][0][0])
    return DCs