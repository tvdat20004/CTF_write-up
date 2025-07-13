from sage.all import *
import itertools
from Crypto.Util.number import *

N = 83839453754784827797201083929300181050320503279359875805303608931874182224243
c = 32104483815246305654072935180480116143927362174667948848821645940823281560338
p = 276784813000398431755706235529589161781
q = N // p
e = 65537

x = PolynomialRing(GF(p), 'x').gen()
f = x**e + (256 * x + ord("."))**e - c
g = pow(x, p, f) - x
mp = [c for c, _ in f.gcd(g).roots()]
print(mp)
x = PolynomialRing(GF(q), 'x').gen()
f = x**e + (256 * x + ord("."))**e - c
g = pow(x, q, f) - x
mq = [c for c, _ in f.gcd(g).roots()]
print(mq)
m = [int(crt(int(mmp), int(mmq), p, q)) for mmp, mmq in itertools.product(mp, mq)]

f = bytes_to_long(b"The flag is maltactf{" + bytes([0]) * len("???????????????????????????????") + b"}")
for mm in m:
    try:
        print(long_to_bytes((mm - f) % N).decode())
    except:
        continue