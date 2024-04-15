#測試資料集
A = [
    [1,2,0],
    [-2,1,0],
    [0,-1,0]
]

i = 0
j = 0
flag = 0 #用來判斷該朝甚麼方向走的旗子，0代表向右走，1代表向左下走，2代表向下走，3代表向右上走
ACs = []

for _ in range(8): #因實際情況為且切割成8*8而非3*3，因此實際情況3*3替換成8*8
    #用除4的餘數讓flag一直在0~3內循環
    flag %= 4
    #向右走
    if flag == 0:
        j += 1
        #如果超出右邊範圍，則改為向下走
        if j == 3: #實際情況j = 3替換成j = 8
            j -= 1
            i += 1
        ACs.append(A[i][j])
        flag += 1
        continue
    
    #向左下走
    if flag == 1:
        i += 1
        j -= 1
        ACs.append(A[i][j])
        #走到底後flag +1
        if i == 2 or j == 0: #實際情況i = 2替換成i = 8
            flag += 1
        continue

    #向下走
    if flag == 2:
        i += 1
        #如果超出底邊範圍，則改為向右走
        if i == 3: #實際情況i = 3替換成i = 8
            i -= 1
            j += 1
        ACs.append(A[i][j])
        flag += 1
        continue

    #向右上走
    if flag == 3:
        i -= 1
        j += 1
        ACs.append(A[i][j])
        #走到底後flag +1
        if i == 0 or j == 2: #實際情況j = 2替換成j = 8
            flag += 1
        continue
print(ACs)
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
print(RL)