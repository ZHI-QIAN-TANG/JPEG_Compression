import numpy as np
from bitstring import BitStream, ReadError
from heapq import heappush, heappop, heapify
from collections import Counter

# 定义节点类
class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

# 建立霍夫曼树
def build_huffman_tree(huffman_table):
    root = Node()
    for value, code in huffman_table.items():
        current_node = root
        for bit in code:
            if bit == '0':
                if current_node.left is None:
                    current_node.left = Node()
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = Node()
                current_node = current_node.right
        current_node.value = value
    return root

# DC霍夫曼表
dc_huffman_table = {
    0: '00', 1: '010', 2: '011', 3: '100', 4: '101', 5: '110',
    6: '1110', 7: '11110', 8: '111110', 9: '1111110', 10: '11111110', 11: '111111110'
}

# 建立霍夫曼表
def create_huffman_table(data):
    frequencies = Counter(data)
    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# 编码霍夫曼表
def huffman_encode(data):
    huffman_table = create_huffman_table(data)
    huffman_dict = {symbol: code for symbol, code in huffman_table}
    encoded_data = ''.join(huffman_dict[symbol] for symbol in data)
    return encoded_data, huffman_dict

# 转换霍夫曼表为JPEG DHT格式
def huffman_table_to_dht(huffman_dict):
    dht_table = [0] * 16
    symbol_list = []

    for symbol, code in huffman_dict.items():
        length = len(code)
        dht_table[length - 1] += 1
        symbol_list.append(symbol)

    dht_segment = dht_table + symbol_list
    return dht_segment

# 用于解码
def decode_huffman_code(bitstream, root):
    current_node = root
    while current_node.value is None:
        bit = bitstream.read('bin:1')
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
    return current_node.value

# DC和AC的霍夫曼编码函数
def Huffman_code(DC, AC):
    # DC部分
    def encode_dc_coefficient(dc_coeff):
        dc_coeff = int(dc_coeff)
        magnitude = abs(dc_coeff)
        size = magnitude.bit_length()
        huffman_code = dc_huffman_table[size]
        if dc_coeff < 0:
            magnitude = (1 << size) - 1 + dc_coeff
        magnitude_bin = bin(magnitude)[2:].zfill(size)
        return huffman_code + magnitude_bin

    dc_coefficients = DC
    encoded_dc_coeffs = [encode_dc_coefficient(coeff) for coeff in dc_coefficients]
    encoded_dc_bitstream = ''.join(encoded_dc_coeffs)

    dc_huffman_tree = build_huffman_tree(dc_huffman_table)

    def decode_dc_coefficient(bitstream, huffman_tree):
        size = decode_huffman_code(bitstream, huffman_tree)
        if size == 0:
            return 0
        try:
            magnitude_bin = bitstream.read('bin:' + str(size))
        except ReadError as e:
            print("Error reading magnitude:", e)
            return None
        magnitude = int(magnitude_bin, 2)
        if magnitude < (1 << (size - 1)):
            magnitude -= (1 << size) - 1
        return magnitude

    bitstream = BitStream(bin=encoded_dc_bitstream)
    decoded_dc_coeffs = []
    while bitstream.pos < bitstream.len and len(decoded_dc_coeffs) < len(dc_coefficients):
        try:
            decoded_dc_coeff = decode_dc_coefficient(bitstream, dc_huffman_tree)
            if decoded_dc_coeff is None:
                break
            decoded_dc_coeffs.append(decoded_dc_coeff)
        except ValueError as e:
            print("Error decoding DC coefficient:", e)
            break

    # AC部分
    flat_ac_data = []
    for segment in AC:
        for count, value in segment:
            flat_ac_data.append(count)
            flat_ac_data.append(value)

    huffman_encoded_data, ac_huffman_dict = huffman_encode(flat_ac_data)

    ac_huffman_tree = build_huffman_tree(ac_huffman_dict)

    # 构建DHT段
    dc_dht_segment = huffman_table_to_dht(dc_huffman_table)
    ac_dht_segment = huffman_table_to_dht(ac_huffman_dict)

    return dc_dht_segment, ac_dht_segment, dc_huffman_tree, ac_huffman_tree

# 示例DC和AC数据
DC = [3, -1, 0, 2, -3]
AC = [
    [(0, 2), (1, 1), (0, 0)],
    [(0, 3), (1, -1), (0, 0)]
]

dc_dht_segment, ac_dht_segment, dc_huffman_tree, ac_huffman_tree = Huffman_code(DC, AC)

print("DC DHT Segment:", dc_dht_segment)
print("AC DHT Segment:", ac_dht_segment)
