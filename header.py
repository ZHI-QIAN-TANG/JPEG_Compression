def generate_jpeg_header(width, height):
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
    q_table_Y = bytes([
        16, 11, 10, 16, 24, 41, 51, 61,
        12, 12, 14, 19, 26, 58, 60, 55,
        14, 13, 16, 24, 40, 67, 69, 56,
        14, 17, 22, 29, 51, 87, 80, 62,
        18, 22, 37, 56, 68, 109, 103, 77,
        24, 35, 55, 64, 81, 104, 113, 92,
        49, 64, 78, 87, 103, 121, 120, 101,
        72, 92, 95, 98, 112, 100, 103, 99])

    # Define Quantization Table for Cb, Cr
    DQT_C = b'\xFF\xDB'  # Define Quantization Table
    dqt_length_C = b'\x00\x43'  # 段長度
    dqt_info_C = b'\x01'  # 表信息
    q_table_C = bytes([
        17, 18, 24, 47, 99, 99, 99, 99,
        18, 21, 26, 66, 99, 99, 99, 99,
        24, 26, 56, 99, 99, 99, 99, 99,
        47, 66, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99,
        99, 99, 99, 99, 99, 99, 99, 99])

    DHT_dc = b'\xFF\xC4'  # Define Huffman Table
    dht_dc_length = b'\x00\x1F'  # 段長度
    dht_dc_info = b'\x00'  # 表信息
    huffman_table_dc = bytes.fromhex('001f0000010501010101010100000000000000808182838485868788898a8b')
    
    DHT_ac = b'\xFF\xC4' 
    dht_ac_length = b'\x00\xB5' 
    dht_ac_info = b'\x10'
    huffman_table_ac = bytes.fromhex('00281001010101000300020202020204000000808f817f7e82837d847c8586877a7b898a79888b8d')
    
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
        SOF0 + sof_length + precision + height_bytes + width_bytes + num_components + components +
        DQT_Y + dqt_length_Y + dqt_info_Y + q_table_Y +
        DQT_C + dqt_length_C + dqt_info_C + q_table_C +
        DHT_dc + dht_dc_length + dht_dc_info + huffman_table_dc +
        DHT_ac + dht_ac_length + dht_ac_info + huffman_table_ac +
        SOS + sos_length + num_sos_components + sos_components + start_spectral + end_spectral + approx_high +
        EOI
    )

    return header

def save_jpeg_header(filename, width, height):
    header = generate_jpeg_header(width, height)
    with open(filename, 'wb') as f:
        f.write(header)
    return header

# 用例
#print(save_jpeg_header('headertmp.jpg', 400, 600))