from pwn import *
from tqdm import tqdm
import json
CHALLENGES = [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]

with open("public_key.json",'r') as f:
    key = json.loads(f.read())

ssq = key["s^e"]
e = key['e']
N = key['N']
r = remote("0.cloud.chals.io", 19523)

for i in tqdm(CHALLENGES):
	if i == 1:
		r.sendline(b"1")
	else:
		r.sendline(str(pow(ssq,-1,N)).encode())
	r.recvline()
	r.sendline(b"1")

r.interactive()
# UDCTF{W3lc0m3_t0_0_kn0wledge_pr0of5}