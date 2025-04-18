import json
from Crypto.Cipher import Salsa20
from secrets import token_hex, token_bytes
from Crypto.Util.number import *
from pwn import *
from zlib import crc32
# r = process(['python3', 'server.py'])
r = remote("tango.chal.imaginaryctf.org", 1337)
def encrypt_command():
	r.sendlineafter(b'> ', b'E')
	r.sendlineafter(b'Your command: ', b'dat')
	data = bytes.fromhex(r.recvlineS().strip().split(':')[1])
	return data[:8],data[8:12], data[12:]

def run_cmd(nonce, ct, checksum):
	payload = nonce + long_to_bytes(checksum) + ct
	r.sendlineafter(b'> ', b'R')
	r.sendlineafter(b'Your encrypted packet (hex): ', payload.hex().encode())
	data = r.recvlineS()
	print(data)
	return 'ictf' in data
nonce,checksum,encrypted = encrypt_command()

# cipher = Salsa20.new(key=key, nonce = nonce)

target = {'user' : 'root', 'command' : 'flag', 'nonce' : token_hex(8)}
target = json.dumps(target).encode()
def plaintext(i):
	return json.dumps({'user' : 'user', "command" : 'dat', 'nonce' : i*16}).encode()
checksum = bytes_to_long(checksum)
for i in '0123456789abcdef':
	# print(plaintext(i))
	keystream = xor(plaintext(i), encrypted)
	enc_target = xor(keystream, target)[:46] + encrypted[46:]
	# print(enc_target)
	### caculate crc32
	sample = b'{"user": "user", "command": "flag", "nonce": "xxxxxxxxxxxxxxx"}'
	x = f'user", "command": "dat", "nonce": "{i}'.encode()
	y = b'root", "command": "flag", "nonce": "'
	diff = b'\0'*10 + xor(x,y) + 17*b'\0'
	c = crc32(xor(sample, plaintext(i))) ^ crc32(sample) ^ crc32(plaintext(i))
	# print(c)
	checksum_target = c ^ crc32(diff) ^ checksum
	if run_cmd(nonce, enc_target, checksum_target):
		print('win	')
		break

