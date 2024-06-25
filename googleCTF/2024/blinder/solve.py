from ecdsa import numbertheory 
from sage.all import *
from Crypto.Random import random
import hashlib
import ast
from pwn import *
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
K = GF(p)
a = K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
b = K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
E = EllipticCurve(K, (a, b))
def H(id):
	hash = hashlib.sha256(f'id={id}'.encode()).digest()
	x = int.from_bytes(hash, 'big')

	while True:
		y2 = (x**3 + a*x + b) % p
		if numbertheory.jacobi(int(y2), p) == 1:
			break
		x += 1

	y = numbertheory.square_root_mod_prime(int(y2), p)
	return E(x, y)
r = remote("blinders.2024.ctfcompetition.com" ,1337)
# r = process(["python3", "chall.py"])

def handle(x,y):
	payload = f"handle {x} {y}"
	r.sendline(payload.encode())
	eids = eval(r.recvlineS().strip())
	deid = eval(r.recvlineS().strip())
	# eids = eval(r.recvlineS().strip().replace("mpz", ""))
	# deid = eval(r.recvlineS().strip().replace("mpz", ""))
	return [E(*eid) for eid in eids], E(*deid)

def submit(S):
	hash = hashlib.sha256(','.join(map(str, S)).encode()).hexdigest()
	r.sendline(f'submit {hash}'.encode())
	return r.recvlineS()

print(r.recvlineS())
n = 256
id_points = [H(id) for id in range(n)]
# ss = [i * 10 for i in id_points]
eids_even = sum(id_points[::2])
eids_odd = sum(id_points[1::2])
for i in range(16):
	eid1, d_even = handle(*eids_even.xy())
	eid2, d_odd = handle(*eids_odd.xy())
	value1 = d_even + d_odd - sum(eid1)
	value2 = d_even + d_odd - sum(eid2)
	for i in range(n):
		full = eid1[:i] + [value1] + eid1[i:]
		full2 = eid2[:i] + [value2] + eid2[i:]

		if (sum(full[::2]) == d_even and sum(full[1::2]) == d_odd) or (sum(full2[::2]) == d_even and sum(full2[1::2]) == d_odd):
			print(i)
			arr = list(range(n))
			arr.remove(i)
			submit(arr)
			break
r.interactive()

