from sage.all import * 
from Crypto.Cipher import AES 
from base64 import * 
import hashlib
enc = {'ciphertext': b'SllGMo5gxalFG9g8j4KO0cIbXeub0CM2VAWzXo3nbIxMqy1Hl4f+dGwhM9sm793NikYA0EjxvFyRMcU2tKj54Q==', 'iv': b'MWkMvRmhFy2vAO9Be9Depw=='}

E = EllipticCurve(GF(335135809459196851603485825030548860907), [13,245])

start_point = E(14592775108451646097, 237729200841118959448447480561827799984)
ans = start_point * 1337 
sha1 = hashlib.sha1()
sha1.update(str(int(ans[0])).encode('ascii'))
key = sha1.digest()[:16]
ct = b64decode(enc["ciphertext"])
iv = b64decode(enc["iv"])
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(ct))