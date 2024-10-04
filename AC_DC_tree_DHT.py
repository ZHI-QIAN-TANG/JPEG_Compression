def AC_DC_tree_DHT(dc_huffman_table,ac_huffman_table):
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

    def huffman_tree_to_dict(node, prefix=''):
        if node.value is not None:
            return {node.value: prefix}
        result = {}
        if node.left is not None:
            result.update(huffman_tree_to_dict(node.left, prefix + '0'))
        if node.right is not None:
            result.update(huffman_tree_to_dict(node.right, prefix + '1'))
        return result

    def create_huffman_table(huffman_dict):
        depth_count = [0] * 16
        huffman_codes = [''] * 256

        # 處理負號的偏移量
        for symbol, code in huffman_dict.items():
            length = len(code)
            depth_count[length - 1] += 1
            huffman_codes[symbol + 128] = code 

        # 刪除偏移量
        symbols = []
        for length in range(16):
            for i, code in enumerate(huffman_codes):
                if len(code) == length + 1:
                    symbols.append(i - 128)

        return depth_count, symbols

    def generate_huffman_segment(huffman_table, table_class):
        depth_count, symbols = create_huffman_table(huffman_table)
        length = 2 + 1 + 16 + len(symbols)

        segment = bytearray()
        segment.extend(b'\xFF\xC4')  # 霍夫曼表標記
        segment.extend(length.to_bytes(2, 'big'))  
        segment.append(table_class)  # 表格類別（0 表示 DC，1 表示 AC）
        segment.extend(depth_count)  # 深度計數數組
        segment.extend((symbol + 128) % 256 for symbol in symbols)  # 帶偏移量的符號

        return segment

    def create_jpeg_header(dc_huffman_table, ac_huffman_table):
        dc_segment = generate_huffman_segment(dc_huffman_table, 0x00)  # 0x00表示DC表0
        ac_segment = generate_huffman_segment(ac_huffman_table, 0x10)  # 0x10表示AC表0

        header = bytearray()
        header.extend(b'\xFF\xD8')  # SOI 標記
        header.extend(b'\xFF\xE0')  # APP0 標記
        header.extend((16).to_bytes(2, 'big'))  # APP0段的長度
        header.extend(b'JFIF\x00')  # 標識符
        header.extend(b'\x01\x01')  # 版本
        header.extend(b'\x00')  # 密度單位
        header.extend((1).to_bytes(2, 'big'))  # X 密度
        header.extend((1).to_bytes(2, 'big'))  # Y 密度
        header.extend(b'\x00\x00')  # 縮圖的寬度和高度

        header.extend(dc_segment)
        header.extend(ac_segment)

        return header

    jpeg_header = create_jpeg_header(dc_huffman_table, ac_huffman_table)
    # print(jpeg_header.hex())

    # 建構霍夫曼樹
    dc_huffman_tree = build_huffman_tree(dc_huffman_table)
    ac_huffman_tree = build_huffman_tree(ac_huffman_table)

    # 將霍夫曼樹轉回字典
    dc_huffman_dict = huffman_tree_to_dict(dc_huffman_tree)
    ac_huffman_dict = huffman_tree_to_dict(ac_huffman_tree)

    # print("DC Huffman Dict:", dc_huffman_dict)
    # print("AC Huffman Dict:", ac_huffman_dict)
    return jpeg_header.hex()
