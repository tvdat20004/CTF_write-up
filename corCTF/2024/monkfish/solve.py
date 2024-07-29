from sage.all import *
from pwn import * 
from hashlib import sha256
m=100
n = 100


def apply(F, v):
    out = []
    for i in range(m):
        out.append((v.T * F[i] * v)[0, 0])
    return matrix(FF, m, 1, out)

def create_pok(v, s, F):
    t = matrix(FF, n, 1, [FF.random_element() for i in range(n)])

    com = apply(F, t)
    verif = apply_verif_info(F, t, s)
    a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
    # a = 0
    return (com, t - a * s, verif)

def apply_verif_info(F, a, b):
    out = []
    for i in range(100):
        out.append((a.T * (F[i] + F[i].T) * b)[0, 0])
    return matrix(FF, 100, 1, out)
while True:
	# io = process(["sage", "server.sage"])
	io = remote("be.ax", 31105)
	io.recvline()
	com = eval(io.recvlineS().strip().split('=')[1])
	resp = eval(io.recvlineS().strip().split('=')[1])
	verif = eval(io.recvlineS().strip().split('=')[1])
	# print(io.recvlineS())

	io.recvline()
	seed = eval(io.recvlineS().strip().split('=')[1])
	v = eval(io.recvlineS().strip().split('=')[1])

	F = []
	seed = bytes(seed)	

	FF = GF(5)
	com = matrix(FF, 100, 1, com)
	verif = matrix(FF,100, 1,verif)
	v = matrix(FF, 100, 1, v)
	resp = matrix(FF, 100, 1, resp)

	for i in range(100):
	    cur = []
	    for j in range(100):
	        cur.append([])
	        for k in range(100):
	            cur[-1].append(list(FF)[sha256(seed).digest()[0] % 5])
	            seed = sha256(seed).digest()
	    F.append(matrix(FF, 100, 100, cur))

	a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
	print(a)
	if a != 0:
		io.close()
		continue
	mat = []
	for k in range(100):
		tmp = resp.T * (F[k] + F[k].T) 
		mat.append(list(tmp[0]))
	mat = matrix(FF, mat)
	try:
		s = (~mat) * verif
	except:
		io.close()
		continue
	pok = create_pok(v, s, F)
	m0 = [i[0] for i in list(pok[0])]
	m1 = [i[0] for i in list(pok[1])]
	m2 = [i[0] for i in list(pok[2])]
	print(m0)
	print(m1)
	print(m2)

	io.sendlineafter(b'm0 =', str(m0).encode())
	io.sendlineafter(b'm1 =', str(m1).encode())
	io.sendlineafter(b'm2 =', str(m2).encode())
	io.interactive()