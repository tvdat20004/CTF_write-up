from Crypto.Util.number import *

def nextPrime(p, n):
    p += (n - p) % n
    p += 1
    iters = 0
    while not isPrime(p):
        iters += 1
        p += n
    print(iters)
    return p

def factorial(n):
    if n == 0:
        return 1
    return factorial(n-1) * n

# flag = bytes_to_long(b'amateurs{dasudhaudhuahduashduha}')
flag = bytes_to_long(open('flag.txt', 'rb').read().strip())
p = getPrime(512)
q = nextPrime(p, factorial(90))
p = getPrime(512)
N = p * q
e = 65537
c = pow(flag, e, N)
print(N, e, c)