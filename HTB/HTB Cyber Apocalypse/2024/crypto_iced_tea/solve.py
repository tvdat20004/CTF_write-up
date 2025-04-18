key = bytes.fromhex('850c1413787c389e0b34437a6828a1b2')
ciphertext = bytes.fromhex('b36c62d96d9daaa90634242e1e6c76556d020de35f7a3b248ed71351cc3f3da97d4d8fd0ebc5c06a655eb57f2b250dcb2b39c8b2000297f635ce4a44110ec66596c50624d6ab582b2fd92228a21ad9eece4729e589aba644393f57736a0b870308ff00d778214f238056b8cf5721a843')
from Crypto.Util.number import * 
K = [bytes_to_long(key[i:i+4]) for i in range(0, len(key), 4)]
blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]

delta = 0x9e3779b9
mask = 1<<32
def decrypt_block(block):
	m0 = bytes_to_long(block[:4])
	m1 = bytes_to_long(block[4:])
	s = 32 * delta
	for i in range(32):
		m1 -= ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3]) 
		m1 %= mask 
		m0 -= ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
		m0 %= mask 
		s -= delta

	return long_to_bytes(m0) + long_to_bytes(m1)
print(b''.join(decrypt_block(b) for b in blocks))