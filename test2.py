Y_AC_codebook_bytes = b'\xff\xc4\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
UV_AC_codebook_bytes = b'\xff\xc4\x00\xb5\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1\x17\x18\x19\x1a&\'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
Y_DC_codebook_bytes = b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
UV_DC_codebook_bytes = b'\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'

class HuffmanNode:
    def __init__(self, symbol=None):
        self.symbol = symbol
        self.left = None
        self.right = None

def build_huffman_tree(data):
    if data[:2] != b'\xff\xc4':
        raise ValueError("Invalid Huffman table marker")
    
    table_class = data[4] >> 4  # 0 for DC, 1 for AC
    table_id = data[4] & 0x0F
    
    code_lengths = data[5:21]
    symbols = data[21:]
    
    root = HuffmanNode()
    code = 0
    symbol_index = 0
    
    for bits in range(1, 17):
        code <<= 1
        for _ in range(code_lengths[bits-1]):
            node = root
            for bit in range(bits-1, -1, -1):
                if code & (1 << bit):
                    if node.right is None:
                        node.right = HuffmanNode()
                    node = node.right
                else:
                    if node.left is None:
                        node.left = HuffmanNode()
                    node = node.left
            node.symbol = symbols[symbol_index]
            symbol_index += 1
            code += 1
    
    return root, 'AC' if table_class else 'DC', table_id

def print_huffman_tree(node, code=''):
    if node.symbol is not None:
        print(f"Symbol: {node.symbol:02X}, Code: {code}")
    if node.left:
        print_huffman_tree(node.left, code + '0')
    if node.right:
        print_huffman_tree(node.right, code + '1')

# 解析並打印每個霍夫曼樹
for name, data in [("Y AC", Y_AC_codebook_bytes), 
                   ("UV AC", UV_AC_codebook_bytes),
                   ("Y DC", Y_DC_codebook_bytes),
                   ("UV DC", UV_DC_codebook_bytes)]:
    root, table_type, table_id = build_huffman_tree(data)
    print(f"\n{name} Codebook (Type: {table_type}, ID: {table_id}):")
    print_huffman_tree(root)