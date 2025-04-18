import random
from Crypto.Util.number import isPrime, getPrime
while 1:
	p = 65537 * random.randint(2**47, 2**48) + 1
	if isPrime(p) and 2**63 < p < 2**64:
		print(p)
		print(getPrime(64))
		break