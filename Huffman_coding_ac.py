from heapq import heappush, heappop, heapify
from collections import Counter

def Huffman_code(AC):

    def rle_decode(encoded_data):
        decoded_data = []
        for segment in encoded_data:
            for count, value in segment:
                decoded_data.extend([value] * count)
        return decoded_data

    class Node:
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right

        def children(self):
            return (self.left, self.right)

        def __lt__(self, other):
            return 0

    def create_huffman_tree(frequencies):
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

    def huffman_encode(data):
        frequencies = Counter(data)
        huffman_tree = create_huffman_tree(frequencies)
        huffman_dict = {symbol: code for symbol, code in huffman_tree}
        encoded_data = ''.join(huffman_dict[symbol] for symbol in data)
        return encoded_data, huffman_dict

    def huffman_decode(encoded_data, huffman_dict):
        reverse_huffman_dict = {v: k for k, v in huffman_dict.items()}
        decoded_data = []
        buffer = ""
        for bit in encoded_data:
            buffer += bit
            if buffer in reverse_huffman_dict:
                decoded_data.append(reverse_huffman_dict[buffer])
                buffer = ""
        return decoded_data


    # 步骤1：RLE编码数据
    #print("RLE 编码数据:", AC)

    # 扁平化RLE数据以进行Huffman编码
    flat_data = []
    for segment in AC:
        for count, value in segment:
            flat_data.append(count)
            flat_data.append(value)

    # 步骤2：Huffman编码
    huffman_encoded_data, huffman_dict = huffman_encode(flat_data)
    #print("Huffman 编码数据:", huffman_encoded_data)
    #print("Huffman 字典:", huffman_dict)

    # 步骤3：Huffman解码
    huffman_decoded_data = huffman_decode(huffman_encoded_data, huffman_dict)
    #print("Huffman 解码数据:", huffman_decoded_data)

    # 从Huffman解码数据重建RLE编码数据
    reconstructed_rle_encoded_data = []
    segment = []
    for i in range(0, len(huffman_decoded_data), 2):
        count = huffman_decoded_data[i]
        value = huffman_decoded_data[i + 1]
        segment.append([count, value])
        if count == 0 and value == 0:
            reconstructed_rle_encoded_data.append(segment)
            segment = []

    # 确保所有数据都被处理
    if segment:
        reconstructed_rle_encoded_data.append(segment)

    #print("重建的RLE编码数据:", reconstructed_rle_encoded_data)

    # 验证原始数据和解码数据是否相同
    #print("数据匹配:", AC == reconstructed_rle_encoded_data)
    
    return huffman_encoded_data, huffman_dict

