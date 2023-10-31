import json
import math
from sympy.ntheory import sqrt_mod
from Crypto.Util.number import * 
from tqdm import trange
from pwn import *
with open("public_key.json", "r") as j:
	j = json.loads(j.read())

p = j["p"]
ssq = j["s^e"]
e = j['e']
def check(can):
	return pow(can, (p-1)//2, p) == 1 

def find_base(res):
	base = res 
	for i in trange(256):
		can = sqrt_mod(base,p, True)
		if check(can[0]):
			base = can[0]
		elif check(can[1]):
			base = can[1]
		else:
			quit()
	assert pow(base,e,p) == res
	return base
s = find_base(ssq) 
print(s)
rsq = json.dumps([pow(2,e,p)]*128)
r = remote("0.cloud.chals.io",14202)
r.sendline(rsq.encode())
requests = json.loads(r.recvlineS().strip())

response = []
for req in requests:
	if req == "rs":
		response.append(2*s)
	else:
		response.append(2)


r.sendline(json.dumps(response).encode())

r.interactive()
# UDCTF{Squ4re_R00t_r3duces_to_fact0riz4ti0n}