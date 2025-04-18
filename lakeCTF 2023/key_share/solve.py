from sage.all import * 
from pwn import * 
from random import randint
from tqdm import trange
import ast
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1

# revcive pub 
E = EllipticCurve(GF(p),[a,b])
r = process(["python3", "chal.py"])
r.recvuntil(b"Alice's public key is ")
pub = ast.literal_eval(r.recvuntilS(b'\n'))
EC_candidate = []
for i in trange(4):
	while True:
		b = randint(1,p-1)
		ec = EllipticCurve(GF(p), [a,b])
		order = ec.order()
		# print(list(factor(order)))
		factors = [f[0] for f in list(factor(order))]
		breaker = 0
		for fac in factors:
			if 42 <= int(fac).bit_length() <= 48:
				EC_candidate.append((ec, fac))
				breaker = 1
				break
		if breaker:
			break
def send_point(point):
	x = point.xy()[0]
	y = point.xy()[1]
	r.sendlineafter(b"Gimme your pub key's x : \n", str(x).encode())
	r.sendlineafter(b"Gimme your pub key's y : \n", str(y).encode())
	r.recvline()
	return ast.literal_eval(r.recvlineS().strip())

s_pk = []
for i in range(4):
	print(1)
	# print(ec[i])
	# print(ec[i][0].order())

	# print(ec[i][0].order() // int(ec[i][1]))
	point = EC_candidate[i][0].gen(0) * (EC_candidate[i][0].order() // EC_candidate[i][1])
	assert point.order() == EC_candidate[i][1]
	shared_key = EC_candidate[i][0](*(send_point(point)))
	s_pk = point.discrete_log(shared_key)
	print(s_pk)
pk = crt(s_pk, [EC_candidate[i][1] for i in range(4)])
print(pk)
r.close()