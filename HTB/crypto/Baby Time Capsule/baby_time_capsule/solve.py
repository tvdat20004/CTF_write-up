from sympy.ntheory.modular import crt
import json
from pwn import *
r = remote("206.189.28.180", 32595)
def get_para():
	r.sendlineafter(b'(Y/n) ', b'y')
	get_enc = json.loads(r.recvlineS().strip())
	c = int(get_enc["time_capsule"], 16)
	# print(type(n))
	n = int(get_enc["pubkey"][0], 16)
	return n,c 

n = []
ct = []
for _ in range(3):
	n_, c_ = get_para()
	n.append(n_)
	ct.append(c_)
print(n)
print(ct)
flag_pow = crt(n,ct)[0]
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(iroot(flag_pow,5)[0]))