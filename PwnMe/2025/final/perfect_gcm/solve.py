from pwn import * 
import json
import string
io = remote("instance4.pwnme.fr", "13172")
# io = process(['python3', "challenge.py"])
io.recvlineS()
io.recvlineS()
io.recvlineS()

bad_char = {}
for i in range(96//2):
	bad_char[i] = list(range(0,16)) + list(range(32, 128))

def encrypt_flag():
	send = {"action" : "encrypt_flag"}
	io.sendline(json.dumps(send).encode())
	recv = eval(io.recvlineS().strip())
	return recv
i = 0
while not all(len(bad_char[i]) <= 1 for i in range(48)):
	i += 1
	recv = encrypt_flag()	
	if recv['enc'] != "try again":
		enc = bytes.fromhex(recv['enc'])
		for i in range(len(enc)):
			# print(enc[i])
			if enc[i] in bad_char[i]:
				bad_char[i].remove(enc[i])
	print(bad_char)
print(i)
for i in range(48):
	print(chr(bad_char[i][0]), end="")