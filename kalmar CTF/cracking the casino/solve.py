from pwn import *
from Crypto.Util.number import * 
from sympy import nextprime
# from sympy.ntheory import discrete_log
def discrete_log(q, g, h, order):
	gi = pow(g, (q-1)//order, q)
	hi = pow(h, (q-1)//order, q)
	for i in range(order):
		if pow(gi, i, q) == hi:
			return i 

while True:
	r = remote("chal-kalmarc.tf", 9)
	# r = process(["python3", "casino.py"])
	r.recvuntil(b'public key for Pedersen Commitment Scheme is:\n')
	exec(r.recvlineS())
	exec(r.recvlineS())
	exec(r.recvlineS())
	# find small factor
	factor = 7
	while True:
		if (q-1) % factor == 0:
			break
		factor = nextprime(factor)
		if factor > 100:
			r.close()
			break
	print(factor)
	if factor:
		# caculate s mod factor
		s = discrete_log(q, g,h,factor)
		print(s)
		if s == 0 :
			break
		else:
			r.close()
	else:
		r.close()

r.sendlineafter(b'what would you like to play?\n[D]ice\n[C]ards', b'd')
i = 0
while True:
	try:
		r.recvuntil(b'Commitment: ')
		commitment = int(r.recvuntilS(b'\n').strip())
		commit = discrete_log(q, g, commitment, factor)
		print(commit)
		i += 1 
		print(i)
		if commit == 1 or commit == 0:
			r.sendlineafter(b'Are you able to guess the value? [Y]es/[N]o', b'n')
		else:
			r.sendlineafter(b'Are you able to guess the value? [Y]es/[N]o', b'y')
			r.sendlineafter(b'whats your guess?', str(commit).encode())
	except:
		print(r.recv(2024))
		break