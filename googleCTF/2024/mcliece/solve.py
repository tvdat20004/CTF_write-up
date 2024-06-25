from sage.all import *
from Crypto.Util.number import *
import math
from tqdm import trange
p, n, k, r = 521, 256, 169, 39
pubkey = load("pubkey.sobj")
encrypted_flag = load("flag_enc.sobj")
l = 30
F = GF(p)
cnt = 0
def decode_flag(x):
	x = [int(i) for i in x]
	ret = 0
	for i in x[::-1]:
		ret *= p
		ret += i
	return long_to_bytes(ret)

while True:
	print(l)
	padding = k-l
	for i in trange(int(math.comb(295, l)/math.comb(295-31, l))):
		# poses = list(range(n))[-l:]
		poses = sample(list(range(n)), l)
		cols = [pubkey.column(i) for i in poses]
		# cols = matrix(F, cols)
		# m = vector(F,[316, 141, 502, 198, 55, 27, 309, 233, 81, 262, 473, 93, 62, 146, 228, 492, 301, 338, 198, 443, 108, 108, 66, 507, 329, 24, 45, 303, 351, 391, 368, 153, 395, 329, 127, 29, 470, 154, 157, 266, 514, 360, 173, 350, 515, 119, 288, 406, 252, 296, 255, 444, 357, 290, 244, 377, 289, 164, 321, 347, 378, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108])
		# c = vector(F, [encrypted_flag[0][i] for i in poses])
		# assert cols * m == c
		c = [encrypted_flag[0][i] for i in poses]
		c = [(c[i] - padding * sum(cols[i][l:])) % p for i in range(l)]
		c = vector(F, c)
		cols = matrix(F, [x[:l] for x in cols])
		try:
			x = cols.inverse() * c
		except:
			continue
		flag = decode_flag(list(x))
		if b'CTF{' in flag:
			print(flag)
			quit()
	l += 1

