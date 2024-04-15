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