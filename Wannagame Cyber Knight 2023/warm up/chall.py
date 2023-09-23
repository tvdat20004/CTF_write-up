from Crypto.Util.number import getPrime, isPrime 
from Crypto.Util.number import long_to_bytes as ltb, bytes_to_long as btl 
from random import randint 
from secret import FLAG


def genprimes1():
    while True:
        p = getPrime(512)
        q = p + int(str(p), 12) + 1
        if isPrime(q):
            return p, q
        
def genprimes2():
    ok =  btl(b'd4rkn19ht_w4s_h3r3')
    while True:
        p = getPrime(512)
        q = ok *p +  randint(pow(2,255), pow(2, 256) - 1)
        if isPrime(q):
            return p, q 

def gensmoothprime(bitlen, smoothness ):
    p = 2
    while (bitlen - p.bit_length()) > 2*smoothness:
        p = p * getPrime(smoothness)
    while True:
        bit = bitlen - p.bit_length()
        q = p * getPrime(bit//2) * getPrime(bit//2)
        if isPrime(q+1):
            return q + 1

def genprimes3():
    p = gensmoothprime(1024, 18)
    q = getPrime(1024)
    return p, q 

p1, q1 = genprimes1()

p2, q2 = genprimes2()

p3, q3 = genprimes3()


n1 = p1 * q1 
n2 = p2 * q2 
n3 = p3 * q3

e1 = e2 = e3 = 65537
L = len(FLAG)
part1 = btl(FLAG[ : L // 3])
part2 = btl(FLAG[L // 3 : (2*L)//3])
part3 = btl(FLAG[(2 * L) // 3 : ])

c1 = pow(part1, e1, n1)
c2 = pow(part2, e2, n2)
c3 = pow(part3, e3, n3)

print(f"{n1 = }")
print(f"{e1 = }")
print(f"{c1 = }")

print(f"{n2 = }")
print(f'{e2 = }')
print(f"{c2 = }")

print(f"{n3 = }")
print(f"{e3 = }")
print(f"{c3 = }")