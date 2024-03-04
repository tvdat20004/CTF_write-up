# import binascii
# # enc = binascii.unhexlify('06c3abc49dc4b443ca9d65c8b0c386c4b0c99fc798c2bdc5bccb94c68c37c296ca9ac29ac790c4af7bc585c59d')
# enc = bytes.fromhex('c8ba2dc79cc8a4ca9dc895c6a507c7bac59bc8bbc8b62c77c9a0c8b001cb87c58bc3a7c5b0c987c29ec9b1cab411')

# from Crypto.Util.number import long_to_bytes
# encoded_value = 0
# for b in enc:

# 	encoded_value += 727*encoded_value + b
# print(encoded_value)
# # print(long_to_bytes(encoded_value))
import binascii

def decode_base_727(encoded_string):
    base = 727
    encoded_value = 0
    for char in encoded_string:
        encoded_value = encoded_value * base + ord(char)
    return encoded_value

output_hex = '06c3abc49dc4b443ca9d65c8b0c386c4b0c99fc798c2bdc5bccb94c68c37c296ca9ac29ac790c4af7bc585c59d'
binary_data = binascii.unhexlify(output_hex)
encoded_string = binary_data.decode('utf-8')
print(encoded_string)
encoded_value = decode_base_727(encoded_string)
flag = ''
while encoded_value > 0:
    flag = chr(encoded_value % 256) + flag
    encoded_value //= 256
print(flag)
