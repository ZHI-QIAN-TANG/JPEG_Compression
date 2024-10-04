def rle_encode_ac_coefficients(ac_coefficients):
    """
    对输入的 AC 係數列表进行 RLE 编码。

    参数:
    - ac_coefficients: 经过 Zigzag 扫描后的 AC 係數列表（长度为 63，因为 DC 係數不包括在内）

    返回:
    - RLE 编码后的列表，包含 `(RunLength, Value)` 对
    """
    rle_result = []
    zero_count = 0

    for coeff in ac_coefficients:
        if coeff == 0:
            zero_count += 1

            # 如果0的个数达到16个，插入一个 (15, 0) 并重置计数器
            if zero_count == 16:
                rle_result.append((15, 0))
                zero_count = 0
        else:
            # 存储 (RunLength, Value) 对
            rle_result.append((zero_count, coeff))
            zero_count = 0

    # 最后添加 EOB 标记 (0, 0) 如果序列尾部还有 0
    if zero_count > 0:
        rle_result.append((0, 0))

    return rle_result

ac_coefficients = [0] * 63

encoded_ac = rle_encode_ac_coefficients(ac_coefficients)
print(encoded_ac)
