from Crypto.Util.number import * 
from pwn import * 
from tqdm import trange
io = process(["python3", "kRSA.py"])
io.recvline()
n = int(io.recvlineS().strip().split('=')[1])
e = int(io.recvlineS().strip().split('=')[1])
io.recvline()
ck = int(io.recvlineS().strip().split('=')[1])

saved = []
for i in trange(1, 2**16):
	saved.append(ck * pow(i, -e, n) % n)
for i in trange(2**15, 2**20):
	x = pow(i, e, n)
	if x in saved:
		secret = i * (saved.index(x) + 1) 
		assert pow(secret, e, n) == ck 
		io.sendlineafter(b'Secret key ? ', str(secret).encode())
		print(io.recvlineS())
		exit(0)

