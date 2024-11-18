# AC 跳過DC值後，Z字編碼
# 回傳值為AC值陣列(已去掉DC值)
def Zigzag(blocks) :
    i = 0
    j = 0
    flag = 0 #用來判斷該朝甚麼方向走的旗子，0代表向右走，1代表向左下走，2代表向下走，3代表向右上走
    ACs = []

    for _ in range(63): #因實際情況為且切割成8*8而非3*3，因此實際情況3*3替換成8*8
        #用除4的餘數讓flag一直在0~3內循環
        flag %= 4
        #向右走
        if flag == 0:
            j += 1
            #如果超出右邊範圍，則改為向下走
            if j == 8: #實際情況j = 3替換成j = 8
                j -= 1
                i += 1
            ACs.append(blocks[i][j])
            flag += 1
            continue
        
        #向左下走
        if flag == 1:
            i += 1
            j -= 1
            ACs.append(blocks[i][j])
            #走到底後flag +1
            if i == 7 or j == 0: #實際情況i = 2替換成i = 8
                flag += 1
            continue

        #向下走
        if flag == 2:
            i += 1
            #如果超出底邊範圍，則改為向右走
            if i == 8: #實際情況i = 3替換成i = 8
                i -= 1
                j += 1
            ACs.append(blocks[i][j])
            flag += 1
            continue

        #向右上走
        if flag == 3:
            i -= 1
            j += 1
            ACs.append(blocks[i][j])
            #走到底後flag +1
            if i == 0 or j == 7: #實際情況j = 2替換成j = 8
                flag += 1
            continue
    
    return ACs