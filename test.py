import numpy as np
from bitstring import BitStream, ReadError

def Huffman_code(DC, AC):
    DC = np.array(DC, dtype=np.int32)
    AC = np.array(AC, dtype=np.int32)
    
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

    ac_huffman_table = {
        (0, 0): '1010',      # EOB (End of Block)
        (0, 1): '00',        (0, 2): '01',        (0, 3): '100',      (0, 4): '1011',     (0, 5): '11010',
        (0, 6): '1111000',   (0, 7): '11111000',  (0, 8): '1111110110', (0, 9): '1111111110000010', (0, 10): '1111111110000011',
        (1, 1): '1100',      (1, 2): '11011',     (1, 3): '1111001',  (1, 4): '111110110', (1, 5): '11111110110', 
        (1, 6): '1111111110000100', (1, 7): '1111111110000101', (1, 8): '1111111110000110', (1, 9): '1111111110000111', (1, 10): '1111111110001000',
        (2, 1): '11100',     (2, 2): '11111001',  (2, 3): '1111110111', (2, 4): '111111110100', (2, 5): '1111111110001001', 
        (2, 6): '1111111110001010', (2, 7): '1111111110001011', (2, 8): '1111111110001100', (2, 9): '1111111110001101', (2, 10): '1111111110001110',
        (3, 1): '111010',    (3, 2): '111110111', (3, 3): '111111110101', (3, 4): '1111111110001111', (3, 5): '1111111110010000',
        (3, 6): '1111111110010001', (3, 7): '1111111110010010', (3, 8): '1111111110010011', (3, 9): '1111111110010100', (3, 10): '1111111110010101',
        (4, 1): '111011',    (4, 2): '1111111000', (4, 3): '1111111110010110', (4, 4): '1111111110010111', (4, 5): '1111111110011000',
        (4, 6): '1111111110011001', (4, 7): '1111111110011010', (4, 8): '1111111110011011', (4, 9): '1111111110011100', (4, 10): '1111111110011101',
        (5, 1): '1111010',   (5, 2): '11111110111', (5, 3): '1111111110011110', (5, 4): '1111111110011111', (5, 5): '1111111110100000',
        (5, 6): '1111111110100001', (5, 7): '1111111110100010', (5, 8): '1111111110100011', (5, 9): '1111111110100100', (5, 10): '1111111110100101',
        (6, 1): '1111011',   (6, 2): '111111110110', (6, 3): '1111111110100110', (6, 4): '1111111110100111', (6, 5): '1111111110101000',
        (6, 6): '1111111110101001', (6, 7): '1111111110101010', (6, 8): '1111111110101011', (6, 9): '1111111110101100', (6, 10): '1111111110101101',
        (7, 1): '11111010',  (7, 2): '111111110111', (7, 3): '1111111110101110', (7, 4): '1111111110101111', (7, 5): '1111111110110000',
        (7, 6): '1111111110110001', (7, 7): '1111111110110010', (7, 8): '1111111110110011', (7, 9): '1111111110110100', (7, 10): '1111111110110101',
        (8, 1): '111111000', (8, 2): '1111111110110110', (8, 3): '1111111110110111', (8, 4): '1111111110111000', (8, 5): '1111111110111001',
        (8, 6): '1111111110111010', (8, 7): '1111111110111011', (8, 8): '1111111110111100', (8, 9): '1111111110111101', (8, 10): '1111111110111110',
        (9, 1): '111111001', (9, 2): '1111111110111111', (9, 3): '1111111111000000', (9, 4): '1111111111000001', (9, 5): '1111111111000010',
        (9, 6): '1111111111000011', (9, 7): '1111111111000100', (9, 8): '1111111111000101', (9, 9): '1111111111000110', (9, 10): '1111111111000111',
        (10, 1): '111111010', (10, 2): '1111111111001000', (10, 3): '1111111111001001', (10, 4): '1111111111001010', (10, 5): '1111111111001011',
        (10, 6): '1111111111001100', (10, 7): '1111111111001101', (10, 8): '1111111111001110', (10, 9): '1111111111001111', (10, 10): '1111111111010000',
        (11, 1): '11111111000', (11, 2): '1111111111010001', (11, 3): '1111111111010010', (11, 4): '1111111111010011', (11, 5): '1111111111010100',
        (11, 6): '1111111111010101', (11, 7): '1111111111010110', (11, 8): '1111111111010111', (11, 9): '1111111111011000', (11, 10): '1111111111011001',
        (12, 1): '1111111111011010', (12, 2): '1111111111011011', (12, 3): '1111111111011100', (12, 4): '1111111111011101', (12, 5): '1111111111011110',
        (12, 6): '1111111111011111', (12, 7): '1111111111100000', (12, 8): '1111111111100001', (12, 9): '1111111111100010', (12, 10): '1111111111100011',
        (13, 1): '1111111111100100', (13, 2): '1111111111100101', (13, 3): '1111111111100110', (13, 4): '1111111111100111', (13, 5): '1111111111101000',
        (13, 6): '1111111111101001', (13, 7): '1111111111101010', (13, 8): '1111111111101011', (13, 9): '1111111111101100', (13, 10): '1111111111101101',
        (14, 1): '1111111111101110', (14, 2): '1111111111101111', (14, 3): '1111111111110000', (14, 4): '1111111111110001', (14, 5): '1111111111110010',
        (14, 6): '1111111111110011', (14, 7): '1111111111110100', (14, 8): '1111111111110101', (14, 9): '1111111111110110', (14, 10): '1111111111110111',
        (15, 0): '11111111001',    # ZRL (Zero Run Length)
        (15, 1): '1111111111111000', (15, 2): '1111111111111009', (15, 3): '1111111111111010', (15, 4): '1111111111111011', (15, 5): '1111111111111100',
        (15, 6): '1111111111111101', (15, 7): '1111111111111110', (15, 8): '1111111111111111'
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

    dc_coefficients = DC
    ac_coefficients = AC

    encoded_dc_coeffs = [encode_dc_coefficient(coeff) for coeff in dc_coefficients]
    encoded_dc_bitstream = ''.join(encoded_dc_coeffs)

    encoded_ac_coeffs = [ac_huffman_table[tuple(coeff)] for coeff in ac_coefficients]
    encoded_ac_bitstream = ''.join(encoded_ac_coeffs)

    compressed_data = encoded_dc_bitstream + encoded_ac_bitstream

    print("Encoded DC Bitstream:", encoded_dc_bitstream)
    print("Encoded AC Bitstream:", encoded_ac_bitstream)
    print("Compressed Data:", compressed_data)

    dc_huffman_tree = build_huffman_tree(dc_huffman_table)
    ac_huffman_tree = build_huffman_tree(ac_huffman_table)

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

    bitstream.pos = 0
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

    bitstream.pos = len(encoded_dc_bitstream)
    decoded_ac_coeffs = []
    while bitstream.pos < bitstream.len:
        ac_coeff = decode_huffman_code(bitstream, ac_huffman_tree)
        if ac_coeff == (0, 0):  # EOB
            decoded_ac_coeffs.append(ac_coeff)
            break
        decoded_ac_coeffs.append(ac_coeff)

    print("Original DC Coefficients:", DC)
    print("Original AC Coefficients:", AC)
    print("Decoded DC Coefficients:", decoded_dc_coeffs)
    print("Decoded AC Coefficients:", decoded_ac_coeffs)

# Example input
DC = [15, -3, 8]
AC = [[0, 1], [1, 2], [0, 0]]
Huffman_code(DC, AC)
