# from Blupper
from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

p = 4420073644184861649599
a = 1144993629389611207194
b = 3504184699413397958941

trunc = [39, 47, 95, 1, 77, 89, 77, 70, 99, 23, 44, 38, 87, 34, 99, 42, 10, 67, 24, 3, 2, 80, 26, 87, 91, 86, 1, 71, 59, 97, 69, 31, 17, 91, 73, 78, 43, 18, 15, 46, 22, 68, 98, 60, 98, 17, 53, 13, 6, 13, 19, 50, 73, 44, 7, 44, 3, 5, 80, 26, 10, 55, 27, 47, 72, 80, 53, 2, 40, 64, 55, 6]
n = len(trunc)
ct = bytes.fromhex('34daaa9f7773d7ea4d5f96ef3dab1bbf5584ecec9f0542bbee0c92130721d925f40b175e50587196874e14332460257b')

As = [(a**i) % p for i in range(n)]
Bs = [(b*(a**i-1)//(a-1)) % p for i in range(n)]

I = identity_matrix(n)
L = block_matrix([
    [matrix(t - b for t, b in zip(trunc, Bs)),  0,  1],
    [matrix(As),                                0,  0],
    [I*p,                                       0,  0],
    [I*100,                                     I,  0]])

S = 2**72
W = diagonal_matrix([S]*n + [1]*n + [S**2])

for v in (L*W).LLL() / W:
    if abs(v[-1]) == 1:
        v *= sign(v[-1])
        ks = v[n:2*n]
        assert all(x==0 for x in v[:n])
        assert all([abs(k)<(p//100) for k in ks])
        s = (trunc[0] + ks[0]*100) % p

def lcg():
    global s
    s = (a * s + b) % p
    return s % 100

for _ in range(72-1): lcg()

key = bytes([lcg() for _ in range(16)])
iv = bytes([lcg() for _ in range(16)])
cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ct), 16).decode())