from pwn import * 
from tqdm import trange
from Crypto.Util.number import *
io = remote("instance1.pwnme.fr", 14980)

# io = process(["python3", "challenge.py"])
def build_msg():
	template = b'0' * (64 - len(PASSPHRASE) - 2) + PASSPHRASE
	print(template)
	msg = b''
	for i in trange(65536):
		msg += template + long_to_bytes(i, 2)
	return msg + b'0' * (64 - len(PASSPHRASE) - 2)
PASSPHRASE = b'' 
for i in range(0,64, 2):
	msg = build_msg()
	io.sendlineafter(b'Enter your message: ', msg.hex().encode())
	# print(io.recvlineS())

	encrypted = bytes.fromhex(io.recvlineS().strip())
	block_size = 64
	blocks = [encrypted[i : i+block_size] for i in range(0, len(encrypted), block_size)]
	print(blocks[bytes_to_long(b'ab')])
	print(blocks[-2])
	for b in blocks[:-2]:
		if b == blocks[-2]:
			print(121)
			PASSPHRASE += long_to_bytes(blocks[:-2].index(b), 2)
	print(PASSPHRASE)

io.sendlineafter(b'Did you get the passphrase?\n', PASSPHRASE.hex().encode())
print(io.recvlineS())