from pwn import * 
from Crypto.Cipher import AES 
from tqdm import trange
from Crypto.Util.Padding import unpad
r = remote("betta.utctf.live",2435)
# r = process(["python3", "main.py"])

def get_random_number():
	global seed 
	seed = int(str(seed * seed).zfill(12)[3:9])
	return seed

def gen_key():
	key = b''
	for i in range(8):
		key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
	return key

for _ in range(3):
	msg = b'0000Test_message'
	r.sendlineafter("(1 - guess the key, 2 - encrypt a message)?\n",b'2')
	r.sendlineafter("What is your message?\n", msg)
	encrypted = bytes.fromhex(r.recvlineS().strip().split(':')[1])
	for seed in trange(10**6):
		key = gen_key()
		key = gen_key()
		
		cipher = AES.new(key, AES.MODE_ECB)
		recovered_msg = cipher.decrypt(encrypted)
		try:
			if unpad(recovered_msg, 16) == msg:
				print("Found key!")
				r.sendlineafter("(1 - guess the key, 2 - encrypt a message)?\n",b'1')
				r.sendlineafter(b'What is your guess (in hex)?\n', key.hex().encode())
				break
		except:
			continue
r.interactive()