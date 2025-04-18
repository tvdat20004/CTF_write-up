from sage.all import * 
from Crypto.Util.number import *
from pwn import * 

import json
io = remote('instance3.pwnme.fr', 12697)
# io = process(["python3", "server.py"])
q = 0x10001
# print(io.recvlineS())
def get_leak(idx):
	command = {"action" : "get_leak", "index" : idx}
	io.sendlineafter(b'Enter your command in JSON format: ', json.dumps(command).encode())
	recv = json.loads(io.recvlineS().strip())
	return recv['A'], int(recv['B'])

As = []
Bs = []
Bs_mod_q = []
for i in range(512):
	A, B = get_leak(i)
	As.append(A)
	Bs.append(B)
	Bs_mod_q.append(B % q)
As = matrix(GF(q), As)
Bs_mod_q = vector(GF(q), Bs_mod_q)
S = (~As) * Bs_mod_q
print(len(S))
S = S.change_ring(ZZ)
As = As.change_ring(ZZ)
guess = []
cnt = 0
for A,B in zip(As, Bs):
	cc = (B - A*S) // q 
	for i in range(1024):
		_min = (2**63) << i
		_max = (2**64) << i
		if _min < cc < _max:
			guess.append(i)
			break
g = ((Bs[511] - As[511] * S)//q ) // 2**(guess[511])
print(g)
cmd = {"action" : "get_encrypted_challenge"}
io.sendlineafter(b'Enter your command in JSON format: ', json.dumps(cmd).encode())
# print(io.recvlineS())
recv = int(json.loads(io.recvlineS().strip())['value'],16)
assert recv % g == 0
challenge = bin(recv // g)[2:].zfill(1024)
ans = [0] * 512
for i in range(1024):
	if challenge[i] == '1':
		ans[guess.index(1023 - i)] = 1
print(ans)
challenge = int(''.join(str(i) for i in ans),2)
print(long_to_bytes(challenge).hex())
cmd = {"action" : "get_flag", "challenge_guess" : long_to_bytes(challenge).hex()}
io.sendlineafter(b'Enter your command in JSON format: ', json.dumps(cmd).encode())
io.interactive()