from pwn import * 
from tqdm import trange
r = remote("chal.amt.rs", 1414)
# r = process(["python3", "faked-onion.py"])
def encrypt(pt):
	r.sendlineafter(b'> ', b'1')
	r.sendlineafter(b'Enter your message in hex: ', pt)
	enc = bytes.fromhex(r.recvlineS().strip())
	return enc 
def getEncryptedFlag():
	r.sendlineafter(b'> ', b'2')
	return bytes.fromhex(r.recvlineS().strip())

hmac_byte = []

# for i in trange(256):
# 	payload = hex(i)[2:].zfill(32)
# 	hmac_byte.append(encrypt(payload.encode())[:-1])
flag = b""
encrypted_flag = getEncryptedFlag()
blocks = [encrypted_flag[i:i+16] for i in range(0, len(encrypted_flag), 16)]
for block in blocks:
	payload = hex(block[0])[2:].zfill(32)
	print(payload)
	hmac = encrypt(payload.encode())[1:]
	flag += xor(hmac, block[1:]) + bytes([block[0]])
	print(xor(hmac, block[1:]))
print(flag)