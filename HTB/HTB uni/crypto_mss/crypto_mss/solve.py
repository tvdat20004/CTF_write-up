from pwn import * 
from json import * 
from sympy.ntheory.modular import crt
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from hashlib import sha256
r = process(["python3", "server.py"])
# r = remote("94.237.54.27", 45342)
getflagPayload = dumps({"command" : "encrypt_flag"})
payload = dumps({"command" : "get_share", "x" : 0})
r.sendlineafter(b'query = ', payload.encode())
key = int(loads(r.recvlineS().strip())['y'])
print(key)
r.sendlineafter(b'query = ', getflagPayload.encode())
r.recvuntil(b"Here is your encrypted flag : ")
j = loads(r.recvlineS().strip()[:-1])
# print(j)
iv = bytes.fromhex(j['iv'])
enc = bytes.fromhex(j['enc_flag'])
key = sha256(str(key).encode()).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.decrypt(enc)
print(ct)
