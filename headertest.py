import pickle
import Huffman_coding_cf
import Zigzag as z

def generate_jpeg_header(width, height, encoded_bytes):
    # JPEG標頭常量部分
    SOI = b'\xFF\xD8'  # Start of Image
    APP0 = b'\xFF\xE0'  # Application Marker
    JFIF = b'JFIF\x00'  # JFIF標識符
    length = b'\x00\x10'  # APP0段長度
    version = b'\x01\x01'  # JFIF版本
    units = b'\x00'  # 密度單位（0：無單位，1：每英寸，2：每厘米）
    x_density = b'\x00\x48'  # X方向密度
    y_density = b'\x00\x48'  # Y方向密度
    x_thumb = b'\x00'  # 縮略圖寬度
    y_thumb = b'\x00'  # 縮略圖高度

    # 定義SOF0段（Start Of Frame 0）
    SOF0 = b'\xFF\xC0'
    sof_length = b'\x00\x11'  # 段長度
    precision = b'\x08'  # 精度
    height_bytes = height.to_bytes(2, 'big')
    width_bytes = width.to_bytes(2, 'big')
    num_components = b'\x03'  # 分量數（Y, Cb, Cr）

    # 每個分量的信息（Y, Cb, Cr）
    components = (
        b'\x01\x11\x00'  # Y分量（ID：1，取樣係數：1x1，量化表ID：0）
        b'\x02\x11\x01'  # Cb分量（ID：2，取樣係數：1x1，量化表ID：1）
        b'\x03\x11\x01'  # Cr分量（ID：3，取樣係數：1x1，量化表ID：1）
    )

    # 定義DQT段（Define Quantization Table）
    DQT_Y = b'\xFF\xDB'  # Define Quantization Table
    dqt_length_Y = b'\x00\x43'  # 段長度
    dqt_info_Y = b'\x00'  # 表信息
    table_Y = [ [16, 11, 10, 16, 24, 41, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 67, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99] ]
    q_table_Y = bytes(z.Zigzag(table_Y))

    # 定義量化表對於 Cb, Cr
    DQT_C = b'\xFF\xDB'  # Define Quantization Table
    dqt_length_C = b'\x00\x43'  # 段長度
    dqt_info_C = b'\x01'  # 表信息
    table_C = [ [17, 18, 24, 47, 99, 99, 99, 99],
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99]]
    q_table_C = bytes(z.Zigzag(table_C))

    # 定義DHT段（Huffman編碼表）
    y_dc_table = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
    y_ac_table = b'\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
    uv_dc_table = b'\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
    uv_ac_table = b'\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'

    # 定義SOS段（Start Of Scan）
    SOS = b'\xFF\xDA'
    sos_length = b'\x00\x0C'  # 段長度
    num_sos_components = b'\x03'  # 分量數
    sos_components = (
        b'\x01\x00'  # Y分量
        b'\x02\x11'  # Cb分量
        b'\x03\x11'  # Cr分量
    )
    start_spectral = b'\x00'
    end_spectral = b'\x3F'
    approx_high = b'\x00'

    # EOI標記（End of Image）
    EOI = b'\xFF\xD9'

    # 組裝JPEG標頭
    header = (
        SOI +
        APP0 + length + JFIF + version + units + x_density + y_density + x_thumb + y_thumb + 
        DQT_Y + dqt_length_Y + dqt_info_Y + q_table_Y +
        DQT_C + dqt_length_C + dqt_info_C + q_table_C +
        SOF0 + sof_length + precision + height_bytes + width_bytes + num_components + components +
        y_dc_table + y_ac_table + uv_dc_table + uv_ac_table +
        SOS + sos_length + num_sos_components + sos_components + start_spectral + end_spectral + approx_high +
        encoded_bytes +
        EOI
    )

    return header
