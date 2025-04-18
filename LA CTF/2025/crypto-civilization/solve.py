from pwn import *
import hashlib
import os
import binascii
from tqdm import *
def PRG(s: bytes) -> bytes:
    assert len(s) == 2, "You're trying to cheat! Go to Crypto Prison!"
    s_int = int.from_bytes(s, byteorder="big")

    h = hashlib.new("sha3_256")
    h.update(s)

    out = h.digest()

    return out[:4]


def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise ValueError("Byte objects must be of the same length")

    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))
def brute(com):
    if com in candidates_set:
        return candidates_list.index(com).to_bytes(2, 'big')
    else:
        return b'\0\0' 
candidates_set = set()
candidates_list = []

for i in range(256**2):
    candidates_set.add(PRG(i.to_bytes(2, 'big')))
    candidates_list.append(PRG(i.to_bytes(2, 'big')))
# io = process(["python3", "chall.py"])
io = remote("chall.lac.tf", 31173)
for i in range(200):
    io.recvuntil(b"Here's y: ")
    y = bytes.fromhex(io.recvuntilS(b'\n').strip())
    for i in range(256**2):
        decom = i.to_bytes(2, 'big')
        com = candidates_list[i]
        if xor_bytes(com, y) in candidates_set:
            break
    io.sendlineafter(b'> ', com.hex().encode())
    if b'chicken' in io.recvline():
        choice = 0 
    else:
        choice = 1 
    if choice:
        result = brute(xor_bytes(com, y))
        io.sendlineafter(b'> ', result.hex().encode())
    else:
        io.sendlineafter(b'> ', decom.hex().encode())
io.interactive()
