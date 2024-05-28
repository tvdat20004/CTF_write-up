from pwn import * 
from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot
from tqdm import trange
# r = process(["python3", "random_rabin.py"])
r = remote("challs.actf.co", 31300)
for i in trange(64):
	n = int(r.recvlineS().strip().split(':')[1])
	pt = int(r.recvlineS().strip().split(':')[1])
	secret = iroot(pow(pt, 2, n), 2)
	assert secret[1]
	secret = long_to_bytes(int(secret[0]))
	r.sendlineafter(b'gimme the secret:', secret.hex().encode())

r.interactive()
