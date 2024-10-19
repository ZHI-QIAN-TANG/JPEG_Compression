'''
def binary_to_bytes(binary_str):
    # Ensure the binary string length is a multiple of 8
    if len(binary_str) % 8 != 0:
        raise ValueError("The binary string length must be a multiple of 8.")

    # Convert the binary string to an integer
    integer_value = int(binary_str, 2)

    # Calculate the number of bytes needed
    num_bytes = len(binary_str) // 8

    # Convert the integer to a bytes object
    byte_array = integer_value.to_bytes(num_bytes, byteorder='big')

    return byte_array

# Example usage
binary_str = "00000001"
byte_array = binary_to_bytes(binary_str)
print(byte_array)  # Output: b'\xc9\x96'
'''
""" 
hex_string = '001f0000010501010101010100000000000000808182838485868788898a8b'
'00281001010101000300020202020204000000808f817f7e82837d847c8586877a7b898a79888b8d'

# 將十六進制字符串轉換為字節串
byte_string = bytes.fromhex(hex_string)

# 轉換為類似的格式
formatted_string = str(byte_string)

print(byte_string)
 """
'''
def binary_to_hex(binary_str):
        # 補零，使二進制字符串長度為8的倍數
    while len(binary_str) % 8 != 0:
        binary_str = '0' + binary_str
    
    # 將二進制字符串轉換為十六進制字符串
    hex_str = hex(int(binary_str, 2))[2:].upper()
    
    # 確保十六進制字符串的長度是偶數
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    hex_bytes = bytes.fromhex(hex_str)
    return hex_bytes

# 示例二進制字符串
binary_str = ""
result_bytes = binary_to_hex(binary_str)
print(result_bytes)
'''
'''
import Huffman_coding_ac as Ha
import Huffman_coding_dc as Hd
import pickle
import struct

def generate_dht_segment(hex_data, table_class, table_id):
    # 解序列化十六進制位元流
    huffman_dict = pickle.loads(hex_data)

    # 構建位長分佈和符號值
    lengths = [0] * 16
    symbol_to_code = {}

    # 構建symbol_to_code
    for key, code in huffman_dict.items():
        symbol_to_code[key] = code

    # 計算每個長度的符號數量
    for code in symbol_to_code.values():
        length = len(code)
        lengths[length - 1] += 1

    # 構建符號值（根據碼長度排序）
    symbols = sorted(symbol_to_code.keys(), key=lambda x: len(symbol_to_code[x]))

    # 構建DHT段
    dht_segment = bytearray()
    dht_segment.extend(struct.pack('>H', 0xFFC4))  # DHT段標記
    dht_segment.extend(struct.pack('>H', 3 + 16 + len(symbols)))  # 段長度

    # 表類型
    table_info = (table_class << 4) | table_id
    dht_segment.append(table_info)  # 表信息

    dht_segment.extend(lengths)  # 位長分佈

    for symbol in symbols:
        if isinstance(symbol, tuple):
            for part in symbol:
                dht_segment.append(part & 0xFF)  # 確保符號是單字節
        else:
            dht_segment.append(symbol & 0xFF)  # 確保符號是單字節

    return bytes(dht_segment) 

x = b'\x80\x04\x95\xba\x00\x00\x00\x00\x00\x00\x00}\x94(K\x02K\x05\x86\x94\x8c\x0200\x94K\x01K\x02\x86\x94\x8c\x0201\x94K\x00K\x00\x86\x94\x8c\x0210\x94K\x01K\x00\x86\x94\x8c\x03110\x94K\x03K\x01\x86\x94\x8c\x03111\x94K\x03K\x04\x86\x94\x8c\x0200\x94K\x01K\x01\x86\x94\x8c\x0201\x94K\x02K\x03\x86\x94\x8c\x0200\x94K\x01K\x05\x86\x94\x8c\x0201\x94K\x01K\x04\x86\x94\x8c\x03111\x94J\xff\xff\xff\xff\x8c\x03101\x94K\x05\x8c\x03110\x94K\x03\x8c\x03110\x94K\x00\x8c\x0201\x94K\x17\x8c\x03110\x94J\xfe\xff\xff\xff\x8c\x03100\x94K\x02\x8c\x03111\x94K\x01\x8c\x0200\x94u.'
y = b'\x80\x04\x95\xba\x00\x00\x00\x00\x00\x00\x00}\x94(K\x02K\x05\x86\x94\x8c\x0200\x94K\x01K\x02\x86\x94\x8c\x0201\x94K\x00K\x00\x86\x94\x8c\x0210\x94K\x01K\x00\x86\x94\x8c\x03110\x94K\x03K\x01\x86\x94\x8c\x03111\x94K\x03K\x04\x86\x94\x8c\x0200\x94K\x01K\x01\x86\x94\x8c\x0201\x94K\x02K\x03\x86\x94\x8c\x0200\x94K\x01K\x05\x86\x94\x8c\x0201\x94K\x01K\x04\x86\x94\x8c\x03111\x94J\xff\xff\xff\xff\x8c\x03101\x94K\x05\x8c\x03110\x94K\x03\x8c\x03110\x94K\x00\x8c\x0201\x94K\x17\x8c\x03110\x94J\xfe\xff\xff\xff\x8c\x03100\x94K\x02\x8c\x03111\x94K\x01\x8c\x0200\x94u.'
print(generate_dht_segment(x, table_class=0, table_id=0))

print(generate_dht_segment(y, table_class=0, table_id=0))
'''
import numpy as np

# 測試
src = np.random.randint(-128, 127, (3, 3)) # 假設 src 是隨機生成的 8x8 矩陣
print("輸入矩陣:\n", src)
a =  [[ -44, -47,-119],
    [-125 , 108 , -53],
 [ -11  , 81 , 107]]

for i in range(len(a)):
    print("----------")
    print(a[i][:])



