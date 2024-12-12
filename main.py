import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import time
import numpy as np
import Convert_RGB_to_YUV
import padding8x8
import crop
import RGBToYCbCrTest
import DCT_pro as DCT
import Quantization as Q
import Zigzag as Z
import RLC
import DPCM
import AC_DC_tree_DHT
import header as h
import Huffman_coding_cf as t
import DownSample as DS

def generate_encoded_data(image_path, progress_callback):
    print(f"Processing image: {image_path}")
    img = Image.open(image_path)
    start_time = time.time()
    width, height = img.size
    padding_picture, new_height, new_width = padding8x8.Padding8x8(img)
    blocks = crop.crop_image_into_8x8_blocks(padding_picture, new_height, new_width)
    
    URLs = []
    UDCs = []
    YRLs = []
    YDCs = []
    VRLs = []
    VDCs = []

    for i in range(len(blocks)):
        img = blocks[i]
        Y, Cb, Cr = RGBToYCbCrTest.ConvertRGBToYCbCr(img)
        DCTY = DCT.DCT(Y)
        DCTCb = DCT.DCT(Cb)
        DCTCr = DCT.DCT(Cr)

        QY = Q.YQuantization(DCTY)
        QCb = Q.CbCrQuantization(DCTCb)
        QCr = Q.CbCrQuantization(DCTCr)

        YAC = Z.Zigzag(QY.tolist())
        CbAC = Z.Zigzag(QCb.tolist())
        CrAC = Z.Zigzag(QCr.tolist())
        YAC = YAC[1:]
        CbAC = CbAC[1:]
        CrAC = CrAC[1:]

        YRL = RLC.RLC(YAC)
        URL = RLC.RLC(CbAC)
        VRL = RLC.RLC(CrAC)

        YDCs.append(QY[0][0])
        YRLs.append(YRL)
        UDCs.append(QCb[0][0])
        URLs.append(URL)
        VDCs.append(QCr[0][0])
        VRLs.append(VRL)

        progress_callback(i + 1, len(blocks))

    YDPCM = DPCM.DPCM(YDCs)
    UDPCM = DPCM.DPCM(UDCs)
    VDPCM = DPCM.DPCM(VDCs)

    encoded_bytes = t.Huffman_coding(YDPCM, UDPCM, VDPCM, YRLs, URLs, VRLs)
    return encoded_bytes, width, height,start_time

def compress_image(input_path, output_path, progress_callback):
    
    encoded_bytes, width, height,start_time = generate_encoded_data(input_path, progress_callback)
    header = h.generate_jpeg_header(width, height, encoded_bytes)

    with open(output_path, 'wb') as f:
        f.write(header)
    
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    return file_path

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg")])
    return file_path

def start_compression():
    input_path = select_file()
    if not input_path:
        return

    output_path = save_file()
    if not output_path:
        return

    progress_bar["value"] = 0
    progress_bar.update()

    def update_progress(current, total):
        progress_bar["value"] = (current / total) * 100
        progress_bar.update()

    try:
        execution_time = compress_image(input_path, output_path, update_progress)
        messagebox.showinfo("完成", f"壓縮完成！處理時間: {execution_time:.2f} 秒")
    except Exception as e:
        messagebox.showerror("錯誤", f"壓縮失敗: {e}")

app = tk.Tk()
app.title("圖片壓縮工具")
app.geometry("600x400")

label = tk.Label(app, text="選擇圖片進行壓縮", font=("Arial", 14))
label.pack(pady=40)

compress_button = tk.Button(app, text="開始壓縮", command=start_compression, font=("Arial", 12))
compress_button.pack(pady=40)

progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=40)

app.mainloop()
