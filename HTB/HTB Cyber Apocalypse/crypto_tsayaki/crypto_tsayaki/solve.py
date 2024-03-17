from pwn import * 
from tea import Cipher
from Crypto.Util.number import * 
from Crypto.Util.Padding import pad
import os
def decrypt_block(block, key):
	mask = 1<<32
	K = [bytes_to_long(key[i:i+4]) for i in range(0, len(key), 4)]
	delta = 0x9e3779b9
	m0 = bytes_to_long(block[:4])
	m1 = bytes_to_long(block[4:])
	s = 32 * delta
	for i in range(32):
		m1 -= ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3]) 
		m1 %= mask 
		m0 -= ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
		m0 %= mask 
		s -= delta
	return long_to_bytes(m0) + long_to_bytes(m1)

def find_iv(key, ct, pt):
	block_ct = [ct[i:i+8] for i in range(0,len(ct),8)]
	block_pt = [pt[i:i+8] for i in range(0, len(pt), 8)]
	pt_iv = decrypt_block(block_ct[0], key)
	iv = xor(pt_iv, block_pt[0])
	return iv 
# r = process(["python3", "server.py"]) 
r = remote("94.237.50.175", 36573)

r.recvuntil(b'Here is my special message:')

mess = bytes.fromhex(r.recvuntilS(b'\n').strip())
r.sendlineafter(b"Enter your target ciphertext (in hex) :", b'0000')
r.sendlineafter(b'Enter your encryption key (in hex) :', b'0'*32)
# r.recvlineS()
enc = bytes.fromhex(r.recvlineS().strip().split()[5])
key = b'\0'*16
r.close()
iv = find_iv(key, enc, mess)
print(iv)
def generate_equivalent_keys(key):
	K = [bytes_to_long(key[i:i+4]) for i in range(0, len(key), 4)]
	key1 = b"".join(map(long_to_bytes, [K[0] ^ (1<<31), (K[1]^ (1<<31)), K[2], K[3]]))
	key2 = b"".join(map(long_to_bytes, [K[0], K[1], K[2] ^ (1<<31), K[3] ^ (1<<31)]))
	key3 = b"".join(map(long_to_bytes ,[K[0] ^ (1<<31), (K[1] ^ (1<<31)), (K[2]^(1<<31)), K[3] ^ (1<<31)]))
	return key, key1, key2, key3
r = remote("94.237.50.175", 36573)
# r = process(["python3", "server.py"]) 
r.recvuntil(b'Here is my special message:')
mess = bytes.fromhex(r.recvuntilS(b'\n').strip())

for i in range(10):

	key = os.urandom(16)
	equivalent_keys = generate_equivalent_keys(key)
	ct0 = Cipher(equivalent_keys[0], iv).encrypt(mess)
	ct1= Cipher(equivalent_keys[1], iv).encrypt(mess)
	ct2 = Cipher(equivalent_keys[2], iv).encrypt(mess)
	ct3 = Cipher(equivalent_keys[3], iv).encrypt(mess)
	print(ct0.hex())
	print(ct1.hex())
	print(ct2.hex())
	print(ct3.hex())
	r.sendlineafter(b"Enter your target ciphertext (in hex) :", ct0.hex().encode())
	for j in range(4):
		# print(long_to_bytes(equivalent_keys[j], 32).hex()[2:])
		# print(equivalent_keys[j])
		r.sendlineafter(b'Enter your encryption key (in hex) :',equivalent_keys[j].hex().encode())

r.interactive()
# mess = os.urandom(20)

# iv = b'1'*8
# key = os.urandom(16)
# K = [bytes_to_long(key[i:i+4]) for i in range(0, len(key), 4)]
# print(bin(K[2]).zfill(32))
# K[2] ^= (1<<31)
# print(bin(K[2]).zfill(32))

# K[3] ^= (1<<31)
# key1 = b"".join([long_to_bytes(K[i], 4) for i in range(4)])
# assert key!=key1
# print(Cipher(key, iv).encrypt(mess).hex())
# print(Cipher(key1, iv).encrypt(mess).hex())
