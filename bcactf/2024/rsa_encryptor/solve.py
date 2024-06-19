from sympy.ntheory.modular import crt
from pwn import * 
from gmpy2 import iroot 
from Crypto.Util.number import long_to_bytes
r = remote("challs.bcactf.com", 32666)

cts = []
ns = []
r.recvline()
ct, n = eval(r.recvlineS().strip())
cts.append(ct)
ns.append(n)
def decrypt():
	m3 = crt(ns, cts)[0]
	m, check = iroot(m3, 3)
	if check:
		return long_to_bytes(m)
	else:
		return None

while True:
	if not decrypt():
		r.sendlineafter(b"(y/n) ", b'n')
		ct, n = eval(r.recvlineS().strip())
		cts.append(ct)
		ns.append(n)
	else:
		print(decrypt())
		break