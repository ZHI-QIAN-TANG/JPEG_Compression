import pickle
import Huffman_coding_cf
import Zigzag as z

def generate_jpeg_header(width, height, Y_AC_codebook_bytes,UV_AC_codebook_bytes,Y_DC_codebook_bytes,UV_DC_codebook_bytes,encoded_bytes_Y_DC,encoded_bytes_U_DC,encoded_bytes_V_DC,encoded_bytes_Y_AC,encoded_bytes_U_AC,encoded_bytes_V_AC,encoded_bytes):
    # JPEG標頭常量部分
    SOI = b'\xFF\xD8'  # Start of Image
    APP0 = b'\xFF\xE0'  # Application Marker
    JFIF = b'JFIF\x00'  # JFIF標識符
    length = b'\x00\x10'  # APP0段長度
    version = b'\x01\x01'  # JFIF版本
    units = b'\x01'  # 密度單位（0：無單位，1：每英寸，2：每厘米）
    x_density = b'\x00\x78'  # X方向密度
    y_density = b'\x00\x78'  # Y方向密度
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

    # Define Quantization Table for Cb, Cr
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
 
    def generate_dht_segment(huffman_data, table_class, table_id):
        # Prepare DHT segment header
        segment = b'\xFF\xC4'
        segment_length = 2 + 1 + len(huffman_data)
        segment += segment_length.to_bytes(2, byteorder='big')
        # Table class (0 for DC, 1 for AC) and Huffman table index
        table_class_index = (table_class << 4) | table_id
        segment += bytes([table_class_index])
        return segment 
    y_dc_table = Y_DC_codebook_bytes
    y_ac_table = Y_AC_codebook_bytes
    uv_dc_table = UV_DC_codebook_bytes
    uv_ac_table = UV_AC_codebook_bytes
    #u_dc_table = generate_dht_segment(UV_DC_codebook_bytes, table_class=0, table_id=1)
    #u_ac_table = generate_dht_segment(UV_AC_codebook_bytes, table_class=1, table_id=1)
    #v_dc_table = generate_dht_segment(UV_DC_codebook_bytes, table_class=0, table_id=2)
    #v_ac_table = generate_dht_segment(UV_AC_codebook_bytes, table_class=1, table_id=2)
    '''
    print("1:",y_dc_table,"\n")
    print("1:",y_ac_table,"\n")
    print("1:",u_ac_table,"\n")
    print("1:",u_ac_table,"\n")
    print("1:",v_dc_table,"\n")
    print("1:",v_ac_table,"\n")
    '''
    # 定義SOS段（Start Of Scan）
    SOS = b'\xFF\xDA'
    sos_length = b'\x00\x0C'  # 段長度 or 0E
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
    print("EOI = ",EOI)

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
        # encoded_bytes_Y_DC + encoded_bytes_Y_AC + encoded_bytes_U_DC + encoded_bytes_U_AC + encoded_bytes_V_DC + encoded_bytes_V_AC + 
        EOI
    )

    return header



# 用例
#print(save_jpeg_header('headertmp.jpg', 600, 400,dc_jpeg_header, ac_jpeg_header, dc_merged_encoded_data, ac_merged_encoded_data))
