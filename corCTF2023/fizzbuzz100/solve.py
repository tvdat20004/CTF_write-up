from pwn import *
from Crypto.Util.number import long_to_bytes

while True:
	r = remote("be.ax", 31100)
	
	data = r.recvuntil(b'n = ')
	n = int(r.recvline().decode().strip())
	data = r.recvuntil(b'ct = ')
	ct = int(r.recvline().decode().strip())
	e = 65537
	print(n)
	print(ct)
	send = ct * pow(2,e,n) % n
	data = r.recvuntil(b'> ')
	r.sendline(str(send).encode())
	# x = r.recvline()
	try:
		flag = int(r.recvline().decode().strip())
		print(long_to_bytes(flag//2))
		r.close()
		break
	except:
		r.close()
