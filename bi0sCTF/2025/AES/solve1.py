from pwn import * 
import json
import logging
from Crypto.Util.strxor import strxor
cnt = 0

# io = remote("13.233.255.238", 4001)
io = process(["python3", "chall.py"])
def send_token(iv1, ct):
	global cnt
	cnt += 1
	token = {
		"IV1" : iv1.hex(),
		"IV2" : '0'*32, 
		"ciphertext" : ct.hex()
	}
	io.sendlineafter(b'Enter token: ', json.dumps(token).encode())
	io.recvuntil(b'result: ')
	return 'Valid padding' in json.loads(io.recvuntilS(b'\n').strip())['result']

io.recvuntil(b'Here is the encrypted message : ')
token = json.loads(io.recvuntilS(b'\n').strip())
iv1 = bytes.fromhex(token['IV1'])
iv2 = bytes.fromhex(token['IV2'])
ct = bytes.fromhex(token['ciphertext'])


def _attack_block(padding_oracle, iv, c):
	logging.info(f"Attacking block {c.hex()}...")
	r = bytes()
	for i in reversed(range(16)):
		s = bytes([16 - i] * (16 - i))
		for b in range(256):
			iv_ = bytes(i) + strxor(s, bytes([b]) + r)
			if padding_oracle(iv_, c):
				r = bytes([b]) + r
				break
		else:
			raise ValueError(f"Unable to find decryption for {s}, {iv}, and {c}")

	return strxor(iv, r)


def attack(padding_oracle, iv1, iv2, c):
	"""
	Recovers the plaintext using the padding oracle attack.
	:param padding_oracle: the padding oracle, returns True if the padding is correct, False otherwise
	:param iv: the initialization vector
	:param c: the ciphertext
	:return: the (padded) plaintext
	"""
	p = _attack_block(padding_oracle, iv1, xor(iv2, c[0:16]))
	state1, state2 = iv1, iv2
	for i in range(16, len(c), 16):
		block = xor(c[i - 16:i], state2)
		dec = xor(p[i-16:i], state1)
		state1 = block
		state2 = dec
		p += _attack_block(padding_oracle, block, xor(dec,c[i:i + 16]))

	return p
print(attack(send_token, iv1, iv2, ct))
print(cnt)