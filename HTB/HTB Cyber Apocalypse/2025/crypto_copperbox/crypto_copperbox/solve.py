import cuso
from sage.all import *
p = 0x31337313373133731337313373133731337313373133731337313373133732ad
a = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
b = 0xdeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0de
h1 = 77759147870011250959067600299812670660963056658309113392093130 << 48
h2 = 50608194198883881938583003429122755064581079722494357415324546 << 48
trunc = 48 
x1, x2 = var('x1,x2')
# x1,x2 = P.gens()
ms1 = 1 - a*(h1 + x1)
ms2 = 1 - a*(h2 + x2)
f = (a+1)*ms1*ms2 + a**2 * ms2 * (h1+x1) - ms1 * (h2 + x2) 
bounds = {x1 : (0, 2**48), x2 : (0, 2**48)}
roots = cuso.find_small_roots([f], bounds, modulus =p)
print(roots)
_x1 = roots[0][x1]
_x2 = roots[0][x2]

h1 = h1 + _x1
x1 = h1*b * pow(1-a*h1, -1, p) % p
x0 = (x1 - b) * pow(a, -1, p)%p
from Crypto.Util.number import *
print(long_to_bytes(x0))