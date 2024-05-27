# 變動長度編碼(Run-Length Coding：RLC)，跳過DC值後，紀錄數列有幾個0以及下個不是0的數值
# 回傳值為二維陣列
def RLC(ACs):
    RL = []
    count = 0
    
    for i in range(len(ACs)):
        if ACs[i] == 0:
            count += 1
            if count == 16:
                RL.append([15, 0])  # 16个0视为一个ZRL
                count = 0
        else:
            while count > 15:  # 如果有超过15个连续的零
                RL.append([15, 0])  # 添加一个ZRL
                count -= 16
            RL.append([count, ACs[i]])
            count = 0
    
    # 结束时添加EOB标志
    if count != 0:
        RL.append([0, 0])
    
    return RL
