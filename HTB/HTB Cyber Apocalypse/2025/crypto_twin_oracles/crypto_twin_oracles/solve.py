from pwn import * 
from sympy import primerange
from server import *
from Crypto.Util.number import *
from tqdm import *
io = process(["python3", "server.py"])
# print(bin(int(io.recvlineS().strip())))
def get_param():
	io.sendlineafter(b'> ', b'1')
	n = int(io.recvlineS().strip().split(' = ')[1])
	enc_flag = int(io.recvlineS().strip().split(':')[1])
	return n, enc_flag
def send_ct(ct):
	io.sendlineafter(b'> ', b'2')
	io.sendlineafter(b"Submit your encrypted scripture for the Seers' judgement: ", hex(ct)[2:].encode())
	res = int(io.recvlineS().strip().split(':')[1])
	return res
def check_candidate(candidate):
	x = candidate

	res = []
	for i in range(50):
		res.append(int(not pow(x, 2, M) % 2))
		x = pow(x, 2, M)
	return res==states
io.recvline()
io.recvline()
M = int(io.recvlineS().strip().split(' = ')[1])
n, enc_flag = get_param()
states = []
for i in range(50):
	states.append(send_ct(1))
candidates = list(primerange(2**14, 2**15))
for c in candidates:
	if check_candidate(c):
		print(c)
		x = c 

left = 0
right = n
e = 65537
i0, i1 = 0, 1
for i in range(50):
	x = pow(x, 2, M)

for i in range(1024):
	x = pow(x, 2, M)

	if x % 2:
		res = send_ct(enc_flag * pow(2**i0, e, n) % n)
	else:
		res = send_ct(enc_flag * pow(2**i1, e, n) % n)
	if res:
		left = (left + right) // 2 
	else:
		right = (left + right) // 2

	# c = c * pow(2, e, n) % n
	i0 += 1
	i1 += 1
print(long_to_bytes((left-1)%n))

