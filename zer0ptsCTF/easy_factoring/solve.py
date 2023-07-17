from pwn import *
from Crypto.Util.number import isPrime
from sage.all import *

while True:
	r = remote("crypto.2023.zer0pts.com", 10333)
	data = r.recvuntil(b'N:')
	n = int(r.recvline().decode().strip())
	try:
		p,q = two_squares(n)
	except:
		r.close()
		continue

	if isPrime(int(p)) and isPrime(int(q)):
		data = r.recvuntil(b'p: ')
		r.sendline(str(int(p)).encode())
		data = r.recvuntil(b'q: ')
		r.sendline(str(int(q)).encode())
		flag = r.recv(2024)
		print(flag)
		r.close()
		break
	else:
		r.close()

