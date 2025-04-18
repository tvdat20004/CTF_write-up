from pwn import * 
from itertools import permutations
from sage.all import * 
from Crypto.Util.number import *
from tqdm import *
from collections import Counter
import random
io = process(["python3", "chall.py"])
# io = remote("35.187.238.100", 5001)

def find(n, ctr):
	return [element for element, count in ctr.items() if count == n]


def combine(arr):
    perms = [list(permutations(x)) for x in arr]
    
    result = [[]]
    for options in perms:
        result = [x + list(y) for x in result for y in options]
    
    return result
p = int(io.recvlineS().strip().split()[2])
print(p)
xs = [random.randint(0,p) for i in range(33)]

payload = []
for i in range(1,16):
    payload += [xs[i]] * i 
for i in range(16,31):
    payload += [xs[i]]*(i-15)
payload += [xs[31]]
payload += 2*[xs[32]]
payload = ' '.join(str(i) for i in payload)

io.sendlineafter(b'Gib me the queries: ', payload.encode())

shares = eval(io.recvlineS().strip().split('=')[1])
ctr = Counter(shares)
res = []
for i in range(1, 16):
    res.append(find(i, ctr))

candidate = combine(res)
F = GF(p)
mtx = []
x = [xs[1], xs[16],xs[31],xs[2],xs[17],xs[32]]
for i in range(3, 16):
    x += [xs[i], xs[i + 15]]
assert len(x) == 32
for i in x:
	row = []
	for j in range(32):
		row.append(pow(i,j,p))
	mtx.append(row)
# print(mtx)
mtx = Matrix(GF(p), mtx)
inv = ~mtx
for arr in tqdm(candidate):	
	# print(res)
	x = inv * vector(F, arr)
	x = [long_to_bytes(int(i)) for i in x]
	for i in x:
		if b'ISITDTU' in i:
			print(i)
			quit()