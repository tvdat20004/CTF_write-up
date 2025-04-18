from sage.all import * 
from pwn import * 
import random
# r = remote('challenge03.play.potluckctf.com',31337)
# r = process(['python3', 'main.py'])

p = int("fffffffffffffffffffffffffffffffeffffffffffffffff", 16)
a = int("fffffffffffffffffffffffffffffffefffffffffffffffc", 16)
b = int("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16)
n = int("ffffffffffffffffffffffff99def836146bc9b1b4d22831", 16)
Gx = int("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16)
Gy = int("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16)

# r.recvuntil(b'Alice public key: ')
# Q_a = E(*(list(map(int, r.recvuntilS(b'\n').strip().split(',')))))
while True:
    b = random.randint(0,p-1)
    E = EllipticCurve(GF(p), [a,b])
    od = E.order()
    fac = list(factor(od))
    if all(prime < 2**45 for prime,e in fac):
        print(b)
        break 
# 5286792990678095946872411039764355443644685268799870943415