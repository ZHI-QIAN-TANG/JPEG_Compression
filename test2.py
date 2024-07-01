import struct
from bitstring import BitStream, BitArray

# 解析霍夫曼表
def parse_huffman_table(data):
    stream = BitStream(data)
    lengths = [stream.read('uint:8') for _ in range(16)]
    symbols = []
    for length in lengths:
        symbols.extend([stream.read('uint:8') for _ in range(length)])
    return lengths, symbols

# 构建霍夫曼表
def build_huffman_table(lengths, symbols):
    huffman_table = {}
    code = 0
    code_length = 1
    symbol_index = 0

    for length in lengths:
        for _ in range(length):
            huffman_table[symbols[symbol_index]] = BitArray(uint=code, length=code_length)
            code += 1
            symbol_index += 1
        code <<= 1
        code_length += 1

    return huffman_table

# 使用霍夫曼表进行编码
def huffman_encode(value, huffman_table):
    return huffman_table[value]

# 计算DC系数的差分值并进行霍夫曼编码
def encode_dc_coefficients(data, huffman_table):
    encoded_data = BitArray()
    previous_value = 0
    for value in data:
        diff = value - previous_value
        size_category = get_size_category(diff)
        encoded_data.append(huffman_encode(size_category, huffman_table))
        if size_category > 0:
            encoded_data.append(encode_value(diff, size_category))
        previous_value = value
    return encoded_data

# 根据差分值计算大小类别
def get_size_category(value):
    if value == 0:
        return 0
    abs_value = abs(value)
    bits = abs_value.bit_length()
    return bits

# 编码差分值
def encode_value(value, size_category):
    if value >= 0:
        return BitArray(uint=value, length=size_category)
    else:
        max_positive_value = (1 << size_category) - 1
        return BitArray(int=value, length=size_category) & BitArray(uint=max_positive_value, length=size_category)

# 霍夫曼表数据
Y_AC_codebook_bytes = b'\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
UV_AC_codebook_bytes = b'\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
Y_DC_codebook_bytes = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
UV_DC_codebook_bytes = b'\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
    
# 解析霍夫曼表
Y_AC_lengths, Y_AC_symbols = parse_huffman_table(Y_AC_codebook_bytes[5:])
UV_AC_lengths, UV_AC_symbols = parse_huffman_table(UV_AC_codebook_bytes[5:])
Y_DC_lengths, Y_DC_symbols = parse_huffman_table(Y_DC_codebook_bytes[5:])
UV_DC_lengths, UV_DC_symbols = parse_huffman_table(UV_DC_codebook_bytes[5:])

# 构建霍夫曼表
Y_AC_table = build_huffman_table(Y_AC_lengths, Y_AC_symbols)
UV_AC_table = build_huffman_table(UV_AC_lengths, UV_AC_symbols)
Y_DC_table = build_huffman_table(Y_DC_lengths, Y_DC_symbols)
UV_DC_table = build_huffman_table(UV_DC_lengths, UV_DC_symbols)

# 参考数据
Y_AC_data = [[[3, 1], [2, 5], [0, 0]], [[1, 2], [0, 0]]]
U_AC_data = [[[2, 3], [3, 4], [0, 0]], [[1, 1], [0, 0]]]
V_AC_data = [[[1, 4], [2, 3], [0, 0]], [[1, 5], [0, 0]]]
Y_DC_data = [23, -2, 3, 0, 0, -1, 5]
U_DC_data = [5, -1, 2, 1, 0, 0, 3]
V_DC_data = [3, 1, -1, 2, 0, 0, -2]

# 将参考数据进行编码
Y_AC_encoded = BitArray()
for block in Y_AC_data:
    for value_pair in block:
        for value in value_pair:
            Y_AC_encoded.append(huffman_encode(value, Y_AC_table))

U_AC_encoded = BitArray()
for block in U_AC_data:
    for value_pair in block:
        for value in value_pair:
            U_AC_encoded.append(huffman_encode(value, UV_AC_table))

V_AC_encoded = BitArray()
for block in V_AC_data:
    for value_pair in block:
        for value in value_pair:
            V_AC_encoded.append(huffman_encode(value, UV_AC_table))

Y_DC_encoded = encode_dc_coefficients(Y_DC_data, Y_DC_table)
U_DC_encoded = encode_dc_coefficients(U_DC_data, UV_DC_table)
V_DC_encoded = encode_dc_coefficients(V_DC_data, UV_DC_table)

# 打印结果
print("Y_AC_encoded:", Y_AC_encoded.tobytes())
print("U_AC_encoded:", U_AC_encoded.tobytes())
print("V_AC_encoded:", V_AC_encoded.tobytes())
print("Y_DC_encoded:", Y_DC_encoded.tobytes())
print("U_DC_encoded:", U_DC_encoded.tobytes())
print("V_DC_encoded:", V_DC_encoded.tobytes())
