import time
from Crypto.Cipher import AES 
from tqdm import trange
def get_random_number():
    global seed 
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed

def gen_key():
    key = b''
    for i in range(8):
        key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
    return key
# enc = bytes.fromhex("2134a04b2693402ea3d334e88b39e393b68d9d258dd163fea1d57096d34658a19c558e9e893f0635eb27de90e206769e")
enc = bytes.fromhex("2421ea9587244c9a3ad7cc04fc1c402044f7eaa76a15407c97122e7db0484a4e")
for seed in trange(10**6):
    key = gen_key()
    key = gen_key()
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(enc)
    try:
        print(flag.decode())
    except:
        continue