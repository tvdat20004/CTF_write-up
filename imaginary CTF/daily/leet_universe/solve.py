from sage.all import * 

x = polygen(ZZ)
f = x**13 + 37
g = (x + 42) ** 13 + 42
r = ZZ(f.resultant(g))
print(r)
R = Zmod(r)
ff = f.change_ring(R)
gg = g.change_ring(R)
while gg:
    ff,gg = gg, ff % gg 

n = ZZ((-ff[0]) / ff[1])

from pwn import *
io = process(['python3', 'server.py'])
io.sendlineafter(b'x = ', str(n).encode())
io.interactive()