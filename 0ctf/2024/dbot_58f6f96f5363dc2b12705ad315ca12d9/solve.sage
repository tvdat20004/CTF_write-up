# from sage.all import * 
import os
os.environ['PWNLIB_NOTERM'] = '1'
os.environ['TERM'] = 'xterm-256color'
from pwn import * 
from tqdm import trange
import sys
sys.path.append("/mnt/e/tvdat20004/CTF/tools/attacks/hnp")

from lattice_attack import * 

def hnp_sum(A, E, T, mod):
	"""
	Solves the HNP-SUM problem.
	The HNP-SUM problem is defined as finding y such that Ai = Ti * x + ei mod m.
	:param A: the Ai values
	:param E: abs(ei) <= E
	:param T: abs(ti) <= T
	:param mod: the modulus
	:return: a list of Ti (maybe -Ti) values
	"""
	M = matrix(ZZ, len(A)+1, len(A)+1)
	for i in range(0, len(A)):
		M[i, -1] = T*A[i]
		M[i, i] = E
	M[-1, -1] = T*mod
	M = M.LLL()
	K = M.submatrix(row=0, col=0, nrows=len(A) - 1, ncols=len(A)).right_kernel()
	q = K.an_element()
	return q

def Level0():
	io.sendlineafter(b'Choose one prime you prefer: ', b'2')
	mod = int(io.recvlineS().strip().split(':')[1])
	c = int(io.recvlineS().strip().split('=')[1]) 
	N = int(io.recvlineS().strip().split('=')[1]) 
	ai = []
	# print(io.recvlineS().strip())
	# print(io.recvlineS().strip())

	for i in range(80):
		x0 = int(io.recvlineS().strip().split('=')[1]) 
		x1 = int(io.recvlineS().strip().split('=')[1]) 
		io.sendlineafter(b'Give me v: ',str(x0).encode())
		m0 = int(io.recvlineS().strip().split('=')[1]) 
		m1 = int(io.recvlineS().strip().split('=')[1]) 
		ph12 = ((m0 + m1) - pow(x0 - x1, pow(65537, -1, mod - 1), mod)) % mod 
		ai.append([ph12])
	b = [0]*80
	candidate = []
	for _, y in attack(ai, b, mod, 2**497):
		candidate.append(pow(y[0], -1, mod))
	print(candidate)
	x = Zmod(N//mod)['x'].gen()
	f = candidate[0] - x
	root = f.monic().small_roots(X=2**248, beta=0.499, epsilon=0.012)[0]
	print(root)
	p1 = ZZ(candidate[0] - root)
	p0 = ZZ(N//(mod*p1))
	phi = (mod -1)*(p1-1)*(p0- 1)
	m = pow(c, pow(65537, -1, int(phi)), N)
	io.sendlineafter(b'Give me m: ', str(m).encode())
	if b'Good job!' in io.recvline():
		return 1
	else:
		return 0
def Level1():
	io.sendlineafter(b'Choose one prime you prefer: ', b'3')
	mod = int(io.recvlineS().strip().split(':')[1])
	c = int(io.recvlineS().strip().split('=')[1]) # c
	N = int(io.recvlineS().strip().split('=')[1]) # c
	ai = []
	ph1 = []
	ph2 = []
	# print(io.recvlineS().strip())
	for i in range(80):        
		x0 = int(io.recvlineS().strip().split('=')[1]) 
		x1 = int(io.recvlineS().strip().split('=')[1])
		io.sendlineafter(b'Give me v: ',str(x0).encode())
		m0 = int(io.recvlineS().strip().split('=')[1]) # c
		m1 = int(io.recvlineS().strip().split('=')[1]) # c
		ph1.append(m0)
		ph2.append((m1 - pow(x0 - x1, pow(65537, -1, mod - 1), mod)) % mod)
	ai = []
	for i in range(1, 80):
		ai.append(((ph1[i] - ph2[i]) - (ph1[0] - ph2[0])) % mod)
	E = 2**231
	ai_a0 = hnp_sum(ai, E, 2**160, mod)
	sus1 = (ai[0] * pow(2*int(ai_a0[0]), -1, mod)) % mod 
	sus2 = (-sus1) % mod 
	x = Zmod(N // mod)['x'].gen()
	fx1 = sus1 - x
	fx2 = sus2 - x
	root1 = fx1.monic().small_roots(X=2**161, beta=0.33, epsilon=0.008)
	root2 = fx2.monic().small_roots(X=2**161, beta=0.33, epsilon=0.008)
	print(root1)
	print(root2)
	assert len(root1) + len(root2) == 1
	if len(root1):
		sum_a1_a0 = int(root1[0]) - 1
		a0 = (sum_a1_a0 - int(ai_a0[0]))//2
		p1 = sus1 - int(root1[0])
		p0 = (ph1[0] * pow(p1 + a0, -1, mod) - a0) % mod 
	elif len(root2):
		sum_a1_a0 = int(root2[0]) - 1
		a0 = (sum_a1_a0 + int(ai_a0[0]))//2
		p1 = sus2 - int(root2[0])
		p0 = (ph1[0] * pow(p1 + a0, -1, mod) - a0) % mod 
	print(p0)
	print(p1)
	assert N %(p1*p0) == 0
	p2 = N // (p1*p0*mod)
	m = pow(c, pow(65537, -1, (p0-1)*(p1-1)*(p2-1)*(mod-1)), N)
	io.sendlineafter(b'Give me m: ', str(m).encode())
	if b'Good job!' in io.recvline():
		return 1
	else:
		return 0
while True:
	io = process(["python3", "task.py"])
	io.recvline()
	try:
		if Level0() and Level1():
			io.interactive()
		else:
			continue
	except:
		continue