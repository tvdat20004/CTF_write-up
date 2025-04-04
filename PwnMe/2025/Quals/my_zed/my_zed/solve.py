from Crypto.Cipher import AES
from Crypto.Util.number import *
import json
from tqdm import trange
import zlib
from openzedlib import openzed

from hashlib import sha256
def brute_force(start, end, password, password_hash):
    for i in trange(start, end):
        if sha256(password + long_to_bytes(i)).digest() == password_hash:
            return long_to_bytes(i)
    return None

enc_data = open("flag.txt.ozed", "rb").read()
parsed_metadata = json.loads(enc_data.split(b'\0')[0][4:])
ct = zlib.decompress(enc_data[304:])
iv = ct[:16]
password = iv[3:]
password_hash = bytes.fromhex(parsed_metadata["password_hash"])

# for i in trange(256**3):
#     if sha256(password + long_to_bytes(i)).digest() == password_hash:
#         password = password + long_to_bytes(i)
#         print(password.hex())
#         break
password = bytes.fromhex('fcca965b7560d92483a4d66b4c80b974')
file = openzed.Openzed(b'zed', password, 'flag.txt', 63)
print(file.decrypt(ct))