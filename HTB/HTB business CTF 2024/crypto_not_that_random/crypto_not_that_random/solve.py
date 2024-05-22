from pwn import *  
from hashlib import sha256
# r = process(["python3", "server.py"])
r = remote("94.237.57.119", 46117)
def win():
	r.sendlineafter(b"Option: ", b'3')
	input = bytes.fromhex(r.recvlineS().strip().split(' ')[3])
	output = bytes.fromhex(r.recvlineS().strip().split(' ')[3])[:32]
	true_output = sha256(trap_key + input).digest()
	if true_output == output:
		r.sendlineafter(b':: ', b'0')
	else:
		r.sendlineafter(b':: ', b'1')
	if b'Wrong' in r.recvline():
		r.interactive()
# r.recvlineS()
# secret = r.recvlineS()
r.sendlineafter(b"Option: ", b'2')

value = b"Improving on the security of SHA is easy"
r.sendlineafter(b'Enter your input in hex :: ', value.hex().encode())
trap_key = bytes.fromhex(r.recvlineS().strip().split('::')[1])[32:]

for i in range((500 - 100 + 10)//5 + 1):
	win()

r.interactive()
# HTB{#rule_of_thumb___do_not_roll_your_own_hash_based_message_authentication_codes___#_aea569ed8c11479dccc82efc9614287b}