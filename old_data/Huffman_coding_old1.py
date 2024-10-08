import heapq
from collections import defaultdict, Counter
import pickle

def Huffman_coding(Y_DC_data,U_DC_data,V_DC_data,Y_AC_data,U_AC_data,V_AC_data):

    class Node:
        def __init__(self, symbol, freq):
            self.symbol = symbol
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def build_huffman_tree(frequencies):
        heap = [Node(symbol, freq) for symbol, freq in frequencies.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        return heap[0]

    def generate_huffman_codes(node, prefix="", codebook={}):
        if node is not None:
            if node.symbol is not None:
                codebook[node.symbol] = prefix
            generate_huffman_codes(node.left, prefix + "0", codebook)
            generate_huffman_codes(node.right, prefix + "1", codebook)
        return codebook

    def huffman_encoding(data, codebook):
        return ''.join(codebook[symbol] for symbol in data)

    def huffman_decoding(encoded_data, huffman_tree):
        decoded_data = []
        node = huffman_tree
        for bit in encoded_data:
            if bit == '0':
                node = node.left
            else:
                node = node.right
            if node.symbol is not None:
                decoded_data.append(node.symbol)
                node = huffman_tree
        return decoded_data

    def flatten_data(data):
        return [tuple(item) for sublist in data for item in sublist]

    def reduce_symbols(data, max_symbols=255):
        frequencies = Counter(data)
        if len(frequencies) > max_symbols:
            most_common = frequencies.most_common(max_symbols)
            reduced_data = []
            symbol_map = {item[0]: idx for idx, item in enumerate(most_common)}
            for item in data:
                reduced_data.append(symbol_map.get(item, max_symbols))
            return reduced_data, symbol_map
        else:
            return data, None

    def encode_and_decode(data, is_dc=False):
        if is_dc:
            flattened_data = data
        else:
            flattened_data = flatten_data(data)
        
        # Reduce symbols to max 255 if necessary
        flattened_data, symbol_map = reduce_symbols(flattened_data)
        
        frequencies = Counter(flattened_data)
        huffman_tree = build_huffman_tree(frequencies)
        codebook = generate_huffman_codes(huffman_tree)
        encoded_data = huffman_encoding(flattened_data, codebook)
        decoded_data = huffman_decoding(encoded_data, huffman_tree)
        
        if symbol_map:
            reversed_symbol_map = {v: k for k, v in symbol_map.items()}
            decoded_data = [reversed_symbol_map.get(item, item) for item in decoded_data]
        
        return flattened_data, encoded_data, decoded_data, codebook, huffman_tree

    def serialize_data(codebook, encoded_data):
        codebook_bytes = pickle.dumps(codebook)
        encoded_data_bytes = pickle.dumps(encoded_data)
        return codebook_bytes, encoded_data_bytes

    def deserialize_data(codebook_bytes, encoded_data_bytes):
        codebook = pickle.loads(codebook_bytes)
        encoded_data = pickle.loads(encoded_data_bytes)
        return codebook, encoded_data

    def bytes_roundtrip(data, is_dc=False):
        flattened_data, encoded_data, decoded_data, codebook, huffman_tree = encode_and_decode(data, is_dc)
        codebook_bytes, encoded_data_bytes = serialize_data(codebook, encoded_data)
        deserialized_codebook, deserialized_encoded_data = deserialize_data(codebook_bytes, encoded_data_bytes)
        
        huffman_tree = build_huffman_tree(Counter(flattened_data))  # Rebuild tree from frequencies
        decoded_data_from_bytes = huffman_decoding(deserialized_encoded_data, huffman_tree)
        
        return flattened_data, decoded_data_from_bytes, codebook_bytes, encoded_data_bytes

    # # 範例
    # Y_AC_data = [[[3, 1], [2, 5], [1, 0]], [[1, 2], [0, 0]]]
    # U_AC_data = [[[2, 3], [3, 4], [1, 0]], [[1, 1], [0, 0]]]
    # V_AC_data = [[[1, 4], [2, 3], [1, 0]], [[1, 5], [0, 0]]]

    # Y_DC_data = [23, -2, 3, 0, 0, -1, 5]
    # U_DC_data = [5, -1, 2, 1, 0, 0, 3]
    # V_DC_data = [3, 1, -1, 2, 0, 0, -2]

    # 對AC數據進行霍夫曼編碼與解碼，並獲取霍夫曼表和數據
    Y_AC_flattened, Y_AC_decoded_from_bytes, Y_AC_codebook_bytes, Y_AC_encoded_data_bytes = bytes_roundtrip(Y_AC_data)
    U_AC_flattened, U_AC_decoded_from_bytes, U_AC_codebook_bytes, U_AC_encoded_data_bytes = bytes_roundtrip(U_AC_data)
    V_AC_flattened, V_AC_decoded_from_bytes, V_AC_codebook_bytes, V_AC_encoded_data_bytes = bytes_roundtrip(V_AC_data)

    # 對DC數據進行霍夫曼編碼與解碼，並獲取霍夫曼表和數據
    Y_DC_flattened, Y_DC_decoded_from_bytes, Y_DC_codebook_bytes, Y_DC_encoded_data_bytes = bytes_roundtrip(Y_DC_data, is_dc=True)
    U_DC_flattened, U_DC_decoded_from_bytes, U_DC_codebook_bytes, U_DC_encoded_data_bytes = bytes_roundtrip(U_DC_data, is_dc=True)
    V_DC_flattened, V_DC_decoded_from_bytes, V_DC_codebook_bytes, V_DC_encoded_data_bytes = bytes_roundtrip(V_DC_data, is_dc=True)

    print("Y_AC_codebook_bytes:", Y_AC_codebook_bytes)
    print("Y_AC_encoded_data_bytes:", Y_AC_encoded_data_bytes)
    print("U_AC_codebook_bytes:", U_AC_codebook_bytes)
    print("U_AC_encoded_data_bytes:", U_AC_encoded_data_bytes)
    print("V_AC_codebook_bytes:", V_AC_codebook_bytes)
    print("V_AC_encoded_data_bytes:", V_AC_encoded_data_bytes)

    print("Y_DC_codebook_bytes:", Y_DC_codebook_bytes)
    print("Y_DC_encoded_data_bytes:", Y_DC_encoded_data_bytes)
    print("U_DC_codebook_bytes:", U_DC_codebook_bytes)
    print("U_DC_encoded_data_bytes:", U_DC_encoded_data_bytes)
    print("V_DC_codebook_bytes:", V_DC_codebook_bytes)
    print("V_DC_encoded_data_bytes:", V_DC_encoded_data_bytes)

    return Y_AC_codebook_bytes,Y_AC_encoded_data_bytes,U_AC_codebook_bytes,U_AC_encoded_data_bytes,V_AC_codebook_bytes,V_AC_encoded_data_bytes,Y_DC_codebook_bytes,Y_DC_encoded_data_bytes,U_DC_codebook_bytes,U_DC_encoded_data_bytes,V_DC_codebook_bytes,V_DC_encoded_data_bytes


