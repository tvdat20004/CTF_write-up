from pwn import *
import base64
from Crypto.Util.number import isPrime
r = remote("flu.xxx", 10010)
# r.recvline()
# # flag_base64 = base64.b64decode(r.recvlineS())
# # iv, flag_enc = flag_base64[:16], flag_base64[16:] 

for i in range(42):
	if isPrime(2**i - 1):
		t = i
		s = (2**(t-1))*(2**(t)-1)
		if 20000 < s < 150000000000:
			break

r.sendlineafter(b'You know the moment when you have this special number that gives you luck? Great cause I forgot mine\n', str(s).encode())
r.sendlineafter(b"I also had a second lucky number, but for some reason I don't remember it either :(\n", str(t).encode())

r.interactive()
