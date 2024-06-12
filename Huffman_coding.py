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

    # # 示例使用數據
    # Y_AC_data = [[[3, 1], [2, 5], [1, 0]], [[1, 2], [0, 0]]]
    # U_AC_data = [[[2, 3], [3, 4], [1, 0]], [[1, 1], [0, 0]]]
    # V_AC_data = [[[1, 4], [2, 3], [1, 0]], [[1, 5], [0, 0]]]

    # Y_DC_data = [23, -2, 3, 0, 0, -1, 5]
    # U_DC_data = [5, -1, 2, 1, 0, 0, 3]
    # V_DC_data = [3, 1, -1, 2, 0, 0, -2]

    def flatten_data(data):
        return [tuple(item) for sublist in data for item in sublist]

    def encode_and_decode(data, is_dc=False):
        if is_dc:
            flattened_data = data
        else:
            flattened_data = flatten_data(data)
        frequencies = Counter(flattened_data)
        huffman_tree = build_huffman_tree(frequencies)
        codebook = generate_huffman_codes(huffman_tree)
        encoded_data = huffman_encoding(flattened_data, codebook)
        decoded_data = huffman_decoding(encoded_data, huffman_tree)
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
        
        return flattened_data, decoded_data_from_bytes

    # 對AC資料進行霍夫曼編碼和解碼，並獲取霍夫曼表和編碼資料的字節
    Y_AC_flattened, Y_AC_encoded, Y_AC_decoded, Y_AC_codebook, _ = encode_and_decode(Y_AC_data)
    U_AC_flattened, U_AC_encoded, U_AC_decoded, U_AC_codebook, _ = encode_and_decode(U_AC_data)
    V_AC_flattened, V_AC_encoded, V_AC_decoded, V_AC_codebook, _ = encode_and_decode(V_AC_data)

    # 對DC資料進行霍夫曼編碼和解碼，並獲取霍夫曼表和編碼資料的字節
    Y_DC_flattened, Y_DC_encoded, Y_DC_decoded, Y_DC_codebook, _ = encode_and_decode(Y_DC_data, is_dc=True)
    U_DC_flattened, U_DC_encoded, U_DC_decoded, U_DC_codebook, _ = encode_and_decode(U_DC_data, is_dc=True)
    V_DC_flattened, V_DC_encoded, V_DC_decoded, V_DC_codebook, _ = encode_and_decode(V_DC_data, is_dc=True)


    # 序列化霍夫曼表和編碼數據為16進制
    Y_AC_codebook_bytes, Y_AC_encoded_data_bytes = serialize_data(Y_AC_codebook, Y_AC_encoded)
    U_AC_codebook_bytes, U_AC_encoded_data_bytes = serialize_data(U_AC_codebook, U_AC_encoded)
    V_AC_codebook_bytes, V_AC_encoded_data_bytes = serialize_data(V_AC_codebook, V_AC_encoded)

    Y_DC_codebook_bytes, Y_DC_encoded_data_bytes = serialize_data(Y_DC_codebook, Y_DC_encoded)
    U_DC_codebook_bytes, U_DC_encoded_data_bytes = serialize_data(U_DC_codebook, U_DC_encoded)
    V_DC_codebook_bytes, V_DC_encoded_data_bytes = serialize_data(V_DC_codebook, V_DC_encoded)

    # 印出霍夫曼編碼與資料:(codebook:霍夫曼表、encoded:資料)
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

    print()
    # 對AC數據進行霍夫曼編碼和解碼，驗證序列化和反序列化
    Y_AC_flattened, Y_AC_decoded_from_bytes = bytes_roundtrip(Y_AC_data)
    U_AC_flattened, U_AC_decoded_from_bytes = bytes_roundtrip(U_AC_data)
    V_AC_flattened, V_AC_decoded_from_bytes = bytes_roundtrip(V_AC_data)

    # 對DC數據進行霍夫曼編碼和解碼，驗證序列化和反序列化
    Y_DC_flattened, Y_DC_decoded_from_bytes = bytes_roundtrip(Y_DC_data, is_dc=True)
    U_DC_flattened, U_DC_decoded_from_bytes = bytes_roundtrip(U_DC_data, is_dc=True)
    V_DC_flattened, V_DC_decoded_from_bytes = bytes_roundtrip(V_DC_data, is_dc=True)

    # # 查看資料並驗證
    # print("Y AC data encoding =", Y_AC_flattened)
    # print("Y AC data decoding =", Y_AC_decoded_from_bytes)
    # print("U AC data encoding =", U_AC_flattened)
    # print("U AC data decoding =", U_AC_decoded_from_bytes)
    # print("V AC data encoding =", V_AC_flattened)
    # print("V AC data decoding =", V_AC_decoded_from_bytes)

    # print("Y DC data encoding =", Y_DC_flattened)
    # print("Y DC data decoding =", Y_DC_decoded_from_bytes)
    # print("U DC data encoding =", U_DC_flattened)
    # print("U DC data decoding =", U_DC_decoded_from_bytes)
    # print("V DC data encoding =", V_DC_flattened)
    # print("V DC data decoding =", V_DC_decoded_from_bytes)
    print("Y AC data check", Y_AC_flattened == Y_AC_decoded_from_bytes)
    print("U AC data check", U_AC_flattened == U_AC_decoded_from_bytes)
    print("V AC data check", V_AC_flattened == V_AC_decoded_from_bytes)
    print("Y DC data check", Y_DC_flattened == Y_DC_decoded_from_bytes)
    print("U DC data check", U_DC_flattened == U_DC_decoded_from_bytes)
    print("V DC data check", V_DC_flattened == V_DC_decoded_from_bytes)

    return Y_AC_codebook_bytes,Y_AC_encoded_data_bytes,U_AC_codebook_bytes,U_AC_encoded_data_bytes,V_AC_codebook_bytes,V_AC_encoded_data_bytes,Y_DC_codebook_bytes,Y_DC_encoded_data_bytes,U_DC_codebook_bytes,U_DC_encoded_data_bytes,V_DC_codebook_bytes,V_DC_encoded_data_bytes


