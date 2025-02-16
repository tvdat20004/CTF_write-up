from pwn import * 
from Crypto.Util.number import * 
r = remote("chall.lac.tf", 31171)

exec(r.recvlineS().strip())
exec(r.recvlineS().strip())
exec(r.recvlineS().strip())
while True:
	r.sendlineafter(b'> ', b'1')
	response = int(r.recvlineS().strip())
	if response != 1 and response != N-1:
		p = GCD(response + 1,N)
		q = N // p 
		print(long_to_bytes(pow(ct,pow(e,-1,(p-1)*(q-1)),N)))
		break