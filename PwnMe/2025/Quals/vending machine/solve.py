from pwn import * 
import json 
import sys
from Crypto.Cipher import AES
from hashlib import sha3_256
sys.path.append("/mnt/e/tvdat20004/CTF/tools/attacks/hnp")
from lattice_attack import * 
n = 0xf1fd178c0b3ad58f10126de8ce42435b53dc67e140d2bf941ffdd459c6d655e1

def get_signatures():
	send = json.dumps({
		"action" : "get_signatures",
		"alea_1" : -1,
		"alea_2" : -2
	})
	io.sendlineafter(b'Enter your command in JSON format: ', send.encode())
	recv = eval(io.recvlineS().strip())
	return recv["signatures"]
def buy_credit(proofs):
	send = json.dumps({
		"action" : "buy_credit",
		"owner_proofs" : proofs
	})
	io.sendlineafter(b'Enter your command in JSON format: ', send.encode())
	recv = eval(io.recvlineS().strip())
	return recv["credit_currency"]
def get_sigs():
	sigs = []
	print(buy_credit([]))
	sigs.extend(get_signatures())
	sigs.extend(get_signatures())
	proofs = []
	for i, (r,s) in enumerate(sigs):
		m = sha3_256(b"this is my lovely loved distributed item " + str(10 + i).encode()).digest()
		proofs.append((m.hex(), r, (-s) % n))
	print(buy_credit(proofs[:5])) 
	sigs.extend(get_signatures())
	print(buy_credit(proofs[:10])) 
	sigs.extend(get_signatures())
	print(buy_credit(proofs[:15])) 
	sigs.extend(get_signatures())
	print(buy_credit(proofs[:20])) 
	sigs.extend(get_signatures())
	return sigs
while True:
	io = process(["ncat", "--ssl", "vendingmachine-1aedf8a8bf3d2698.deploy.phreaks.fr", "443"])
	# io = process(["python3", "server.py"])
	# ks = eval(io.recvlineS().strip())
	# d = int(io.recvlineS().strip())

	choice = json.dumps({
		"action" : "get_encrypted_flag"
	})

	io.sendlineafter(b'Enter your command in JSON format: ', choice.encode())
	data = eval(io.recvlineS().strip())
	enc_flag = bytes.fromhex(data["encrypted_flag"])
	iv = bytes.fromhex(data["iv"])
	# sigs = []
	# print(buy_credit([]))
	# sigs.extend(get_signatures())
	# sigs.extend(get_signatures())
	signature = get_sigs()
	
	m0 = sha3_256(b"this is my lovely loved distributed item 10").digest()
	e0 = int.from_bytes(sha3_256(m0).digest(), "big")
	r0, s0 = signature[0]
	def div(a,b):
		return (a * pow(b, -1, n)) % n
	ai = []
	bi = []

	for i in range(1,60):
		r,s = signature[i]
		m = sha3_256(b"this is my lovely loved distributed item " + str(i+10).encode()).digest()
		e = int.from_bytes(sha3_256(m).digest(), "big")
		ai.append([(div(r0, s0) - div(r, s)) % n])
		bi.append((div(e0, s0) - div(e, s)) % n)
		# assert ks[0] > ks[i]
		# assert ks[0] - ks[i] < 2**249
		# assert (ks[0] - ks[i]) % n ==  ((div(r0, s0) - div(r, s)) * d + (div(e0, s0) - div(e, s))) % n
	isBreak = 0
	for x, y in attack(ai, bi, n, 2**249):
		# print(y[0] == d)
		key = sha3_256(int(y[0]).to_bytes(32, "big")).digest()[:16]
		cipher = AES.new(key, IV=iv, mode=AES.MODE_CBC)
		
		ct = cipher.decrypt(enc_flag)
		if b'PWNME' in ct:
			print(ct)
			quit()
	io.close()