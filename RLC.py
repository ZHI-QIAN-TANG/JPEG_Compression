# 變動長度編碼(Run-Length Coding：RLC)，跳過DC值後，紀錄數列有幾個0以及下個不是0的數值
# 回傳值為二維陣列
def RLC(ACs):
    RL = []
    count = 0
    for i in range(len(ACs)):
        if ACs[i] == 0:
            count += 1
        else:
            RL.append([count, ACs[i]])
            count = 0
    if count != 0:
        RL.append([0,0])
    return RL