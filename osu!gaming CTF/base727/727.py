import binascii

# flag = open('flag.txt').read()
flag = 'osu{test_flag93i219i3921i39123}'
def encode_base_727(string):
    base = 727
    encoded_value = 0

    for char in string:
        encoded_value = encoded_value * 256 + ord(char)
    print(encoded_value)
    encoded_string = ""
    while encoded_value > 0:
        encoded_string = chr(encoded_value % base) + encoded_string
        encoded_value //= base

    return encoded_string

encoded_string = encode_base_727(flag)
print(encoded_string)
print(binascii.hexlify(encoded_string.encode()))
