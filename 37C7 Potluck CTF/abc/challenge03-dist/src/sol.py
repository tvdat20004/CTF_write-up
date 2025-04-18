from sage.all import * 
from pwn import * 
import random
import hashlib
r = remote('challenge03.play.potluckctf.com',31337)
# r = process(['python3', 'main.py'])

def xor(data, key):
    result = []
    for i, b in enumerate(data):
        result.append(b ^ key[i % len(key)])
    return bytes(result)

p = int("fffffffffffffffffffffffffffffffeffffffffffffffff", 16)
a = int("fffffffffffffffffffffffffffffffefffffffffffffffc", 16)
b = int("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16)
n = int("ffffffffffffffffffffffff99def836146bc9b1b4d22831", 16)
Gx = int("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16)
Gy = int("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16)
E = EllipticCurve(GF(p), [a,b])
r.recvuntil(b'Alice public key: ')
Q_a = E(*(list(map(int, r.recvuntilS(b'\n').strip().split(',')))))
b_ = 5286792990678095946872411039764355443644685268799870943415
E_ = EllipticCurve(GF(p), [a,b_])
G_ = E_.gen(0)
n_ = G_.order()
# P = G_ * factor[-1][0]
# new_od = n_ // factor[-1][0]
x,y = G_.xy()

r.sendlineafter(b'Input Bob public key: ', (str(x) + ', '+ str(y)).encode())
# r.sendline(str(y).encode())
message = b"Hello, Bob. What are you bringing to the potluck???"
enc_mess = bytes.fromhex(r.recvlineS().strip().split(':')[1])
key_ab = xor(message, enc_mess)[:24]
Qab_x = int.from_bytes(key_ab, 'little')
Qab = E_.lift_x(GF(p)(Qab_x))
print(Qab)
dlog = discrete_log(Qab, G_, operation='+')
print(dlog)

r.recvuntil(b'Charlie public key: ')
pubkey = E(*(list(map(int, r.recvuntilS(b'\n').strip().split(',')))))
enc_flag = bytes.fromhex(r.recvlineS().strip().split(':')[1])
k = 0
while True:
    can = k*n_ + dlog
    if can > n:
        exit(1)
    Q_ac = pubkey * can
    key = hashlib.sha512(int(Q_ac.xy()[0]).to_bytes(24,'little')).digest()
    flag = xor(enc_flag, key)
    if b'potluck' in flag:
        print(flag)
        break
    else:
        k += 1
        