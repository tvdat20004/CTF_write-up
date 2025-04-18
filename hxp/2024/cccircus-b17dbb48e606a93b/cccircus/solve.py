from sage.all import *
from Crypto.Util.number import *
import os
from pwn import *
from tqdm import *
P = GF(2)['x']
x = P.gen()
f = 0x1f3267f571be716d65f11ecb21b86d2e9
mod = P([(f >> i) & 1 for i in range(129)])
F = GF(2 ** 128, name="y", modulus=mod)
y = F.gen()
def red(x):
    while (l := x.bit_length()) > 128:
        x ^= f << (l - 129)
    return x

def mul(x, y):
    z = 0
    for i in range(x.bit_length()):
        if (x >> i) & 1:
            z ^= y << i
    return red(z)
def exp(x, n):
    assert n >= 0
    if not n:
        return 1
    if n % 2:
        return mul(x, exp(x, n-1))
    return exp(mul(x, x), n//2)

def int2field(n: int):
    f = P([(n >> i) & 1 for i in range(n.bit_length())])
    return F(f)
def field2int(f):
    return f.to_integer()
# x = os.urandom(32)
# key = bytes_to_long(x + b'\x01\x00')
# add = bytes_to_long(b'\x01\x00')
# print((int2field(bytes_to_long(x))*y**16 + int2field(add)))
# print(int2field(key))
# io = process(["python3", "vuln.py"])
io = remote("188.245.36.243", 7700)
key_mod = []
reses = []
# ff = int2field(int(io.recvlineS(), 16))
# print(ff)
for i in range(50):
    io.sendline(b'query ' + hex(i)[2:].zfill(2).encode())
    add = int2field(bytes_to_long(b'\x01' + bytes([i])))
    res = int2field(int(io.recvlineS().strip(), 16))
    reses.append(res)
    t = (res.nth_root(1000000) - add) / y**16
    assert (t * y**16 + add)**1000000 == res
    if t not in key_mod:
        key_mod.append(t)
# x = int2field(bytes_to_long(os.urandom(32)))
candidate = []
for poly in key_mod:
    for i in range(50):
        add = int2field(bytes_to_long(b'\x01' + bytes([i])))
        if (poly * y**16 + add)**1000000 != reses[i]:
            break
    else:
        candidate.append(poly)
key = hex(field2int(candidate[0]))[2:].zfill(32)

io.sendline(b'solve ' + key.encode())
print(io.recvlineS())
