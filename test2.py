from collections import defaultdict

# 霍夫曼編碼表
dc_luminance = {0: '00', 1: '010', 2: '011', 3: '100', 4: '101', 5: '110', 6: '1110', 7: '11110', 8: '111110', 9: '1111110', 10: '11111110', 11: '111111110'}
dc_chrominance = {0: '00', 1: '01', 2: '10', 3: '110', 4: '1110', 5: '11110', 6: '111110', 7: '1111110', 8: '11111110', 9: '111111110', 10: '1111111110', 11: '11111111110'}
ac_luminance = {(0, 0): '1010', (0, 1): '00', (0, 2): '01', (0, 3): '100', (0, 4): '1011', (0, 5): '11010', (0, 6): '1111000', (0, 7): '11111000', (0, 8): '1111110110', (0, 9): '1111111110000010', (0, 10): '1111111110000011', (1, 1): '1100', (1, 2): '11011', (1, 3): '1111001', (1, 4): '111110110', (1, 5): '11111110110', (1, 6): '1111111110000100', (1, 7): '1111111110000101', (1, 8): '1111111110000110', (1, 9): '1111111110000111', (1, 10): '1111111110001000', (2, 1): '11100', (2, 2): '11111001', (2, 3): '1111110111', (2, 4): '111111110100', (2, 5): '1111111110001001', (2, 6): '1111111110001010', (2, 7): '1111111110001011', (2, 8): '1111111110001100', (2, 9): '1111111110001101', (2, 10): '1111111110001110', (3, 1): '111010', (3, 2): '111110111', (3, 3): '111111110101', (3, 4): '1111111110001111', (3, 5): '1111111110010000', (3, 6): '1111111110010001', (3, 7): '1111111110010010', (3, 8): '1111111110010011', (3, 9): '1111111110010100', (3, 10): '1111111110010101', (4, 1): '111011', (4, 2): '1111111000', (4, 3): '1111111110010110', (4, 4): '1111111110010111', (4, 5): '1111111110011000', (4, 6): '1111111110011001', (4, 7): '1111111110011010', (4, 8): '1111111110011011', (4, 9): '1111111110011100', (4, 10): '1111111110011101', (15, 0): '11111111001'}
ac_chrominance = {(0, 0): '00', (0, 1): '01', (0, 2): '100', (0, 3): '1010', (0, 4): '11000', (0, 5): '11001', (0, 6): '111000', (0, 7): '1111000', (0, 8): '111110100', (0, 9): '1111110110', (0, 10): '111111110100', (1, 1): '1011', (1, 2): '111001', (1, 3): '11110110', (1, 4): '111110101', (1, 5): '11111110110', (1, 6): '111111110101', (1, 7): '1111111110001000', (1, 8): '1111111110001001', (1, 9): '1111111110001010', (1, 10): '1111111110001011', (2, 1): '11010', (2, 2): '11110111', (2, 3): '1111110111', (2, 4): '111111110110', (2, 5): '111111111000010', (2, 6): '1111111110001100', (2, 7): '1111111110001101', (2, 8): '1111111110001110', (2, 9): '1111111110001111', (2, 10): '1111111110010000', (3, 1): '11011', (3, 2): '11111000', (3, 3): '1111111000', (3, 4): '111111110111', (3, 5): '1111111110010001', (3, 6): '1111111110010010', (3, 7): '1111111110010011', (3, 8): '1111111110010100', (3, 9): '1111111110010101', (3, 10): '1111111110010110', (15, 0): '1111111010'}

# 參考數據
Y_AC_data = [[[0, -2], [0, 9], [2, 1], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, -1], [0, 10], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, -2], [2, -1], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, 1], [0, 2], [0, -1], [4, -1], [15, 0], [15, 0], [15, 0], [0, 0]]]
U_AC_data = [[[1, -1], [15, 0], [15, 0], [15, 0], [0, 0]], [[1, -2], [15, 0], [15, 0], [15, 0], [0, 0]], [[15, 0], [15, 0], [15, 0], [0, 0]], [[15, 0], [15, 0], [15, 0], [0, 0]]]
V_AC_data = [[[1, 3], [15, 0], [15, 0], [15, 0], [0, 0]], [[1, 2], [15, 0], [15, 0], [15, 0], [0, 0]], [[15, 0], [15, 0], [15, 0], [0, 0]], [[15, 0], [15, 0], [15, 0], [0, 0]]]
Y_DC_data = [77, 9, -19, 3]
U_DC_data = [71, -2, 5, -1]
V_DC_data = [44, 4, -11, 3]

def encode_dc(data, table):
    encoded = ""
    prev = 0
    for value in data:
        diff = value - prev
        prev = value
        category = len(bin(abs(diff))[2:]) if diff != 0 else 0
        encoded += table[category]
        if diff > 0:
            encoded += bin(diff)[2:].zfill(category)
        elif diff < 0:
            encoded += bin(abs(diff) - 1)[2:].zfill(category).replace('0', 'x').replace('1', '0').replace('x', '1')
    return encoded

def encode_ac(data, table):
    encoded = ""
    for block in data:
        zero_count = 0
        for run, value in block:
            if run == 15 and value == 0:
                encoded += table[(15, 0)]
                zero_count = 0
            elif value == 0:
                zero_count += run
            else:
                while zero_count > 15:
                    encoded += table[(15, 0)]
                    zero_count -= 16
                category = len(bin(abs(value))[2:])
                encoded += table[(zero_count, category)]
                if value > 0:
                    encoded += bin(value)[2:].zfill(category)
                else:
                    encoded += bin(abs(value) - 1)[2:].zfill(category).replace('0', 'x').replace('1', '0').replace('x', '1')
                zero_count = 0
        if block[-1] != [0, 0]:
            encoded += table[(0, 0)]
    return encoded

def bitstring_to_bytes(s):
    return bytes(int(s[i:i+8], 2) for i in range(0, len(s), 8))

# 編碼 DC 數據
encoded_Y_DC = encode_dc(Y_DC_data, dc_luminance)
encoded_U_DC = encode_dc(U_DC_data, dc_chrominance)
encoded_V_DC = encode_dc(V_DC_data, dc_chrominance)

# 編碼 AC 數據
encoded_Y_AC = encode_ac(Y_AC_data, ac_luminance)
encoded_U_AC = encode_ac(U_AC_data, ac_chrominance)
encoded_V_AC = encode_ac(V_AC_data, ac_chrominance)

# 轉換為字節並打印
encoded_bytes_Y_DC = bitstring_to_bytes(encoded_Y_DC)
encoded_bytes_U_DC = bitstring_to_bytes(encoded_U_DC)
encoded_bytes_V_DC = bitstring_to_bytes(encoded_V_DC)
encoded_bytes_Y_AC = bitstring_to_bytes(encoded_Y_AC)
encoded_bytes_U_AC = bitstring_to_bytes(encoded_U_AC)
encoded_bytes_V_AC = bitstring_to_bytes(encoded_V_AC)

print("encoded_bytes_Y_DC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_Y_DC))
print("encoded_bytes_U_DC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_U_DC))
print("encoded_bytes_V_DC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_V_DC))
print("encoded_bytes_Y_AC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_Y_AC))
print("encoded_bytes_U_AC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_U_AC))
print("encoded_bytes_V_AC:", ''.join('\\x{:02x}'.format(b) for b in encoded_bytes_V_AC))