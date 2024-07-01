import itertools

def Huffman_coding(Y_DC_data,U_DC_data,V_DC_data,Y_AC_data,U_AC_data,V_AC_data):
    # DC 亮度表
    dc_luminance = {
        0: '00', 1: '010', 2: '011', 3: '100', 4: '101', 5: '110',
        6: '1110', 7: '11110', 8: '111110', 9: '1111110', 10: '11111110', 11: '111111110'
    }

    # DC 色度表
    dc_chrominance = {
        0: '00', 1: '01', 2: '10', 3: '110', 4: '1110', 5: '11110',
        6: '111110', 7: '1111110', 8: '11111110', 9: '111111110', 10: '1111111110', 11: '11111111110'
    }

    # AC 亮度表
    ac_luminance = {
        (0, 0): '1010',  # EOB
        (0, 1): '00', (0, 2): '01', (0, 3): '100', (0, 4): '1011', (0, 5): '11010',
        (0, 6): '1111000', (0, 7): '11111000', (0, 8): '1111110110', (0, 9): '1111111110000010', (0, 10): '1111111110000011',
        (1, 1): '1100', (1, 2): '11011', (1, 3): '1111001', (1, 4): '111110110', (1, 5): '11111110110',
        (1, 6): '1111111110000100', (1, 7): '1111111110000101', (1, 8): '1111111110000110', (1, 9): '1111111110000111', (1, 10): '1111111110001000',
        (2, 1): '11100', (2, 2): '11111001', (2, 3): '1111110111', (2, 4): '111111110100', (2, 5): '1111111110001001',
        (2, 6): '1111111110001010', (2, 7): '1111111110001011', (2, 8): '1111111110001100', (2, 9): '1111111110001101', (2, 10): '1111111110001110',
        (3, 1): '111010', (3, 2): '111110111', (3, 3): '111111110101', (3, 4): '1111111110001111', (3, 5): '1111111110010000',
        (3, 6): '1111111110010001', (3, 7): '1111111110010010', (3, 8): '1111111110010011', (3, 9): '1111111110010100', (3, 10): '1111111110010101',
        (4, 1): '111011', (4, 2): '1111111000', (4, 3): '1111111110010110', (4, 4): '1111111110010111', (4, 5): '1111111110011000',
        (4, 6): '1111111110011001', (4, 7): '1111111110011010', (4, 8): '1111111110011011', (4, 9): '1111111110011100', (4, 10): '1111111110011101',
        (5, 1): '1111010', (5, 2): '11111110111', (5, 3): '1111111110011110', (5, 4): '1111111110011111', (5, 5): '1111111110100000',
        (5, 6): '1111111110100001', (5, 7): '1111111110100010', (5, 8): '1111111110100011', (5, 9): '1111111110100100', (5, 10): '1111111110100101',
        (6, 1): '1111011', (6, 2): '111111110110', (6, 3): '1111111110100110', (6, 4): '1111111110100111', (6, 5): '1111111110101000',
        (6, 6): '1111111110101001', (6, 7): '1111111110101010', (6, 8): '1111111110101011', (6, 9): '1111111110101100', (6, 10): '1111111110101101',
        (7, 1): '11111010', (7, 2): '111111110111', (7, 3): '1111111110101110', (7, 4): '1111111110101111', (7, 5): '1111111110110000',
        (7, 6): '1111111110110001', (7, 7): '1111111110110010', (7, 8): '1111111110110011', (7, 9): '1111111110110100', (7, 10): '1111111110110101',
        (8, 1): '111111000', (8, 2): '111111111000000', (8, 3): '1111111110110110', (8, 4): '1111111110110111', (8, 5): '1111111110111000',
        (8, 6): '1111111110111001', (8, 7): '1111111110111010', (8, 8): '1111111110111011', (8, 9): '1111111110111100', (8, 10): '1111111110111101',
        (9, 1): '111111001', (9, 2): '1111111110111110', (9, 3): '1111111110111111', (9, 4): '1111111111000000', (9, 5): '1111111111000001',
        (9, 6): '1111111111000010', (9, 7): '1111111111000011', (9, 8): '1111111111000100', (9, 9): '1111111111000101', (9, 10): '1111111111000110',
        (10, 1): '111111010', (10, 2): '1111111111000111', (10, 3): '1111111111001000', (10, 4): '1111111111001001', (10, 5): '1111111111001010',
        (10, 6): '1111111111001011', (10, 7): '1111111111001100', (10, 8): '1111111111001101', (10, 9): '1111111111001110', (10, 10): '1111111111001111',
        (11, 1): '1111111001', (11, 2): '1111111111010000', (11, 3): '1111111111010001', (11, 4): '1111111111010010', (11, 5): '1111111111010011',
        (11, 6): '1111111111010100', (11, 7): '1111111111010101', (11, 8): '1111111111010110', (11, 9): '1111111111010111', (11, 10): '1111111111011000',
        (12, 1): '1111111010', (12, 2): '1111111111011001', (12, 3): '1111111111011010', (12, 4): '1111111111011011', (12, 5): '1111111111011100',
        (12, 6): '1111111111011101', (12, 7): '1111111111011110', (12, 8): '1111111111011111', (12, 9): '1111111111100000', (12, 10): '1111111111100001',
        (13, 1): '11111111000', (13, 2): '1111111111100010', (13, 3): '1111111111100011', (13, 4): '1111111111100100', (13, 5): '1111111111100101',
        (13, 6): '1111111111100110', (13, 7): '1111111111100111', (13, 8): '1111111111101000', (13, 9): '1111111111101001', (13, 10): '1111111111101010',
        (14, 1): '1111111111101011', (14, 2): '1111111111101100', (14, 3): '1111111111101101', (14, 4): '1111111111101110', (14, 5): '1111111111101111',
        (14, 6): '1111111111110000', (14, 7): '1111111111110001', (14, 8): '1111111111110010', (14, 9): '1111111111110011', (14, 10): '1111111111110100',
        (15, 0): '11111111001',  # ZRL
        (15, 1): '1111111111110101', (15, 2): '1111111111110110', (15, 3): '1111111111110111', (15, 4): '1111111111111000', (15, 5): '1111111111111001',
        (15, 6): '1111111111111010', (15, 7): '1111111111111011', (15, 8): '1111111111111100', (15, 9): '1111111111111101', (15, 10): '1111111111111110'
    }

    # AC 色度表
    ac_chrominance = {
        (0, 0): '00',  # EOB
        (0, 1): '01', (0, 2): '100', (0, 3): '1010', (0, 4): '11000', 
        (0, 5): '11001', (0, 6): '111000', (0, 7): '1111000', (0, 8): '111110100', 
        (0, 9): '1111110110', (0, 10): '111111110100',
        (1, 1): '1011', (1, 2): '111001', (1, 3): '11110110', (1, 4): '111110101', 
        (1, 5): '11111110110', (1, 6): '111111110101', (1, 7): '1111111110001000', 
        (1, 8): '1111111110001001', (1, 9): '1111111110001010', (1, 10): '1111111110001011',
        (2, 1): '11010', (2, 2): '11110111', (2, 3): '1111110111', (2, 4): '111111110110', 
        (2, 5): '111111111000010', (2, 6): '1111111110001100', (2, 7): '1111111110001101', 
        (2, 8): '1111111110001110', (2, 9): '1111111110001111', (2, 10): '1111111110010000',
        (3, 1): '11011', (3, 2): '11111000', (3, 3): '1111111000', (3, 4): '111111110111', 
        (3, 5): '1111111110010001', (3, 6): '1111111110010010', (3, 7): '1111111110010011', 
        (3, 8): '1111111110010100', (3, 9): '1111111110010101', (3, 10): '1111111110010110',
        (4, 1): '111010', (4, 2): '111110110', (4, 3): '1111111110010111', 
        (4, 4): '1111111110011000', (4, 5): '1111111110011001', (4, 6): '1111111110011010', 
        (4, 7): '1111111110011011', (4, 8): '1111111110011100', (4, 9): '1111111110011101', 
        (4, 10): '1111111110011110',
        (5, 1): '111011', (5, 2): '1111111001', (5, 3): '1111111110011111', 
        (5, 4): '1111111110100000', (5, 5): '1111111110100001', (5, 6): '1111111110100010', 
        (5, 7): '1111111110100011', (5, 8): '1111111110100100', (5, 9): '1111111110100101', 
        (5, 10): '1111111110100110',
        (6, 1): '1111001', (6, 2): '11111110111', (6, 3): '1111111110100111', 
        (6, 4): '1111111110101000', (6, 5): '1111111110101001', (6, 6): '1111111110101010', 
        (6, 7): '1111111110101011', (6, 8): '1111111110101100', (6, 9): '1111111110101101', 
        (6, 10): '1111111110101110',
        (7, 1): '1111010', (7, 2): '11111111000', (7, 3): '1111111110101111', 
        (7, 4): '1111111110110000', (7, 5): '1111111110110001', (7, 6): '1111111110110010', 
        (7, 7): '1111111110110011', (7, 8): '1111111110110100', (7, 9): '1111111110110101', 
        (7, 10): '1111111110110110',
        (8, 1): '11111001', (8, 2): '1111111110110111', (8, 3): '1111111110111000', 
        (8, 4): '1111111110111001', (8, 5): '1111111110111010', (8, 6): '1111111110111011', 
        (8, 7): '1111111110111100', (8, 8): '1111111110111101', (8, 9): '1111111110111110', 
        (8, 10): '1111111110111111',
        (9, 1): '111110111', (9, 2): '1111111111000000', (9, 3): '1111111111000001', 
        (9, 4): '1111111111000010', (9, 5): '1111111111000011', (9, 6): '1111111111000100', 
        (9, 7): '1111111111000101', (9, 8): '1111111111000110', (9, 9): '1111111111000111', 
        (9, 10): '1111111111001000',
        (10, 1): '111111000', (10, 2): '1111111111001001', (10, 3): '1111111111001010', 
        (10, 4): '1111111111001011', (10, 5): '1111111111001100', (10, 6): '1111111111001101', 
        (10, 7): '1111111111001110', (10, 8): '1111111111001111', (10, 9): '1111111111010000', 
        (10, 10): '1111111111010001',
        (11, 1): '111111001', (11, 2): '1111111111010010', (11, 3): '1111111111010011', 
        (11, 4): '1111111111010100', (11, 5): '1111111111010101', (11, 6): '1111111111010110', 
        (11, 7): '1111111111010111', (11, 8): '1111111111011000', (11, 9): '1111111111011001', 
        (11, 10): '1111111111011010',
        (12, 1): '111111010', (12, 2): '1111111111011011', (12, 3): '1111111111011100', 
        (12, 4): '1111111111011101', (12, 5): '1111111111011110', (12, 6): '1111111111011111', 
        (12, 7): '1111111111100000', (12, 8): '1111111111100001', (12, 9): '1111111111100010', 
        (12, 10): '1111111111100011',
        (13, 1): '11111111001', (13, 2): '1111111111100100', (13, 3): '1111111111100101', 
        (13, 4): '1111111111100110', (13, 5): '1111111111100111', (13, 6): '1111111111101000', 
        (13, 7): '1111111111101001', (13, 8): '1111111111101010', (13, 9): '1111111111101011', 
        (13, 10): '1111111111101100',
        (14, 1): '11111111100000', (14, 2): '1111111111101101', (14, 3): '1111111111101110', 
        (14, 4): '1111111111101111', (14, 5): '1111111111110000', (14, 6): '1111111111110001', 
        (14, 7): '1111111111110010', (14, 8): '1111111111110011', (14, 9): '1111111111110100', 
        (14, 10): '1111111111110101',
        (15, 0): '1111111010',  # ZRL
        (15, 1): '111111111000011', (15, 2): '1111111111110110', (15, 3): '1111111111110111', 
        (15, 4): '1111111111111000', (15, 5): '1111111111111001', (15, 6): '1111111111111010', 
        (15, 7): '1111111111111011', (15, 8): '1111111111111100', (15, 9): '1111111111111101', 
        (15, 10): '1111111111111110'
    }

    def huffman_encode_dc(value, table):
        if value == 0:
            category = 0
            additional_bits = ''
        else:
            category = len(bin(abs(value))[2:])
            additional_bits = bin(value & (2**category - 1))[2:].zfill(category)
        huffman_code = table.get(category, '')
        return huffman_code + additional_bits

    def huffman_encode_ac(values, table):
        result = []
        for run_length, size in values:
            if (run_length, size) == (0, 0):
                result.append(table.get((0, 0), ''))  # EOB
                break
            result.append(table.get((run_length, size), ''))
        return ''.join(result)

    def bits_to_bytes(bits):
        b = bytearray()
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                byte = byte.ljust(8, '0')  # 填充0
            b.append(int(byte, 2))
        return bytes(b)

    def diff_encode(dc_data):
        diff_data = [dc_data[0]]
        for i in range(1, len(dc_data)):
            diff_data.append(dc_data[i] - dc_data[i-1])
        return diff_data

    # # 示例数据
    # Y_AC_data = [[[3, 1], [2, 5], [1, 0]], [[1, 2], [0, 0]]]
    # U_AC_data = [[[2, 3], [3, 4], [1, 0]], [[1, 1], [0, 0]]]
    # V_AC_data = [[[1, 4], [2, 3], [1, 0]], [[1, 5], [0, 0]]]

    # Y_DC_data = [23, -2, 3, 0, 0, -1, 5]
    # U_DC_data = [5, -1, 2, 1, 0, 0, 3]
    # V_DC_data = [3, 1, -1, 2, 0, 0, -2]

    # 差分编码
    Y_DC_diff = diff_encode(Y_DC_data)
    U_DC_diff = diff_encode(U_DC_data)
    V_DC_diff = diff_encode(V_DC_data)

    # DC 数据的霍夫曼编码
    encoded_dc_bits_Y = ''.join(huffman_encode_dc(value, dc_luminance) for value in Y_DC_diff)
    encoded_dc_bits_U = ''.join(huffman_encode_dc(value, dc_chrominance) for value in U_DC_diff)
    encoded_dc_bits_V = ''.join(huffman_encode_dc(value, dc_chrominance) for value in V_DC_diff)

    # AC 数据的霍夫曼编码
    encoded_ac_bits_Y = ''.join(huffman_encode_ac(values, ac_luminance) for values in Y_AC_data)
    encoded_ac_bits_U = ''.join(huffman_encode_ac(values, ac_chrominance) for values in U_AC_data)
    encoded_ac_bits_V = ''.join(huffman_encode_ac(values, ac_chrominance) for values in V_AC_data)

    # 将比特流转换为字节串
    encoded_bytes_Y_DC = bits_to_bytes(encoded_dc_bits_Y)
    encoded_bytes_U_DC = bits_to_bytes(encoded_dc_bits_U)
    encoded_bytes_V_DC = bits_to_bytes(encoded_dc_bits_V)

    encoded_bytes_Y_AC = bits_to_bytes(encoded_ac_bits_Y)
    encoded_bytes_U_AC = bits_to_bytes(encoded_ac_bits_U)
    encoded_bytes_V_AC = bits_to_bytes(encoded_ac_bits_V)

    # 输出结果
    print("Y DC:", encoded_bytes_Y_DC)
    print("U DC:", encoded_bytes_U_DC)
    print("V DC:", encoded_bytes_V_DC)
    print("Y AC:", encoded_bytes_Y_AC)
    print("U AC:", encoded_bytes_U_AC)
    print("V AC:", encoded_bytes_V_AC)

    Y_AC_codebook_bytes = b'\xff\xc4\x00H\x10\x00\x02\x01\x02\x04\x04\x03\x06\x04\x05\x01\x07\x03\x02\x06\x03\x01\x02\x03\x04\x11\x00\x05\x12!\x06\x131A"Qa\x07\x142q\x81\x91#B\xa1\xb1\x15R\xc1\xd1\xf0$\x08\x163br\xe1\xf14C\x82\x92\xb2\x17%Sc\xa2\xc2Ds\x83'
    UV_AC_codebook_bytes = b'\xff\xc4\x009\x11\x00\x01\x04\x01\x03\x02\x03\x07\x04\x02\x03\x00\x02\x01\x05\x00\x01\x00\x02\x03\x11!\x04\x121AQ\x13a\xf0\x05"q\x81\x91\xa1\xb1\x142\xc1\xd1\xe1\xf1\x06#B3R\x15$%Cbr'
    Y_DC_codebook_bytes = b'\xff\xc4\x00\x1d\x00\x00\x02\x02\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x05\x03\x06\x01\x02\x07\x00\x08\t'
    UV_DC_codebook_bytes = b'\xff\xc4\x00\x1b\x01\x00\x02\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03\x00\x01\x04\x05\x06\x07'

    return Y_AC_codebook_bytes,UV_AC_codebook_bytes,Y_DC_codebook_bytes,UV_DC_codebook_bytes,encoded_bytes_Y_DC,encoded_bytes_U_DC,encoded_bytes_V_DC,encoded_bytes_Y_AC,encoded_bytes_U_AC,encoded_bytes_V_AC
