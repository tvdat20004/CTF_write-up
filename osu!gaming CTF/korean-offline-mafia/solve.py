from pwn import *  
from sympy.ntheory import sqrt_mod
from mt19937predictor import MT19937Predictor
from tqdm import trange
r = remote('chal.osugaming.lol',7275)
# r = process(["python3" ,"server.py"])
# bypass POW
r.recvline()
PoW = r.recvlineS()
print(PoW)
sol = input("Solution: ")
r.sendlineafter(b'solution: ', sol.encode())
exec(r.recvlineS().strip())
exec(r.recvlineS().strip())
predictor = MT19937Predictor()
for i in range(624):
	# print(i)
	r.sendlineafter(b'Pick a random r, give me x = r^2 (mod n): ', b'1')
	mask = int(r.recvlineS().strip().split()[-1], 2)
	predictor.setrandbits(mask, 32)
	r.sendlineafter(b'Now give me r*product of IDs with mask applied: ', b'1')
print(r.recvline())
for i in range(10):
	predicted_mask = '{:032b}'.format(predictor.getrandbits(32))
	val = 1
	for j in range(32):
		if predicted_mask[j] == '1':
				val = (val * vs[j]) % n
	x = pow(val, -1, n)
	r.sendlineafter(b'Pick a random r, give me x = r^2 (mod n): ', str(x).encode())

	mask = r.recvlineS().strip().split()[-1]
	assert mask == predicted_mask
	r.sendlineafter(b'Now give me r*product of IDs with mask applied: ', b'1')

r.interactive()
