from pwn import * 
from Crypto.Util.number import *
import json
from sage.all import kronecker, crt
# io = process(["python3", 'challenge.py'])
io = remote("18.203.110.195", 30504)
def add_key(p,q):
	io.sendlineafter(b'|  > ', b'a')
	data = json.dumps({
		'p' : p,
		'q' : q
	}).encode()	
	io.sendlineafter(b'|  > (JSON) ', data)
def egcd(a, b):
    if a == 0 : 
        return b, 0, 1 
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
def get_encrypted_flag():
	io.sendlineafter(b'|  > ', b'e')
	enc = int(io.recvlineS().strip().split('0x')[1], 16)
	return enc 
def rabin_decrypt(c):
	mp = pow(c, (p+1)//4, p)
	mq = pow(c, (q+1)//4, q)
	_, yp, yq = egcd(p, q)
	# assert yp*p + yq*q==1
	r1 = (yp*p*mq + yq*q*mp) % n
	r2 = n - r1 
	r3 = (yp*p*mq - yq*q*mp) % n
	r4 = n - r3
	# r2 = crt([mp, mq], [p,q])
	# print(r1==r2)
	# # assert r1**2 % n == c
	# print(all(pow(r, 2, n) == c for r in [r1,r2]))
	# print(all(pow(r, 2, n) == c for r in [r3,r4]))

	return [r1, r2, r3, r4]
def decrypt(c):
	d = pow(65537, -1, (p-1)*(q-1))
	return pow(c, d, n)

while True:
	p,q = [getPrime(1024) for i in range(2)]
	if p % 4 == q % 4 == 3:
		break
print(p,q)
n = p*q
add_key(p,q)
enc1 = decrypt(get_encrypted_flag() % n)

add_key(p,q)
enc2 = decrypt(get_encrypted_flag() % n)
y8 = enc2 * pow(enc1, -1, n) % n
candidate = []
for i in rabin_decrypt(y8):
	if kronecker(i, n)==1:
		for j in rabin_decrypt(i):
			if kronecker(j, n)==1:
				candidate += rabin_decrypt(j)
# for i in candidate:
assert all(pow(y, 8, n) == y8 for y in candidate)
print(len(candidate))
for t in range(50):
	for y in candidate:
		flag = enc1 * pow(y, -t, n) % n 
		if b'BHFlagY' in long_to_bytes(flag):
			print(long_to_bytes(flag)) 
