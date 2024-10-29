from pwn import * 
from sage.all import * 
from Crypto.Util.number import *
while True:
    io = remote("35.187.238.100", 5002)
    p = int(io.recvlineS().strip().split()[2])
    if (p-1)%32 != 0:
        io.close()
        continue
    g = int(GF(p).multiplicative_generator())
    g = pow(g, (p-1)//32, p)
    xs = [pow(g, i, p) for i in range(32)]
    payload = ' '.join(str(i) for i in xs)
    io.sendlineafter(b'Gib me the queries: ', payload.encode())
    shares = eval(io.recvlineS().strip().split('=')[1])

    flag = long_to_bytes(sum(shares) * pow(32, -1, p) % p)
    if b'ISITDTU' in flag:
        print(flag)
        quit()
# ISITDTU{M1x_4941n!_73360d0e5fb4}  