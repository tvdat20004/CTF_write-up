import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from pwn import *
# connect = remote("group-projection.chal.uiuc.tf", 1337)

while True:
	connect = remote("group-projection.chal.uiuc.tf", 1337)
	data = connect.recvuntil(b'p = ')
	p = int(connect.recvuntil(b'\n').decode().strip())
	# print(p)
	if (p - 1) % 3 == 0:
		g = 2
		data = connect.recvuntil(b'A = ')
		A = int(connect.recvuntil(b'\n').decode().strip())
		data = connect.recvuntil(b'k = ')
		break
	connect.close()

connect.sendline(str((p-1)//3).encode())
data = connect.recvuntil(b'c = ')
c = int(connect.recvuntil(b'\n').decode().strip())
connect.close()
S = 1
key = hashlib.md5(long_to_bytes(S)).digest()

cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(long_to_bytes(c))
print(flag)
# b'uiuctf{brut3f0rc3_w0rk3d_b3f0r3_but_n0t_n0w!!11!!!}\r\r\r\r\r\r\r\r\r\r\r\r\r'
