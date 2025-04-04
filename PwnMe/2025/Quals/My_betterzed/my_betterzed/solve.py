from Crypto.Cipher import AES
from Crypto.Util.number import *
import json
from pwn import xor
from tqdm import trange
import zlib
from openzedlib import openzed

enc_data = open("flag.txt.ozed", "rb").read()
parsed_metadata = json.loads(enc_data.split(b'\0')[0][4:])
enc_flag = zlib.decompress(enc_data[304:])
print(parsed_metadata)
# with open("pt.txt", 'wb') as f:
#     f.write(b'\0' * 32)
enc_data = open("pt.txt.ozed", "rb").read()
enc_data = zlib.decompress(enc_data[304:])
print(xor(enc_data[:16], enc_flag[:16]))