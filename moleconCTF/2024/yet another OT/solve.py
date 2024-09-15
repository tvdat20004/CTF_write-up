from pwn import *
import random 
from Crypto.Util.number import *
from hashlib import sha256
from tqdm import *
import math
def jacobi(a, n):
	if n <= 0:
		raise ValueError("'n' must be a positive integer.")
	if n % 2 == 0:
		raise ValueError("'n' must be odd.")
	a %= n
	result = 1
	while a != 0:
		while a % 2 == 0:
			a //= 2
			n_mod_8 = n % 8
			if n_mod_8 in (3, 5):
				result = -result
		a, n = n, a
		if a % 4 == 3 and n % 4 == 3:
			result = -result
		a %= n
	if n == 1:
		return result
	else:
		return 0

def check(c0,c1,p):
	check0, check1 = jacobi(c0,p), jacobi(c1, p)
	# print(check0, check1)
	if check0 == 1 and check1 == -1:
		m0,m1 = 0, 1
	elif check0 == -1 and check1==1:
		m0, m1 = 1, 0
	elif check0 == -1 and check1==-1:
		m0, m1 = 1,1
	else:
		return None
	return m0, m1

ps = [getPrime(32) for _ in range(33)]
tmp = ps[:]
n = math.prod(ps)
x = int.from_bytes(sha256(("x"+str(n)).encode()).digest(), "big")
ps = [p for p in ps if jacobi(x,p) == 1 ]
print(len(ps))
import json
# io = process(["python3", "server.py"])
io = remote("yaot.challs.m0lecon.it", 2844)

io.sendlineafter(b'Send me a number: ', str(n).encode())
tts = json.loads(io.recvlineS().strip())['vals']

for i in range(128):
	data = json.loads(io.recvlineS().strip())
	c0, c1 = data['c0'], data['c1']
	m0, m1 = 0, 0
	for p in ps:
		assert jacobi(x,p)==1
		res = check(c0, c1, p)
		if res:
			m0, m1 = res 
			break
	print(m0, m1)
	io.sendline(json.dumps({"m0" : m0, "m1" : m1}).encode())
from Crypto.Cipher import AES 
enc = bytes.fromhex(io.recvlineS().strip())
phi = math.prod([p-1 for p in tmp])
ts = [pow(t, pow(n, -1, phi), n) for t in tts]
key = sha256((",".join(map(str, ts))).encode()).digest()

print(AES.new(key, AES.MODE_ECB).decrypt(enc))