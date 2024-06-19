from pwn import * 
from Crypto.Util.number import * 

r = remote("challs.bcactf.com", 32542)

for _ in range(3):
	r.sendlineafter(b'Enter text to encrypt: ', b'123')
	r.recvuntil(b'n = ')
	n_ = int(r.recvuntilS(b'\n').strip())

r.sendlineafter(b'(yes or no) ', b'yes')
ct = int(r.recvlineS().strip().split(':')[1])
r.recvline()
exec(r.recvlineS().strip())
p = GCD(n, n_)
r = n // p 
print(long_to_bytes(pow(ct, pow(65537, -1, (p-1)*(r-1)),n)))
