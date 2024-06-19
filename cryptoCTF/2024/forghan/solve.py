from pwn import * 
from Crypto.Util.number import *  
from sage.all import *
import sys
r = remote("00.cr.yp.toc.tf", int(13337))
p = 100439597096049244695943771437201870086992665599846060024405169302963092917287
factor_p = [2,2,2,11853755484104416302795314349063284168497734001, 3,1571,21569, 67733, 462311, 554611, 599941]
assert prod(factor_p)==p+1 and all(is_prime(f) for f in factor_p)
q = 114889937896367448448742674053488620709746656003057130332820093716194679739259
factor_q = [2,2 , 3 , 5 , 31 , 41 , 4723 , 79901, 3992225215701592790601393568553719715522250652280647701138292337]
assert prod(factor_q) == q+1 and all(is_prime(f) for f in factor_q)
factors = dict()
for x in factor_p + factor_q + [2,2,(p-1)//2,(q-1)//2]:
	if x not in factors:
		factors[x] = 1 
	else:
		factors[x] += 1 
print(factors)
phi = prod([x**(factors[x]-1)*(x-1) for x in factors])
def send_para():
	r.sendlineafter(b'uit\n', b's')
	r.sendlineafter(b'comma: \n',  (str(p) + ',' + str(q)).encode())
def get_enc_flag():
	r.sendlineafter(b'uit\n', b'g')
	cp = int(r.recvlineS().strip().split('=')[1])
	cq = int(r.recvlineS().strip().split('=')[1])
	return cp, cq 
def get_para():
	r.sendlineafter(b'uit\n', b'p')
	gp = int(r.recvlineS().strip().split('=')[1])
	gq = int(r.recvlineS().strip().split('=')[1])
	yp = int(r.recvlineS().strip().split('=')[1])
	yq = int(r.recvlineS().strip().split('=')[1])
	return gp, gq, yp, yq 
def ExtendedEuclidAlgo(a, b):
    if a == 0 : 
        return b, 0, 1 
    gcd, x1, y1 = ExtendedEuclidAlgo(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def linearCongruence(A, B, N):
    '''
    find x such that a*x = b mod n with gcd(a,n) > 1 
    '''
    A = A % N
    B = B % N
    u = 0
    v = 0
    d, u, v = ExtendedEuclidAlgo(A, N)
    if (B % d != 0):
        return []
    x0 = (u * (B // d)) % N
    if (x0 < 0):
        x0 += N
    roots = []
    for i in range(d):
        roots.append((x0 + i * (N // d)) % N)
    assert all((A*x - B) % N == 0 for x in roots) 
    return roots

flag1 = 0
flag2 = 0
b1 = False
b2 = False
send_para()
n = (p**2 - 1)*(q**2 - 1)

while True:
	cp, cq = get_enc_flag()
	gp, gq, yp, yq = get_para()
	if GCD(yp, phi) == 1:
		flag1 = pow(int(cp), pow(int(yp), -1, int(phi)), int(n))
		try:
			print(long_to_bytes(int(flag1)).decode())
		except:
			pass
	if GCD(yq, phi) == 1:
		d = pow(int(yq), -1, int(phi))
		flag2 = pow(int(cq), d, int(n))
		for gcd in range(2, 100):
			if n % gcd:
				continue
			roots = linearCongruence(pow(gcd, yq*d, n), flag2, n)
			for x in roots:
				pt = long_to_bytes(int(x * gcd % n))
				try:
					print(pt.decode())
				except:
					continue
# ...::::: CCTF{f!nD1N9_7wIn_5m0OtH_1nT3GErS!!!} :::::...
