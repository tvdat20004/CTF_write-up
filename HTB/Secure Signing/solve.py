from pwn import *  
from hashlib import sha256
from tqdm import trange

r = remote("167.99.85.216", 32672)

def sign(message : bytes):
	r.sendlineafter(b'>', b'1')
	r.sendlineafter(b"Enter your message: ", message)
	hash = r.recvlineS().split(':')[1].strip()
	return hash 
def find_length():
	length = 4
	while True:
		cur_sign = sign(b'\x00' * length)
		check_sign = sign(b'\x00' * (length + 1))
		if cur_sign == check_sign:
			break
		else:
			length += 1
		print(length)
	return length

# length = find_length()
length = 58	
flag = b'HTB{'
print(length)
for _ in range(length - 4):
	for i in trange(31,127):
		send = flag + bytes([i]) 
		# send = b'H'	
		# print(send)
		sample_sign = sha256(len(send) * b'\x00').hexdigest()
		# print(sign(send))
		# print(sample_sign)
		if sign(send) == sample_sign:
			flag = send
			print(flag)
			break
print(flag)