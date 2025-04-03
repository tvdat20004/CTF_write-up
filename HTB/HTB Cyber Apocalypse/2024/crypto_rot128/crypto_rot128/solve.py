from pwn import * 
from Crypto.Util.number import * 
import random
from z3 import * 
# from utils import HashRoll
r = process(['python3', "server.py"])
N = 128
_ROL_ = lambda x, i : ((x << i) | (x >> (N-i))) & (2**N - 1)
def solution(x0, x1):
    X0 = BitVecVal(x0, N)  
    X1 = BitVecVal(x1, N)
    # Define the variables
    s0 = BitVecVal(127, N)
    s1 = BitVecVal(127, N)
    s2 = ZeroExt(121, BitVec('s2', 7))
    s3 = ZeroExt(121, BitVec('s3', 7))
    s4 = BitVec('s4', N)
    s5 = BitVec('s5', N)
    s = Solver()
    s.add(RotateLeft(s4, s0) ^ RotateLeft(s5, s1) == X0)
    s.add(RotateLeft(s4, s2) ^ RotateLeft(s5,s3) == X1)
    if s.check() == sat:
        m = s.model()
        return [127, 127, m.evaluate(s2), m.evaluate(s3), m.evaluate(s4), m.evaluate(s5)]
    return None


for i in range(3):
    r.recvuntil(b'You know H(')
    m = bytes_to_long(bytes.fromhex(r.recvuntilS(b')')[:-1]))
    h = bytes.fromhex(r.recvuntilS(b'\n').strip().split()[1])
    m1 = m >> N
    m2 = m & (2**N - 1)
    h1, h2 = bytes_to_long(h[:16]), bytes_to_long(h[16:])
    sol = list(map(int, map(str, solution(h1 ^ m1, h2 ^ m2))))
    assert _ROL_(sol[4],sol[0]) ^ _ROL_(sol[5],sol[1]) == h1 ^ m1
    assert _ROL_(sol[4],sol[2]) ^ _ROL_(sol[5],sol[3]) == h2 ^ m2
    payload = ",".join(str(s) for s in sol)
    r.sendlineafter(b'Send your hash function state (format: a,b,c,d,e,f) :: ', payload.encode())
r.interactive()
