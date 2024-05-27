'''
import sys
import os
import numpy as np
import Convert_RGB_to_YUV
import crop
import DCT_pro as DCT
import Quantization as Q
import Zigzag as Z
import RLC
import DPCM
import Huffman_coding

def generate_encoded_data(image_path):
    blocks = crop.crop_image_into_8x8_blocks(image_path)
    URLs = []
    UDCs = []
    for i in range(len(blocks)):
        img = blocks[i]
        YuvMatrix = np.array([[0.299, 0.587, 0.114],[-0.147, -0.289, 0.436],[0.615, -0.515, -0.100]])
        zero_channel = Convert_RGB_to_YUV.Creative_Zeros(img)
        RData,GData,BData = Convert_RGB_to_YUV.Cut_RGB(img,zero_channel)
        YUV = Convert_RGB_to_YUV.Convert_YUV(img,YuvMatrix)
        YSpllit,USplist,VSplite,Y,U,V= Convert_RGB_to_YUV.Cut_YUV(YUV)

        DCTU = DCT.DCT(U)
        DCTV = DCT.DCT(V)

        QY = Q.YQuantization(Y)
        QU = Q.CbCrQuantization(DCTU)
        QV = Q.CbCrQuantization(DCTV)
        
        YAC = Z.Zigzag(QY.tolist())
        UAC = Z.Zigzag(QU.tolist())
        VAC = Z.Zigzag(QV.tolist())
        
        YRL = RLC.RLC(YAC)
        URL = RLC.RLC(UAC)
        VRL = RLC.RLC(VAC)

        UDCs.append(QU[0][0])
        URLs.append(URL)

    UDPCM = DPCM.DPCM(UDCs)

    DC,AC,encoded_dc_bitstream,encoded_ac_bitstream,compressed_data,dc_huffman_tree,ac_huffman_tree,decoded_dc_coeffs,decoded_ac_coeffs = Huffman_coding.Huffman_code(UDPCM,URLs)

    # 在這裡將 compressed_data 放入 encoded_data
    encoded_data = compressed_data

    return encoded_data

def write_jpeg_file(encoded_data, output_file):
    # 打開輸出檔案
    with open(output_file, "wb") as f:
        # 寫入 SOI 標記
        f.write(b"\xFF\xD8")

        # 寫入 APP0 標記
        app0_segment = b"\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        f.write(app0_segment)

        # 寫入編碼的資料
        f.write(encoded_data)

        # 寫入 EOI 標記
        f.write(b"\xFF\xD9")

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py input_image output_jpeg")
        sys.exit(1)

    input_image = sys.argv[1]
    output_jpeg = sys.argv[2]

    # 假設您已經實現了將圖片進行編碼並生成編碼後的資料的函數
    encoded_data = generate_encoded_data(input_image)

    # 將編碼後的資料寫入 JPEG 檔案中
    write_jpeg_file(encoded_data, output_jpeg)

if __name__ == "__main__":
    main()
'''


import numpy as np #用於數值處理
import Convert_RGB_to_YUV
import crop
import DCT_pro as DCT
import Quantization as Q
import Zigzag as Z
import RLC
import DPCM
import Huffman_coding_ac
import Huffman_coding_dc

'''
image_path = "test2.jpg" # 將圖像進行導入
blocks = crop.crop_image_into_8x8_blocks(image_path) # 將圖片分割成8*8的小塊作處理
URLs = [] # 存Y的所有AC編碼值
UDCs = [] # 存U的所有DC值
for i in range(len(blocks)):
    img = blocks[i] # 取出8*8的像素
    YuvMatrix = np.array([[0.299, 0.587, 0.114],[-0.147, -0.289, 0.436],[0.615, -0.515, -0.100]]) # 用於將RGB矩陣轉為YUV(Y，Cb,Cr)
    RgbMatrix = np.array([[1, 0, 1.140],[1, -0.395, -0.581],[1, 2.032, 0]]) # 用於將YUV矩陣轉為RGB(R，G,B)

    
    def Calculate_length_and_width(img):
        size = img.shape #計算圖像長與寬
        return size
    

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

    # 二維離散餘弦轉換，將像素值轉換為頻率域的值
    DCTU = DCT.DCT(U)
    DCTV = DCT.DCT(V)

    # 量化處理，壓縮高頻訊號
    QY = Q.YQuantization(Y)
    QU = Q.CbCrQuantization(DCTU)
    QV = Q.CbCrQuantization(DCTV)
    
    # AC值編碼
    # Z字編碼
    YAC = Z.Zigzag(QY.tolist())
    UAC = Z.Zigzag(QU.tolist())
    VAC = Z.Zigzag(QV.tolist())
    # RL編碼，回傳值為二維陣列
    YRL = RLC.RLC(YAC)
    URL = RLC.RLC(UAC)
    VRL = RLC.RLC(VAC)


    UDCs.append(QU[0][0])
    URLs.append(URL)

# U的DC值做DC編碼(DPCM)
UDPCM = DPCM.DPCM(UDCs)


huffman_encoded_data_ac, ac_huffman_tree = Huffman_coding_ac.Huffman_code(URLs)
DC,encoded_dc_bitstream,compressed_data,dc_huffman_tree,decoded_dc_coeffs =Huffman_coding_dc.Huffman_code(UDPCM)
compressed_data = encoded_dc_bitstream + huffman_encoded_data_ac

#需要進入標頭的內容:
#compressed_data、dc_huffman_tree、ac_huffman_tree
'''



'''
print("Original DC Coefficients:", DC,'\n')
"""
print("Encoded DC Bitstream:", encoded_dc_bitstream,'\n')
print("Encoded AC Bitstream:", encoded_ac_bitstream,'\n')
print("Compressed Data:", compressed_data,'\n')
"""
print("Decoded DC Coefficients:", decoded_dc_coeffs,'\n')
print("Decoded AC Coefficients:", decoded_ac_coeffs,'\n')
'''

def generate_encoded_data(image_path):
    print(f"Processing image: {image_path}")
    blocks = crop.crop_image_into_8x8_blocks(image_path)
    URLs = []
    UDCs = []
    for i in range(len(blocks)):
        img = blocks[i]
        YuvMatrix = np.array([[0.299, 0.587, 0.114],[-0.147, -0.289, 0.436],[0.615, -0.515, -0.100]])
        zero_channel = Convert_RGB_to_YUV.Creative_Zeros(img)
        RData, GData, BData = Convert_RGB_to_YUV.Cut_RGB(img, zero_channel)
        YUV = Convert_RGB_to_YUV.Convert_YUV(img, YuvMatrix)
        YSpllit, USplist, VSplite, Y, U, V = Convert_RGB_to_YUV.Cut_YUV(YUV)

        DCTU = DCT.DCT(U)
        DCTV = DCT.DCT(V)

        QY = Q.YQuantization(Y)
        QU = Q.CbCrQuantization(DCTU)
        QV = Q.CbCrQuantization(DCTV)
        
        YAC = Z.Zigzag(QY.tolist())
        UAC = Z.Zigzag(QU.tolist())
        VAC = Z.Zigzag(QV.tolist())
        
        YRL = RLC.RLC(YAC)
        URL = RLC.RLC(UAC)
        VRL = RLC.RLC(VAC)

        UDCs.append(QU[0][0])
        URLs.append(URL)

    UDPCM = DPCM.DPCM(UDCs)

    huffman_encoded_data_ac, ac_huffman_tree = Huffman_coding_ac.Huffman_code(URLs)
    DC,encoded_dc_bitstream,compressed_data,dc_huffman_tree,decoded_dc_coeffs =Huffman_coding_dc.Huffman_code(UDPCM)
    compressed_data = encoded_dc_bitstream + huffman_encoded_data_ac

    ##需要進入標頭的內容:
    #compressed_data、dc_huffman_tree、ac_huffman_tree

    return compressed_data

def write_jpeg_file(encoded_data, output_file):
    # 打開輸出檔案
    with open(output_file, "wb") as f:
        # 寫入 SOI 標記
        f.write(b"\xFF\xD8")

        # 寫入 APP0 標記
        app0_segment = b"\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        f.write(app0_segment)

        # 寫入編碼的資料
        f.write(encoded_data)

        # 寫入 EOI 標記
        f.write(b"\xFF\xD9")

    print(f"JPEG file written: {output_file}")

def main():
    image_path = "test2.jpg"
    output_jpeg = "output.jpg"

    # 假設您已經實現了將圖片進行編碼並生成編碼後的資料的函數
    encoded_data = generate_encoded_data(image_path)

    if encoded_data:
        print(f"Encoded data size: {len(encoded_data)} bytes")
        # 將編碼後的資料寫入 JPEG 檔案中
        write_jpeg_file(encoded_data, output_jpeg)
    else:
        print("Failed to generate encoded data.")

if __name__ == "__main__":
    main()
