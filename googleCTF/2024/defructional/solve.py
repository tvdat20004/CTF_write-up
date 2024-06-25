from pwn import xor
from Crypto.Cipher import DES3
mask = b'\xff'*24

# pt = bytes.fromhex("123456ABCD132536")
# key = bytes.fromhex("2ABB09182736CCDD")
import os 
pt = os.urandom(8)
key = os.urandom(24)
cipher = DES3.new(key, DES3.MODE_ECB)
cipher1 = DES3.new(xor(mask, key), DES3.MODE_ECB)
pt1 = cipher.encrypt(pt)
pt2 = cipher1.encrypt(xor(mask[:8], pt))
print(xor(pt1, pt2))




# import random
# flipped_bits = set(range(0, 192, 8))
# for i in range(128):
#     if len(flipped_bits) == 192:
#         flipped_bits = set(range(0, 192, 8))
#     remaining = list(set(range(192)) - flipped_bits)
#     num_flips = random.randint(1, len(remaining))
#     flipped_bits = flipped_bits.union(random.choices(remaining, k=num_flips))
#     # print(192 - len(flipped_bits))
#     if 192 - len(flipped_bits) == 1:
#         print(1)
