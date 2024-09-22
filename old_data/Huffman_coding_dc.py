import numpy as np
from bitstring import BitStream, ReadError

def Huffman_code(Y_data, U_data, V_data):
    def Huffman_code(DC):
        DC = np.array(DC, dtype=np.int32)

        class Node:
            def __init__(self, value=None):
                self.value = value
                self.left = None
                self.right = None

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

        def decode_huffman_code(bitstream, root):
            current_node = root
            while current_node.value is None:
                bit = bitstream.read('bin:1')
                if bit == '0':
                    current_node = current_node.left
                else:
                    current_node = current_node.right
            return current_node.value

        dc_huffman_table = {
            0: '00', 1: '010', 2: '011', 3: '100', 4: '101', 5: '110',
            6: '1110', 7: '11110', 8: '111110', 9: '1111110', 10: '11111110', 11: '111111110'
        }

        def encode_dc_coefficient(dc_coeff):
            dc_coeff = int(dc_coeff)
            magnitude = abs(dc_coeff)
            size = magnitude.bit_length()

            huffman_code = dc_huffman_table[size]

            if dc_coeff < 0:
                magnitude = (1 << size) - 1 + dc_coeff

            magnitude_bin = bin(magnitude)[2:].zfill(size)
            return huffman_code + magnitude_bin

        encoded_dc_coeffs = [encode_dc_coefficient(coeff) for coeff in DC]
        encoded_dc_bitstream = ''.join(encoded_dc_coeffs)
        compressed_data = encoded_dc_bitstream

        if not set(compressed_data).issubset({'0', '1'}):
            raise ValueError("Invalid character in compressed data")

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

        bitstream = BitStream(bin=compressed_data)
        decoded_dc_coeffs = []
        while bitstream.pos < bitstream.len and len(decoded_dc_coeffs) < len(DC):
            try:
                decoded_dc_coeff = decode_dc_coefficient(bitstream, dc_huffman_tree)
                if decoded_dc_coeff is None:
                    break
                decoded_dc_coeffs.append(decoded_dc_coeff)
            except ValueError as e:
                print("Error decoding DC coefficient:", e)
                break

        def generate_huffman_dict(node, current_code=""):
            if node is None:
                return {}
            if node.value is not None:
                return {node.value: current_code}
            codes = {}
            codes.update(generate_huffman_dict(node.left, current_code + "0"))
            codes.update(generate_huffman_dict(node.right, current_code + "1"))
            return codes

        huffman_dict = generate_huffman_dict(dc_huffman_tree)

        return DC, encoded_dc_bitstream, compressed_data, dc_huffman_tree, decoded_dc_coeffs, huffman_dict

    def create_dht_segment(huffman_dict, table_class, table_id):
        lengths = [0] * 16
        symbols = []
        
        for symbol, code in huffman_dict.items():
            code_length = len(code)
            lengths[code_length - 1] += 1
            symbols.append(symbol)
        
        dht_segment = bytearray()
        dht_segment.append(0xFF)
        dht_segment.append(0xC4)  # DHT marker
        dht_length = 2 + 1 + 16 + len(symbols)
        dht_segment.extend(dht_length.to_bytes(2, byteorder='big'))
        dht_segment.append((table_class << 4) | table_id)
        dht_segment.extend(lengths)
        dht_segment.extend(symbols)
        
        return dht_segment

    def generate_jpeg_header(y_huffman_dict, u_huffman_dict, v_huffman_dict):
        dht_segments = bytearray()
        
        dht_segments.extend(create_dht_segment(y_huffman_dict, 0, 0))  # Y DC table
        dht_segments.extend(create_dht_segment(y_huffman_dict, 1, 0))  # Y AC table
        dht_segments.extend(create_dht_segment(u_huffman_dict, 0, 1))  # U DC table
        dht_segments.extend(create_dht_segment(u_huffman_dict, 1, 1))  # U AC table
        dht_segments.extend(create_dht_segment(v_huffman_dict, 0, 2))  # V DC table
        dht_segments.extend(create_dht_segment(v_huffman_dict, 1, 2))  # V AC table

        return dht_segments

    y_dc, y_encoded_dc_bitstream, y_compressed_data, y_huffman_tree, y_decoded_dc_coeffs, y_huffman_dict = Huffman_code(Y_data)
    u_dc, u_encoded_dc_bitstream, u_compressed_data, u_huffman_tree, u_decoded_dc_coeffs, u_huffman_dict = Huffman_code(U_data)
    v_dc, v_encoded_dc_bitstream, v_compressed_data, v_huffman_tree, v_decoded_dc_coeffs, v_huffman_dict = Huffman_code(V_data)

    jpeg_header = generate_jpeg_header(y_huffman_dict, u_huffman_dict, v_huffman_dict)

    # 合并YUV二进制编码数据
    merged_encoded_data = y_encoded_dc_bitstream + u_encoded_dc_bitstream + v_encoded_dc_bitstream

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

    x = binary_to_hex(merged_encoded_data)
    #新增轉換十六進制，x為原本的merged_encoded_data
    return jpeg_header, x

# 示例使用：
# Y_data = [23, -2, 3, 0, 0, -1, 5]  # 示例DC系数数据
# U_data = [5, -1, 2, 1, 0, 0, 3]    # 示例DC系数数据
# V_data = [3, 1, -1, 2, 0, 0, -2]   # 示例DC系数数据

# jpeg_header, merged_encoded_data = Huffman_code(Y_data, U_data, V_data)
# print(jpeg_header)
# print(merged_encoded_data)
