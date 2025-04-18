import random
import hashlib
import os
class Curve:
    def __init__(self, p, a, b, n, G):
        self.p = p
        self.a = a
        self.b = b
        self.n = n
        self.G = G

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        if self.is_inf():
            return other
        if other.is_inf():
            return self
        if self == other:
            return self.double()
        dx = (other.x - self.x) % P192.p
        dy = (other.y - self.y) % P192.p
        s = (dy * pow(dx,-1,P192.p)) % P192.p
        x = ((s * s) - self.x - other.x) % P192.p
        y = (s * (self.x - x) - self.y) % P192.p
        return Point(x, y)

    def double(self):
        if self.is_inf():
            return self
        s = (((self.x * self.x) * 3 + P192.a) * pow(self.y * 2,-1,P192.p)) % P192.p
        x = ((s * s) - self.x - self.x) % P192.p
        y = (s * (self.x - x) - self.y) % P192.p
        return Point(x, y)

    def negate(self):
        return Point(self.x, -self.y)

    def mul(self, n):
        r = Point(0, 0)
        m = self
        while n > 0:
            if n % 2 == 1:
                r = r.add(m)
            m = m.double()
            n >>= 1
        return r

    def is_inf(self):
        return self.x == 0 and self.y == 0

def hash(data):
    hasher = hashlib.sha512()
    hasher.update(data)
    return hasher.digest()

def encrypt(data, key):
    result = []
    for i, b in enumerate(data):
        result.append(b ^ key[i % len(key)])
    return result

def bytes_to_hex(bytes):
    result = ""
    for b in bytes:
        result += format(b, "02x")
    return result

def int_to_bytes(i):
    return i.to_bytes(24, "little")

P192 = Curve(
    int("fffffffffffffffffffffffffffffffeffffffffffffffff", 16),
    int("fffffffffffffffffffffffffffffffefffffffffffffffc", 16),
    int("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1", 16),
    int("ffffffffffffffffffffffff99def836146bc9b1b4d22831", 16),
    Point(
        int("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012", 16),
        int("07192b95ffc8da78631011ed6b24cdd573f977a11e794811", 16)
    )
)

class FileRandom:
    def __init__(self):
        self.file = open("/dev/urandom", "rb")

    def gen(self):
        buf = self.file.read(4)
        return int.from_bytes(buf, "little")

def main():
    flag = os.getenv("FLAG", b"potluck{fake_FLAG}")
    message = b"Hello, Bob. What are you bringing to the potluck???"
    urandom = FileRandom()
    
    rng = random.Random(urandom)
    d_a = rng.randint(0, P192.n - 1)
    Q_a = P192.G.mul(d_a)
    print(f"Alice public key: {Q_a.x}, {Q_a.y}")
    x = input("Input Bob public key: ")
    y = input()
    if len(x) > 77 or len(y) > 77:
        print("Invalid input")
        return
    Q_b = Point(int(x) % P192.p, int(y) % P192.p)
    Q_ab = Q_b.mul(d_a)
    key_ab = int_to_bytes(Q_ab.x)
    print(f"Alice to Bob: {bytes_to_hex(encrypt(message, key_ab))}")
    d_c = rng.randint(0, P192.n - 1)
    Q_c = P192.G.mul(d_c)
    print(f"Charlie public key: {Q_c.x}, {Q_c.y}")
    Q_ac = Q_c.mul(d_a)
    key_ac = hash(int_to_bytes(Q_ac.x))
    print(f"Alice to Charlie: {bytes_to_hex(encrypt(flag, key_ac))}")

if __name__ == "__main__":
    main()
