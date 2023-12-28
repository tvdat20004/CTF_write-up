from pwn import * 
from json import * 
from sympy.ntheory.modular import crt
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from hashlib import sha256
r = process(["python3", "server.py"])
# r = remote("94.237.54.27", 45342)
# nc 94.237.54.27 45342
primes = [getPrime(14) for _ in range(19)]
payload = [dumps({"command" : "get_share", "x" : p}) for p in primes]
getflagPayload = dumps({"command" : "encrypt_flag"})
y = []
for i in range(19):
	r.sendlineafter(b"query = ", payload[i].encode())
	y.append(loads(r.recvlineS().strip())['y'] % primes[i])

r.sendlineafter(b'query = ', getflagPayload.encode())
r.recvuntil(b"Here is your encrypted flag : ")
j = loads(r.recvlineS().strip()[:-1])
# print(j)
iv = bytes.fromhex(j['iv'])
enc = bytes.fromhex(j['enc_flag'])
key, mod = crt(primes, y)
print(mod.bit_length())
while True:
	key_aes = sha256(str(key).encode()).digest()
	cipher = AES.new(key_aes, AES.MODE_CBC, iv)
	ct = cipher.decrypt(enc)
	if b'HTB' not in ct:
		key += mod 
	else:
		print(ct)
		break

