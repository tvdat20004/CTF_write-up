from Cryptodome.Util.number import getPrime, inverse, bytes_to_long, GCD
import random
import math

FLAG = b'Flag{??????????????????????????????}'

def generateKeyPairs():
    q = getPrime(1024)
    upperBound = int(math.sqrt(q // 2))
    lowerBound = int(math.sqrt(q // 4))
    f = random.randint(2, upperBound)
    while True:
        g = random.randint(lowerBound, upperBound)
        if GCD(f, g) == 1:
            break
    h = (inverse(f, q)*g) % q
    return (q, h), (f, g)

def encrypt(q, h, m):
    assert m < int(math.sqrt(q // 2))
    r = random.randint(2, int(math.sqrt(q // 2)))
    e = (r*h + m) % q
    return e

def decrypt(q, h, f, g, e):
    a = (f * e) % q
    m = (a*inverse(f, g)) % g
    return m



while True:
    try:
        pub, pri = generateKeyPairs()
        q, h = pub
        f, g = pri
        m = bytes_to_long(FLAG)
        e = encrypt(q, h, m)
        print(f'Public key pair: {(q, h)}')
        print(f'My secret: {e}')
        break
    except:
        continue