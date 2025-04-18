from mt19937predictor import MT19937Predictor
from 
from pwn import * 
from Crypto.Util.number import long_to_bytes, isPrime
while True:

	r = process(["python3", "chal.py"])
	predict = MT19937Predictor()
	seed = []
	while True:
		line = r.recvlineS()
		if "Sadly" not in line:
			break
		can = int(line.split(' ')[1])
		seed.append(can)
	for i in seed[-644:]:
		predict.setrandbits(i,1024)

	p = predict.getrandbits(1024)
	assert isPrime(p)
	while True:
		q = predict.getrandbits(1024)
		if isPrime(q):
			break

	c = int(line.split(' ')[1])
	
	plain = long_to_bytes(pow(c,pow(65537,-1, (p-1)*(q-1)), p*q))
	if b'EPFL' in plain:
		print(plain)
		break
	r.close()

