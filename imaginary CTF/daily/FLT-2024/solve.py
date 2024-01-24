from Crypto.Util.number import * 
from pwn import * 
# r = process(["python3", "chall.py"])
r = remote("155.248.203.119",42046)
r.recvuntilS(b'=')
N = int(r.recvuntilS(b'\n'))
while True:
	e = getPrime(2024)
	if e < N:
		break
r.sendlineafter(b'e = ', str(e).encode())
c = int(r.recvlineS().strip().split('=')[1])
m = pow(c,pow(e,-1,N-1),N)
print(long_to_bytes(m))