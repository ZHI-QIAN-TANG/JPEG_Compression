def Huffman_code(AC):
    # Step 1: RLE encoding
    print("Original RLE Encoded Data:", AC)

    # Flatten RLE data for Huffman encoding
    flat_data = []
    for segment in AC:
        for count, value in segment:
            flat_data.append(count)
            flat_data.append(value)

    # Step 2: Huffman encoding
    huffman_encoded_data, huffman_dict = huffman_encode(flat_data)
    print("Huffman Encoded Data:", huffman_encoded_data)
    print("Huffman Dictionary:", huffman_dict)

    # Step 3: Huffman decoding
    huffman_decoded_data = huffman_decode(huffman_encoded_data, huffman_dict)
    print("Huffman Decoded Data:", huffman_decoded_data)

    # Reconstruct RLE encoded data from flat data
    reconstructed_rle_encoded_data = []
    i = 0
    while i < len(huffman_decoded_data):
        count = huffman_decoded_data[i]
        value = huffman_decoded_data[i + 1]
        reconstructed_rle_encoded_data.append([[count, value]])
        i += 2
    print("Reconstructed RLE Encoded Data:", reconstructed_rle_encoded_data)

    # Step 4: RLE decoding
    rle_decoded_data = rle_decode(reconstructed_rle_encoded_data)
    print("RLE Decoded Data:", rle_decoded_data)

    # Verify that the original data and the decoded data are the same
    print("Data matches:", AC == reconstructed_rle_encoded_data)

# 测试数据
AC = [[[1, -2], [15, 0], [15, 0], [15, 0], [0, 0]], [[1, -2], [15, 0], [15, 0], [15, 0], [0, 0]], [[1, -2], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, 1], [2, -1], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, 1], [0, 1], [15, 0], [15, 0], [15, 0], [0, 0]], [[1, 1], [15, 0], [15, 0], [15, 0], [0, 0]], [[0, 1], [0, 1], [15, 0], [15, 0], [15, 0], [0, 0]]]

# 运行示例
Huffman_code(AC)
