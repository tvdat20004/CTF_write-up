from Crypto.Util.number import *
from sage.all import Mod
def solve_quadratic_zmod(a, b, c):
	mod = 2**512
	delta = (b**2 - 4*a*c) % mod 
	sqrt_delta = Mod(delta, mod).nth_root(2, all=True)
	assert len(sqrt_delta) > 0
	roots = []
	for s in sqrt_delta:
		s = int(s)
		x0 = (((-b + s)% mod) // 2) * pow(a, -1, mod) % mod
		x1 = (((-b - s)% mod) // 2) * pow(a, -1, mod) % mod
		if (a*x0**2 + b*x0 + c) % mod == 0 and (a*x1**2 + b*x1 + c) % mod == 0:
			roots.append((x0, x1))
	return roots
def get_param():
	from pwn import remote
	io = remote("chall.lac.tf", 31175)
	io.recvline()
	a = int(io.recvlineS().strip().split('=')[1])
	c = int(io.recvlineS().strip().split('=')[1])
	m = int(io.recvlineS().strip().split('=')[1])
	n = int(io.recvlineS().strip().split('=')[1])
	ct = int(io.recvlineS().strip().split('=')[1])
	io.close()
	return a, c, m, n, ct

while 1:
	a, c, m, n, ct = get_param()
	diff = 1
	while 1:
		_a = pow(a, diff, m)
		_b = c * (a**diff - 1)//(a - 1) % m 
		_c = (-n) % m 
		try:
			roots = solve_quadratic_zmod(_a, _b, _c)
			print(diff)
			for root in roots:
				x0, x1 = root
				if n % x0 == 0:
					p = x0
				elif n % x1 == 0:
					p = x1
				else:
					continue
				q = n // p 
				phi = (p-1)*(q-1)
				print(long_to_bytes(pow(ct, pow(65537, -1, (p-1)*(q-1)), n)))
				quit()
			if diff < 1500:
				diff += 1
			else:
				break
		except:
			if diff < 1500:
				diff += 1
			else:
				break