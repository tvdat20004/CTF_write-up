from hashlib import sha256
import sys
sys.path.append("/mnt/e/tvdat20004/CTF/tools/attacks/hnp")
sys.path.append("/mnt/e/tvdat20004/CTF/tools/shared")
from lattice_attack import *
from partial_integer import *

from sage.all import *
load('https://raw.githubusercontent.com/TheBlupper/linineq/main/linineq.py')

# load("https://gist.githubusercontent.com/Connor-McCartney/952583ecac836f843f50b785c7cb283d/raw/5718ebd8c9b4f9a549746094877a97e7796752eb/solvelinmod.py")
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
E = EllipticCurve(GF(p), [0, 7])
G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

Q = E(75734809163232403156751567099323868969251536315520212930406362087044311009812, 59376216810615307969183220664321477461374978580814681880833956961200252954411)
r = 75188570313431311860804303251549254089807291132108761029130443888999271228837
s = 28425244802253213823226413962559295239693382541446853572606143356013575587849
# Q = E(45902505212273188321903021355839696369286713701843701429234898742542889873555, 3586781962723664871389935635876041675824332945627203966608474740369979265905)
# r = 5540416251847848227911157310155110101173634114648289819948228048773553637827
# s = 18939308594891511470609346629622477998310455538951272337731787852062552770251
h = int(sha256(b"Karmany-evadhikaras te ma phalesu kadacana ma karma-phala-hetur bhur ma te sango 'stv akarmani.").hexdigest(), 16)
h_high = (h >> 128)
a = (r * 2**128 - s) % n 
b = r 
c = ((s * h_high * 2**128) - h) % n 
M = Matrix([[a, b]])
lb = [0, 0]
ub = [2**128, 2**128]


for cc in solve_bounded_mod_gen(M, [c], lb, ub, n):
	x, y = cc 
	assert (a*x + b*y - c) % n == 0
	d = (int(x) << 128) + int(y) 
	if d*G == Q:
		print(d)
		print(sha256(str(d).encode()).hexdigest())




# x,y = var('x y')
# bounds = {x: 2**128, y:2**128}
# eqs = [(a*x + b*y == c, n)]
# sol = solve_linear_mod(eqs, bounds)
# x = int(sol[x])
# y = int(sol[y])
# d = (y << 128) + x 
# assert (a*x + b*y - c) % n == 0
# assert (d % n)*G==Q
# for x,y in attack([[(-b) * pow(a, -1, n) % n]], [c * pow(a, -1, n) % n], n, 2**128):
# 	print(x, y)




# k = PartialInteger.from_msb(256, h >> 128, 128)
# for d, k in dsa_known_msb(n, [h], [r], [s], [k]):
# 	print(d,k)
# 	print(sha256(str(d).encode()).hexdigest())
# 	assert (d % n)*G == Q
# '26ee6ab791e3b003ebb3ca81547a63455fbe19d4a27cc0a73d30395f5aa2e73a'

