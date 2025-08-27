import x25519
import os
from pwn import * 
from Crypto.Cipher import AES
io = process(["python3", "chall.py"])
# io = remote("host1.dreamhack.games", 23827)
def mul(x, point):
    return encodeint(x25519.djbec.curve25519(x, x25519.djbec.decodeint(point)))

decodeint = x25519.djbec.decodeint
encodeint = x25519.djbec.encodeint
decodepoint = x25519.djbec.decodepoint
encodepoint = x25519.djbec.encodepoint

order = 2**252 + 27742317777372353535851937790883648493
o = mul(order+2, x25519.BASE_POINT)
oo = mul(2, x25519.BASE_POINT)
while True:
    random = os.urandom(32)
    point = mul(order, random)
    if decodeint(point) > 1 and decodeint(mul(8,point))==0:
        break

io.sendlineafter(b'>>> ', b'y')
io.sendlineafter(b'>>> ', point.hex().encode())
io.sendlineafter(b'>>> ', b'y')
io.sendlineafter(b'>>> ', point.hex().encode())

io.recvline()
io.recvline()
io.recvline()

A = bytes.fromhex(io.recvlineS().strip().split(': ')[1])
iv_A = A[:16]
A = A[16:]
print(AES.new(b'\0'*32, AES.MODE_CBC, iv_A).decrypt(A))
B = bytes.fromhex(io.recvlineS().strip().split(': ')[1])
iv_B = B[:16]
B = B[16:]
print(AES.new(b'\0'*32, AES.MODE_CBC, iv_B).decrypt(B))
