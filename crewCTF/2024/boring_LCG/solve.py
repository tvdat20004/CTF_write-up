from sage.all import *
import sys 
sys.path.append("/mnt/e/tvdat20004/CTF/tools")
from solve_ineq import *
set_random_seed(1337)
Fp = GF(6143872265871328074704442651454311068421530353607832481181)
a, b = Fp.random_element(), Fp.random_element()

q = ZZ(6143872265871328074704442651454311068421530353607832481181).nth_root(3)
P = ZZ[ ','.join([f's{i}' for i in range(36)] + [f'k{i}' for i in range(33)]) ]
s = P.gens()[:36]
k = P.gens()[36:]

f = Fp.modulus()
x = Fp.gen()

M0 = identity_matrix(GF(q), 3, 3)
M1 = Matrix(GF(q), 3, 3)
M2 = Matrix(GF(q), 3, 3)
M1[1,0] = M1[2,1] = 1
M1.set_column(2, (x**3).list())
M2[2,0] = 1
M2.set_column(1, (x**3).list())
M2.set_column(2, (x**4).list())

va = a.list()
vb = b.list()
A = va[0]*M0 + va[1]*M1 + va[2]*M2
B = vector(GF(q), vb)
A = A.change_ring(ZZ)
B = B.change_ring(ZZ)

out = [50, 32, 83, 12, 49, 34, 81, 101, 46, 108, 106, 57, 105, 115, 102, 51, 67, 34, 124, 15, 125, 117, 51, 124, 38, 10, 30, 76, 125, 27, 89, 14, 50, 93, 88, 56]

fns = []
lbs = []
rbs = []
for i, x in enumerate(out):
    fns.append(s[i])
    lbs.append( x    << 57)
    rbs.append((x+1) << 57)
    
    if i >= 3:
        fns.append(sum(A[i%3, j] * s[(i//3)*3 - 3 + j] for j in range(3)) + B[i%3] - s[i] - k[i-3] * q)
        lbs.append(0)
        rbs.append(0)

ans = solve(fns, lbs, rbs, verbose=True)
print(ans)
s = Fp([ans['s0'], ans['s1'], ans['s2']])

flag = ((s - b) / a).list()
flag = int(flag[0]) + int(flag[1])*q + int(flag[2])*q**2

from Crypto.Util.number import *
print(long_to_bytes(flag))