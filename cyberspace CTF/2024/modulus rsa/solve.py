from Crypto.Util.number import *
from sage.all import *
from tqdm import trange
w = 115017953136750842312826274882950615840
x = 16700949197226085826583888467555942943
y = 20681722155136911131278141581010571320
c = 2246028367836066762231325616808997113924108877001369440213213182152044731534905739635043920048066680458409222434813
from sympy import randprime
for i in trange(100):
	for j in range(100):
		for k in range(100):	
			coeff = matrix(ZZ, [
				[-i, 1, 0],
				[-j, 0, 1],
				[0, -k, 1]
			])
			res = vector(ZZ, [w, x,y])
			try:
				ans = (~coeff) * res
				p,q,r= ans
				if isPrime(int(p)) and isPrime(int(q)) and isPrime(int(r)):
					print(p,q,r)
				phi = int((p-1)*(q-1)*(r-1))
				pt = long_to_bytes(pow(int(c), pow(65537, -1, phi), int(p*q*r)))
				if b'CSCTF' in pt:
					print(pt)
					quit()
			except:
				continue

