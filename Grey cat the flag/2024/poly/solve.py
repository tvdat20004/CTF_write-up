from pwn import * 
from sage.all import *
r = remote("challs.nusgreyhats.org", 31113)
def find_poly(roots):
    R = PolynomialRing(QQ, 'x')
    x = R.gen()
    f = 1
    for root in roots:
        f *= (x - root)
    return f.list()[::-1]

while True:
    r.recvuntil(b'Roots: ')
    roots = r.recvuntilS(b'\n').strip().split(',')
    roots = [int(i) for i in roots]
    
    send = ""
    for coeff in find_poly(roots):
        send += str(coeff) + ","
    r.sendlineafter(b'Present the coefficients of your amazing equation: ', send[:-1].encode())

