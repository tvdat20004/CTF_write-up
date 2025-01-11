from sage.all import *
from Crypto.Util.number import getPrime, isPrime
# from Helper.attacks.acd.ol import attack
from tqdm import trange
from time import time
L = 80
p0 = getPrime(512)
p1 = getPrime(512)
mod = getPrime(512)
print(f"{p0 = }")
print(f"{p1 = }")

while p0 > mod or p1 > mod:
    mod = getPrime(512)
a = [getrandbits(160) for _ in range(L)]
b = a
c = [ai + 1 for ai in a]
e = c
out = [(p1*(2*a[i]+1) - p0 + 2*a[i]**2 + 2*a[i] + 1) % mod for i in range(L)]

A = [(out[i] - out[0]) % mod for i in range(1, L)]
E = 2**321
def hnp_sum(A, E, T, mod):
    """
    Solves the HNP-SUM problem.
    The HNP-SUM problem is defined as finding y such that Ai = Ti * x + ei mod m.
    :param A: the Ai values
    :param E: abs(ei) <= E
    :param T: abs(ti) <= T
    :param mod: the modulus
    :return: a list of Ti (maybe -Ti) values
    """
    M = matrix(ZZ, len(A)+1, len(A)+1)
    for i in range(0, len(A)):
        M[i, -1] = T*A[i]
        M[i, i] = E
    M[-1, -1] = T*mod
    M = M.LLL()
    K = M.submatrix(row=0, col=0, nrows=len(A) - 1, ncols=len(A)).right_kernel()
    q = K.an_element()
    return q
ai_a0 = hnp_sum(A, E, 2**160, mod)
sus1 = (A[0] * pow(2*int(ai_a0[0]), -1, mod)) % mod 
sus2 = (-sus1) % mod 
print(sus1)
print(sus2)
print(f'{p1 + a[0] + a[1] + 1 = }')
print(f'{a[0] + a[1] + 1 = }')
x = Zmod(p0*p1*mod)['x'].gen()
fx1 = sus1 - x
fx2 = sus2 - x
root1 = fx1.monic().small_roots(X=2**161, beta=0.33, epsilon=0.008)
root2 = fx2.monic().small_roots(X=2**161, beta=0.33, epsilon=0.008)
assert len(root1) + len(root2) == 1
if len(root1):
    p1 = sus1 - int(root1[0])
elif len(root2):
    p1 = sus2 - int(root2[0])
print(p1)
