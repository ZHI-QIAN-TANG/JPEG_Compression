import cv2 #載入影像處理函式
import numpy as np #用於數值處理
from PIL import Image #用於切割圖片

def Creative_Zeros(img):
    zero_channel = np.zeros(img.shape[0:2], dtype = "uint8") #創造一個img的高度與長度的全零矩陣，此外設定為8位元整數(0到255)
    return zero_channel

def Cut_RGB(img,zero_channel):
    (R,G,B) = cv2.split(img) #將img分割成3種顏色矩陣(RGB)
    imgR = cv2.merge([zero_channel, zero_channel, R]) #將矩陣進行合併(這麼做的原因是因為要確保高度與長度的一致性)
    imgG = cv2.merge([zero_channel, G, zero_channel]) #將矩陣進行合併(這麼做的原因是因為要確保高度與長度的一致性)
    imgB = cv2.merge([B, zero_channel, zero_channel]) #將矩陣進行合併(這麼做的原因是因為要確保高度與長度的一致性)
    RData = np.array(imgR) #轉換成array(這步驟用於可以利用numpy的指令)
    GData = np.array(imgG) #轉換成array(這步驟用於可以利用numpy的指令)
    BData = np.array(imgB) #轉換成array(這步驟用於可以利用numpy的指令)
    return RData,GData,BData

def Convert_YUV(img,YuvMatrix):
    YUV = np.dot(img,YuvMatrix.T) #將資料藉由內積的方式來進行彩度轉換(.T是用於將矩陣翻轉以利計算)
    YUV[:, :, 1:] += 128.0 #將UV的部份加上128來維持範圍
    '''
    YUV[:, :, 0] (Y通道)
    YUV[:, :, 1] (U通道)
    YUV[:, :, 2] (V通道)
    因為我們要取U和V的資料進行加128的處理所以寫成[:, :, 1:]是要將U和V的通道都被選取起來並進行處理
    '''
    return YUV

def Cut_YUV(YUV):
    (Y1,U1,V1) = cv2.split(YUV) #將YUV分割成3種顏色矩陣(Y1,U1,V1)可以用於看出與以下的差別
    (Y,U,V) = cv2.split(YUV.astype(np.uint8))#將YUV分割成3種顏色矩陣(Y,U,V)並將資料型態轉換為8為元整數(0到255)
    YSpllit = []
    USplist = []
    VSplite = []
    for i in range(len(Y)):
        YSpllit.append(Y[i].tolist())
        USplist.append(U[i].tolist())
        VSplite.append(V[i].tolist())
    return YSpllit,USplist,VSplite,Y,U,V


def Show_Convent_RGB(RGB):
    Convent_RGB = RGB.astype(np.uint8)
    Convent_RGB = cv2.resize(Convent_RGB, (1080, 720))
    cv2.imshow('Convent_RGB',Convent_RGB)
    cv2.waitKey(0)

def Show_RGB(imgR,imgG,imgB):
    #顯示YUV的影像但因為openCV沒有對應YUV的顯示方式所以是用RGB的方式讀取YUV的資料
    imgR = cv2.resize(imgR, (1080, 720))
    imgG = cv2.resize(imgG, (1080, 720))
    imgB = cv2.resize(imgB, (1080, 720))
    cv2.imshow("R",imgR)
    cv2.imshow("G",imgG)
    cv2.imshow("B",imgB)
    cv2.waitKey(0)

def Show_YUV(Y,U,V):
    #顯示YUV的影像但因為openCV沒有對應YUV的顯示方式所以是用RGB的方式讀取YUV的資料
    Y = cv2.resize(Y, (1080, 720))
    U = cv2.resize(U, (1080, 720))
    V = cv2.resize(V, (1080, 720))
    cv2.imshow("Y",Y)
    cv2.imshow("Cb",U)
    cv2.imshow("Cr",V)
    cv2.waitKey(0)
