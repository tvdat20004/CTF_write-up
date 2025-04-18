from pwn import * 
import string
from math import gcd, prod
from sympy import primerange
from sympy.ntheory.modular import crt
from base64 import b64decode
from functools import reduce
class LCG:
	def __init__(self,a,c,m,seed):
		self.a = a
		self.c = c
		self.m = m
		self.state = seed

	def next(self):
		self.state = (self.a * self.state + self.c) % self.m
		return self.state

def recover_lcg_param(states):
	T = [states[i] - states[i-1] for i in range(1, len(states))]
	mod = abs(reduce(gcd, [T[i]**2 - T[i - 1] * T[i + 1] for i in range(1, len(T) - 1)]))
	while mod.bit_length() > 64:
		divisor = 2 
		while mod % divisor:
			divisor += 1 
		mod //= divisor
	a = 0
	for i in range(1, len(T)):
		try:
			a = T[i] * pow(T[i-1], -1, mod) % mod 
			break
		except:
			continue
	if a == 0:
		return None
	c = (states[1] - a*states[0]) % mod
	return a, c, mod

def encrypt_msg(msg):
	io.sendlineafter(b'> ', b'1')
	io.sendlineafter(b'Ok. What do you have to say?\n',msg.encode())
	response = io.recvlineS().strip()
	if 'hack' in response:
		return None
	else:
		return response.split(': ')[1]
def determine_state(msg, enc_msg):
	l = len(msg)
	state = []
	for i in range(l):
		pos = msg.index(enc_msg[i])
		state.append(pos)
	return state
times = 1
def decrypt_msg(L, enc):
	l = len(enc)
	permutation = []
	chosen_nums = set()
	while len(permutation) < l:
		x = L.next()
		pos = x % l
		if pos not in chosen_nums:
			permutation.append(pos)
			chosen_nums.add(pos)
	msg = [None] * l
	for i in range(l):
		msg[permutation[i]] = enc[i]
	assert all(msg)
	return ''.join(msg)

while True:
	print(times)
	times += 1
	io = process(["python3", "shuffler.py"])
	res = eval(io.recvlineS().strip())
	io.sendlineafter(b'> ', b'2')
	enc_secret = io.recvlineS().strip().split(': ')[1]
	primes = list(primerange(0, 97))[::-1]
	total_mod = 1 
	states = [[], [], [], [], [], []]
	for i in range(len(primes)):
		if total_mod > 2**64:
			choosen_primes = primes[:i]
			break
		msg = string.printable[:primes[i]]
		enc_msg = encrypt_msg(msg)
		if enc_msg == None:
			continue
		total_mod *= primes[i]
		state = determine_state(msg, enc_msg)
		for j in range(6):
			states[j].append(state[j])
	io.close()
	lcg_states = []
	for i in range(6):
		lcg_states.append(crt(choosen_primes, states[i])[0])
	if not all([i.bit_length() <= 64 for i in lcg_states]):
		continue
	if lcg_states == res:
		print(lcg_states)
	try:
		params = recover_lcg_param(lcg_states)
		if params:
			a, c, m = params
			prev_state = (lcg_states[0] - c) * pow(a, -1, m) % m 
			L = LCG(a, c, m, prev_state)
			msg = decrypt_msg(L, enc_secret)
			print(msg)
			print(b64decode(msg).decode())
			break
	except Exception as err:
		print(err)

# lactf{th3_h0us3_c0uld_n3v3r_l0se_r1ght}