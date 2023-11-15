from randcrack import RandCrack
from Crypto.Util.number import isPrime, long_to_bytes

from pwn import * 

predictor = RandCrack()
r = process(["python3", "chal.py"])
seed = []
while True:
	line = r.recvlineS()
	if "Sadly" not in line:
		break
	can = int(line.split(' ')[1])
	seed.append(can)
c = int(line.split(' ')[1])


cnt = 0
breaker = 0
for i in seed:
	while i != 0:
		cnt += 1
		if cnt == 625:
			breaker = 1
			break
		predictor.submit(i & 0xffffffff)
		i >>= 32
	if breaker:
		break

predictor.predict_getrandbits(512)
assert predictor.predict_getrandbits(1024) == seed[624//32 + 1]

while True:
	p = predictor.predict_getrandbits(1024)
	if isPrime(p):
		break

while True:
	q = predictor.predict_getrandbits(1024)
	if isPrime(p):
		break
n = p*q 
d = pow(65537,-1,(p-1)*(q-1))

plain = long_to_bytes(pow(c,pow(65537,-1, (p-1)*(q-1)), p*q))
print(plain)
r.close()