
def binary_to_bytes(binary_str):
    # Ensure the binary string length is a multiple of 8
    if len(binary_str) % 8 != 0:
        raise ValueError("The binary string length must be a multiple of 8.")

    # Convert the binary string to an integer
    integer_value = int(binary_str, 2)

    # Calculate the number of bytes needed
    num_bytes = len(binary_str) // 8

    # Convert the integer to a bytes object
    byte_array = integer_value.to_bytes(num_bytes, byteorder='big')

    return byte_array

# Example usage
binary_str = "00000001"
byte_array = binary_to_bytes(binary_str)
print(byte_array)  # Output: b'\xc9\x96'

""" 
hex_string = '001f0000010501010101010100000000000000808182838485868788898a8b'
'00281001010101000300020202020204000000808f817f7e82837d847c8586877a7b898a79888b8d'

# 將十六進制字符串轉換為字節串
byte_string = bytes.fromhex(hex_string)

# 轉換為類似的格式
formatted_string = str(byte_string)

print(byte_string)
 """