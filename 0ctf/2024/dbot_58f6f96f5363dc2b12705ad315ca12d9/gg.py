from   Crypto.Util.number  import bytes_to_long, long_to_bytes, isPrime, getPrime
from   pwn                 import remote, process
from   sage.all            import *
from   tqdm import *
from ast import literal_eval

sys.path.append('/mnt/e/tvdat20004/CTF/tools/attacks/hnp')

from lattice_attack import *

# host = 'instance.penguin.0ops.sjtu.cn'
# port = int(18443)
DEBUG = False
# if DEBUG:
#     io = process(['python3', 'task.py'])
# else:
#     io = remote(host, port)

def Debug():
    if DEBUG:
        io.recvuntil(b'primes1 = ')
        primes1 = eval(io.recvline().strip().decode())
        io.recvuntil(b'primes2 = ')
        primes2 = eval(io.recvline().strip().decode()) 
        return primes1, primes2
    return None, None

def Level0():
    io.sendlineafter(b'Choose one prime you prefer: ', b'2')
    mod = int(io.recvlineS().strip().split(':')[1])
    c = int(io.recvlineS().strip().split('=')[1]) # c
    N = int(io.recvlineS().strip().split('=')[1]) # c
    ai = []
    # print(io.recvlineS().strip())
    # print(io.recvlineS().strip())

    for i in range(80):
        x0 = int(io.recvlineS().strip().split('=')[1]) 
        x1 = int(io.recvlineS().strip().split('=')[1]) 
        io.sendlineafter(b'Give me v: ',str(x0).encode())
        m0 = int(io.recvlineS().strip().split('=')[1]) # c
        m1 = int(io.recvlineS().strip().split('=')[1]) # c
        ph12 = ((m0 + m1) - pow(x0 - x1, pow(65537, -1, mod - 1), mod)) % mod 
        ai.append([ph12])
    b = [0]*80
    candidate = []
    for _, y in attack(ai, b, mod, 2**497):
        candidate.append(pow(y[0], -1, mod))
    print(candidate)
    x = Zmod(N//mod)['x'].gen()
    f = candidate[0] - x
    root = f.monic().small_roots(X=2**248, beta=0.499, epsilon=0.012)[0]
    print(root)
    p1 = ZZ(candidate[0] - root)
    p0 = ZZ(N//(mod*p1))
    phi = (mod -1)*(p1-1)*(p0- 1)
    m = pow(c, pow(65537, -1, int(phi)), N)
    io.sendlineafter(b'Give me m: ', str(m).encode())


def Level1():
    io.sendlineafter(b'Choose one prime you prefer: ', b'3')
    mod = int(io.recvlineS().strip().split(':')[1])
    c = int(io.recvlineS().strip().split('=')[1]) # c
    N = int(io.recvlineS().strip().split('=')[1]) # c
    assert N % mod == 0

    if DEBUG:
        io.recvuntil(b'a = ')
        a = eval(io.recvline().strip().decode()) 

    ph1 = []
    ph2 = []
    for i in range(80):
        x0 = int(io.recvlineS().strip().split('=')[1]) 
        x1 = int(io.recvlineS().strip().split('=')[1]) 
        io.sendlineafter(b'Give me v: ',str(x0).encode())
        m0 = int(io.recvlineS().strip().split('=')[1]) # c
        m1 = int(io.recvlineS().strip().split('=')[1]) # c

        ph1.append(m0)
        ph2.append((m1 - pow(x0 - x1, pow(65537, -1, mod - 1), mod)) % mod)

    ai = []
    for i in range(1, 80):
        ai.append([(ph1[0] - ph1[i] + ph2[0] - ph2[i]) * pow(2, -1, mod)])

    b = [0]*79
    candidate = []
    for x, y in attack(ai, b, mod, 2**160):
        candidate.append((x, pow(y[0], -1, mod)))
        candidate.append((x, int(pow(y[0], -1, mod)) + int(mod)))

    def get_p(candidate):
        for (da, ap) in candidate:
            if 1 < gcd(ap+1, N) < N:
                return da, ap+1
        return None, None
    
    da, p = get_p(candidate); assert p != None, "ui cha 2"
    print(f'[level 1] Got {p = }')

    aq = (ph1[0] - ph2[0] - (ph1[1] - ph2[1])) % mod
    aq *= pow(2, -1, mod)
    aq *= pow(da[0], -1, mod)
    aq %= mod

    if DEBUG:
        print(f'*{primes2[1] = }')
        print(f'*{aq         = }')

    def get_q(aq):
        x = Zmod(N//p//mod)['x'].gen()
        f = (aq>>160<<160) + x
        for dq in f.monic().small_roots(
            X=2**160, 
            beta=0.4, 
            epsilon=0.014
        ):
            q = (aq>>160<<160) + dq
            q = int(q)
            if 1 < gcd(q, N) < N:
                return q

    q = get_q(aq); assert q != None, "ui cha 3"
    print(f'[level 1] Got {q = }')

    r = mod

    s = N//p//q//r

    d = pow(0x10001, -1, (p-1)*(q-1)*(r-1)*(s-1))
    m = pow(c, d, N)

    io.sendlineafter(b'Give me m: ', str(m).encode())
    print(f'[level 1] okela')


primes1, primes2 = Debug()
while True:
    host = 'instance.penguin.0ops.sjtu.cn'
    port = int(18443)
    DEBUG = False
    if DEBUG:
        io = process(['python3', 'task.py'])
    else:
        io = remote(host, port)
    try:
        Level0()
        Level1()
        io.interactive()
    except:
        continue
