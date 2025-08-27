from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import xor
import json 
cc = dict()
key = b'1' * 16
iv = b'1' * 16

enc = bytes.fromhex('36363dd41383bde4b70d1710c6fbe0305e2acc4f5a22b95d9d6ab69595f765bcecacbd29e9efc14639d975b3d18583cc58611836351e8a7f7c034fe3626759a2ea2ab06543411630fa29621f960cb1d5')

cc['username'] = 'dat'
cc['class'] = '10'
cc['bookname'] = 'a' * 21

cc['is_admin'] = 0
dumps = json.dumps(cc).replace(' ', '').encode()
# enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(dumps, 16))

blocks = [dumps[i:i+16] for i in range(0, len(dumps), 16)]
enc_blocks = [enc[i:i+16] for i in range(0, len(enc), 16)]
print(enc_blocks)
idx = blocks[-1].index(b'0')
print(blocks)
print(idx)
payload = bytearray(b'\x00' * 16)
payload[idx] = ord('1') ^ ord('0')
enc_blocks[-2] = xor(enc_blocks[-2],payload)

print(b''.join(enc_blocks).hex())
# print(AES.new(key, AES.MODE_CBC, iv).decrypt(b''.join(enc_blocks)))
# blocks[-2] = (xor(b'1', b'0') )