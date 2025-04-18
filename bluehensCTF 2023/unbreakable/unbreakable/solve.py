from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib

key = hashlib.sha256(b"tasciewapeoiu").digest()
with open("flag.enc", "rb") as f:
	f = f.read()

iv, enc = f[:16], f[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)

flag = cipher.decrypt(enc)
print(flag)