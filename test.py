import Convert_RGB_to_YUV as CRTY
import cv2
import numpy

img = cv2.imread('test.jpg') #將圖像進行導入

size = CRTY.Calculate_length_and_width(img)

print(img)