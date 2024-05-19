import numpy as np #用於數值處理
import Convert_RGB_to_YUV
import crop
import DCT_pro as DCT
import Quantization as Q
import Zigzag as Z
import RLC
import DPCM
import Huffman_coding

image_path = "test2.jpg" #將圖像進行導入
blocks = crop.crop_image_into_8x8_blocks(image_path)
URLs = []
UDCs = []
for i in range(len(blocks)):
    img = blocks[i] #目前只取第一個圖片塊做處理，後續須透過迴圈處理所有資料
    YuvMatrix = np.array([[0.299, 0.587, 0.114],[-0.147, -0.289, 0.436],[0.615, -0.515, -0.100]]) #用於將RGB矩陣轉為YUV(Y，Cb,Cr)
    RgbMatrix = np.array([[1, 0, 1.140],[1, -0.395, -0.581],[1, 2.032, 0]]) #用於將YUV矩陣轉為RGB(R，G,B)

    """
    def Calculate_length_and_width(img):
        size = img.shape #計算圖像長與寬
        return size
    """

    def Convert_RGB(YUV):
        YUV[:, :, 1:] -= 128.0
        RGB = np.dot(YUV,RgbMatrix.T)
        return RGB

    #用於測試
    #size = Calculate_length_and_width(img) #求來源圖像的長度與高度
    zero_channel = Convert_RGB_to_YUV.Creative_Zeros(img) #產生與來源圖像長度與高度相同的全零矩陣
    RData,GData,BData = Convert_RGB_to_YUV.Cut_RGB(img,zero_channel) #切割來源圖像並分成RGB三種通道
    YUV = Convert_RGB_to_YUV.Convert_YUV(img,YuvMatrix) #將來源圖像轉為YUV
    YSpllit,USplist,VSplite,Y,U,V= Convert_RGB_to_YUV.Cut_YUV(YUV) #將以轉變成YUV的圖像進行YUV切割
    #RGB = Convert_RGB(YUV) #將以轉換成YUV的圖像轉成RGB圖像
    #Convert_RGB_to_YUV.Show_RGB(RData,GData,BData) #顯示RGB三個通道畫面
    #Convert_RGB_to_YUV.Show_YUV(Y,U,V) #顯示YUV三個通道畫面
    #Convert_RGB_to_YUV.Show_Convent_RGB(RGB) #顯示經由轉變過YUV後再轉回RGB的圖像(用來確定有沒有翻轉失誤)
    YTemp = [[174,172,170,169,170,176,182,186],
            [171,170,168,168,170,174,180,182],
            [166,165,165,164,168,170,175,176],
            [156,156,156,158,161,162,166,167],
            [146,146,148,149,152,153,156,156],
            [139,140,140,141,144,146,146,147],
            [134,134,136,137,138,141,142,143],
            [133,133,134,134,136,139,140,143]]

    DCTU = DCT.DCT(U)
    DCTV = DCT.DCT(V)

    QY = Q.YQuantization(Y)
    QU = Q.CbCrQuantization(DCTU)
    QV = Q.CbCrQuantization(DCTV)
    
    YAC = Z.Zigzag(QY.tolist())
    YRL = RLC.RLC(YAC)
    """
    YAC = Z.Zigzag(QY.tolist())
    UAC = Z.Zigzag(QU.tolist())
    VAC = Z.Zigzag(QV.tolist())
    
    YRL = RLC.RLC(YAC)
    URL = RLC.RLC(UAC)
    VRL = RLC.RLC(VAC)
    """
    UDCs.append(QU[0][0])
    #URLs.append(URL)

UDPCM = DPCM.DPCM(UDCs)

DC,AC,encoded_dc_bitstream,encoded_ac_bitstream,compressed_data,dc_huffman_tree,ac_huffman_tree,decoded_dc_coeffs,decoded_ac_coeffs = Huffman_coding.Huffman_code(UDPCM,YRL)

print("Original DC Coefficients:", DC,'\n')
print("Original AC Coefficients:", AC,'\n')
print("Encoded DC Bitstream:", encoded_dc_bitstream,'\n')
print("Encoded AC Bitstream:", encoded_ac_bitstream,'\n')
print("Compressed Data:", compressed_data,'\n')
print("Decoded DC Coefficients:", decoded_dc_coeffs,'\n')
print("Decoded AC Coefficients:", decoded_ac_coeffs,'\n')

'''
print(YRL)
print(UDPCM)
'''