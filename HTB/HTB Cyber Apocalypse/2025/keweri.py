#!/usr/bin/env python3
from pwn import*
from sage.all import *
from Crypto.Util.number import *

def recvlineafter(io, lines):
    io.recvuntil(lines)
    rs = io.recvline()
    return rs

local = len(sys.argv) == 1
context.log_level = "debug"
file = "server.py"
io = process(["python", file]) if local else remote(sys.argv[1], int(sys.argv[2]))

xor = lambda a, b: bytes([x^y for x, y in zip(a, b)])
from sympy import factorint

def factorize(list):
    # factors = factorint(p)  # Phân tích thừa số nguyên tố
    return "_".join(f"{k},{v}" for k, v in list)
from sympy import isprime, primerange

def is_generator(g, p):
    for d in divisors:
        if pow(g, d, p) == 1:
            return 0
    return 1
def is_primitive(zeta, factors, n):
    for p, _ in factors:
        if pow(zeta, (n-1)//p, n) == 1:
            return 0
    return 1

def main():
    p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
    # ds = divisors(p-1)
    factorization = factor(p-1)
    lst = factorize(list(factorization))
    io.sendline(b"384")
    io.sendlineafter(b"> ", str(lst).encode())
    # gens = get_generators(p)
    # print(gens)
    io.recvuntil(b"otherwise 0.\n")
    for i in range(17):
        g = int(io.recvuntilS(b'?').strip()[:-1])
        print(g)

        check = is_primitive(g, factorization, p)
        # print(check)
        io.sendlineafter(b'> ', str(check).encode())
    io.recvlineS()
    a = int(io.recvlineS().strip().split(' = ')[1])
    b = int(io.recvlineS().strip().split(' = ')[1])
    E = EllipticCurve(GF(p), [a, b])
    order = E.order()
    io.sendlineafter(b'> ', str(order).encode())

    # order2 = EllipticCurve(GF(p**3), [a, b]).order()
    # io.sendlineafter(b'> ', str(factorize(list(factor(order2)))).encode())
    send = "2,2_7,2_21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061,1_2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019,1"
    io.sendlineafter(b'> ', send.encode())
    x_G = 10754634945965100597587232538382698551598951191077578676469959354625325250805353921972302088503050119092675418338771
    x_A = 6909807541579016488447585691059408639181744396311325554172339981307525139763314637506160367438561207157918037941666
    G = E.lift_x(x_G)
    A = E.lift_x(x_A)
    d = A.log(G)
    io.sendlineafter(b'> ', str(d).encode())
    io.interactive()
    return 


if __name__ == '__main__':
    main()