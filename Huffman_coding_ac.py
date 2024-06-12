from heapq import heappush, heappop, heapify
from collections import Counter, defaultdict

def Huffman_code(Y_data, U_data, V_data):
    def Huffman_code(data):
        class Node:
            def __init__(self, symbol=None, weight=0, left=None, right=None):
                self.symbol = symbol
                self.weight = weight
                self.left = left
                self.right = right

            def __lt__(self, other):
                return self.weight < other.weight

        def create_huffman_tree(frequencies, max_code_length=16):
            heap = [Node(symbol, weight) for symbol, weight in frequencies.items()]
            heapify(heap)
            while len(heap) > 1:
                lo = heappop(heap)
                hi = heappop(heap)
                merged = Node(weight=lo.weight + hi.weight, left=lo, right=hi)
                heappush(heap, merged)
            
            root = heap[0]
            huffman_dict = {}
            def assign_codes(node, code=""):
                if node.symbol is not None:
                    huffman_dict[node.symbol] = code
                    return
                if node.left:
                    assign_codes(node.left, code + '0')
                if node.right:
                    assign_codes(node.right, code + '1')
            
            assign_codes(root)

            # Check if any code length exceeds max_code_length
            lengths = defaultdict(int)
            for code in huffman_dict.values():
                lengths[len(code)] += 1

            # If any code length exceeds the maximum, adjust the tree
            if any(length > max_code_length for length in lengths.keys()):
                huffman_dict = adjust_code_lengths(huffman_dict, max_code_length)

            return huffman_dict

        def adjust_code_lengths(huffman_dict, max_code_length):
            # This function adjusts the code lengths to fit within the max_code_length constraint
            sorted_symbols = sorted(huffman_dict.items(), key=lambda item: (len(item[1]), item[1]))
            new_huffman_dict = {}
            current_length = 1
            for symbol, code in sorted_symbols:
                if len(code) > max_code_length:
                    new_code = bin(len(new_huffman_dict))[2:].zfill(max_code_length)
                    new_huffman_dict[symbol] = new_code
                else:
                    new_huffman_dict[symbol] = code
                current_length += 1
            return new_huffman_dict

        # Flatten RLE data for Huffman encoding and ensure symbols are within the valid range
        flat_data = []
        for segment in data:
            for count, value in segment:
                count = max(0, min(255, count))  # Ensure count is within valid range
                value = max(0, min(255, value))  # Ensure value is within valid range
                flat_data.append(count)
                flat_data.append(value)

        # Huffman encode the flat data
        frequencies = Counter(flat_data)
        huffman_dict = create_huffman_tree(frequencies)
        encoded_data = ''.join(huffman_dict[symbol] for symbol in flat_data)
        
        return encoded_data, huffman_dict

    def create_dht_segment(huffman_dict, table_class, table_id):
        lengths = [0] * 16
        symbols = []
        
        for symbol, code in huffman_dict.items():
            code_length = len(code)
            if code_length > 16:
                raise ValueError(f"Code length {code_length} is too long for JPEG standard")
            lengths[code_length - 1] += 1
            symbol = max(0, min(255, symbol))  # Ensure symbol is within valid byte range
            symbols.append(symbol)

        dht_segment = bytearray()
        dht_segment.extend(b'\xFF\xC4\x00\xB5\x10')  # DHT marker
        dht_length = 2 + 1 + 16 + len(symbols)
        dht_segment.extend(dht_length.to_bytes(2, byteorder='big'))
        dht_segment.append((table_class << 4) | table_id)
        dht_segment.extend(lengths)
        dht_segment.extend(symbols)
        
        return dht_segment

    def generate_jpeg_header(y_huffman_dict, u_huffman_dict, v_huffman_dict):
        dht_segments = bytearray()
        
        # Create DHT segments for Y, U, and V components
        dht_segments.extend(create_dht_segment(y_huffman_dict, 0, 0))  # Y DC table
        dht_segments.extend(create_dht_segment(y_huffman_dict, 1, 0))  # Y AC table
        dht_segments.extend(create_dht_segment(u_huffman_dict, 0, 1))  # U DC table
        dht_segments.extend(create_dht_segment(u_huffman_dict, 1, 1))  # U AC table
        dht_segments.extend(create_dht_segment(v_huffman_dict, 0, 2))  # V DC table
        dht_segments.extend(create_dht_segment(v_huffman_dict, 1, 2))  # V AC table

        # Here we should add other JPEG header segments (SOI, APP0, DQT, SOF0, SOS, etc.)
        # For simplicity, this example only focuses on DHT segments.
        
        return dht_segments

    y_huffman_encoded_data, y_huffman_dict = Huffman_code(Y_data)
    u_huffman_encoded_data, u_huffman_dict = Huffman_code(U_data)
    v_huffman_encoded_data, v_huffman_dict = Huffman_code(V_data)

    jpeg_header = generate_jpeg_header(y_huffman_dict, u_huffman_dict, v_huffman_dict)

    # 合并YUV二进制编码数据
    merged_encoded_data = y_huffman_encoded_data + u_huffman_encoded_data + v_huffman_encoded_data

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
    
    y = binary_to_hex(merged_encoded_data)
    #新增轉換十六進制，x為原本的merged_encoded_data
    return jpeg_header, y

# # Example usage:
# Y_data = [[[3, 1], [2, 5], [1, 0]], [[1, 2], [0, 0]]]  # Example RLE data for Y component
# U_data = [[[2, 3], [3, 4], [1, 0]], [[1, 1], [0, 0]]]  # Example RLE data for U component
# V_data = [[[1, 4], [2, 3], [1, 0]], [[1, 5], [0, 0]]]  # Example RLE data for V component

# jpeg_header, merged_encoded_data = Huffman_code(Y_data, U_data, V_data)
# print(y)
# print(merged_encoded_data)
