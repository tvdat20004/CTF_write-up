from pwn import * 
from sage.all import *
from hashlib import md5
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
K = GF(p)
def hash(m):
    return bytes_to_long(md5(m).digest())

r = remote("13.201.224.182",30773)
# r = process(["python3", "server.py"])
# recover curve parameters
pubkey = eval(r.recvlineS().strip().split(':')[1])
enc = eval(r.recvlineS().strip().split(':')[1])
coeff = matrix(K, [[pubkey[0], 1], [enc[0], 1]])
hstd = vector(K, [pubkey[1]**2 - pubkey[0]**3, enc[1]**2 - enc[0]**3])
res = coeff.inverse() * hstd 
a,b = res 
print(res)
# get data from server
E = EllipticCurve(K, (a, b))
n = E.order()
m1 = b'1234'
m2 = b'abcd'
r.sendlineafter(b'Message: ', m1.hex().encode())
r.sendlineafter(b'Nonce: ',b'0000')
sig1 = json.loads(r.recvlineS().strip())
r1 = int(sig1['r'][2:], 16)
s1 = int(sig1['s'][2:], 16)

r.sendlineafter(b'Message: ', m2.hex().encode())
r.sendlineafter(b'Nonce: ',b'000000')

sig2 = json.loads(r.recvlineS().strip())
r2 = int(sig2['r'][2:], 16)
s2 = int(sig2['s'][2:], 16)
# ECDSA nonce reuse attack
k = (hash(m2) - hash(m1))*pow((s2 - s1),-1,n) % n 
d = (k*s1 - hash(m1))* pow(r1,-1,n) % n 
# Once we have the secret, find the flag
flag = E(enc) * int(pow(d,-1,n))
print(flag)
print(bytes.fromhex(hex(flag.xy()[0])[2:]))