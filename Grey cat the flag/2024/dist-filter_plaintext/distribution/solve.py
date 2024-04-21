from pwn import *  
import os
# r = process(["python3", "filter_plaintext.py"])
r = remote("challs.nusgreyhats.org", 32223)
enc_secret = bytes.fromhex(r.recvlineS().strip().split(":")[1])
iv = bytes.fromhex(r.recvlineS().strip().split(":")[1])

ct = bytes.fromhex(r.recvlineS().strip().split(":")[1])
def send(ct):
	r.sendlineafter(b'> ', ct.hex().encode())
	return bytes.fromhex(r.recvlineS().strip())

def findFirstIV():
	a = b'a'*16
	b = b'b'*16 

	dec_a = send(a)
	dec_b = send(b)
	dec_ab = send(a+b)
	res = xor(dec_ab[16:], xor(dec_a, dec_b))
	res = xor(res, a) 
	return res 
firstIV = findFirstIV()
def findSecretBlock(index):
	a = b'a'*16
	dec_a = xor(send(a), firstIV)
	payload = b''
	for i in range(index+1):
		payload += enc_blocks[i]
	payload += a  
	response = send(payload)
	assert len(response) == 16 
	sec_block = xor(xor(response, dec_a), enc_blocks[index])
	return sec_block

enc_blocks = [enc_secret[i:i+16] for i in range(0,len(enc_secret), 16)]

secret = b''
for i in range(5):
	secret += findSecretBlock(i)
import hashlib
from Crypto.Cipher import AES  
key = hashlib.md5(secret).digest()
cipher = AES.new(key = key, iv = iv, mode = AES.MODE_CBC)
flag = cipher.decrypt(ct)
print(flag)