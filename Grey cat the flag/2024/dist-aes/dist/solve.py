from aes import *
from pwn import * 
relation = [5, 14, 7, 12, 9, 2, 11, 0, 13, 6, 15, 4, 1, 10, 3, 8]
# r = process(['python3', 'server.py'])
r = remote("challs.nusgreyhats.org" ,35100)

plaintext = b''
for i in range(256):
	plaintext += bytes([i])*16

r.sendlineafter(b'm: ', plaintext.hex().encode())
ct = bytes.fromhex(r.recvlineS().strip().split(':')[1])
password_enc = bytes.fromhex(r.recvlineS().strip().split(':')[1])
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
lookup = [{} for _ in range(16)]
for i in range(256):
	for j in range(16):
		lookup[j][blocks[i][j]] = i 
# print(lookup)
password = [0]*16
def mix(p):
	ret = []
	for i in range(0,16,4):
		x = p[i:i+4]
		x[0], x[1], x[2], x[3] = x[2], x[3], x[0], x[1]
		ret += x  
	return ret
	
for i in range(16):
	password[i] = lookup[relation[i]][password_enc[relation[i]]]

password = mix(password)
r.sendlineafter(b'password: ', bytes(password)	.hex().encode())
r.interactive()
