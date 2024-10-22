from pwn import *
import json 
import paillier
import ecc
import dlnproof
from secrets import randbelow
from Crypto.Util.number import *
from mta import *
from math import lcm
from common import *
0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
io= process(['python3', 'server.py'])
# io = remote("183.91.11.30", 1337)
# def gen():
#     p = 2
#     factor = []
#     for i in range(32):
#         _p = getPrime(32)
#         factor.append(_p)
#         p *= _p
#     if isPrime(p + 1):
#         return p+1, factor   
#     else:
#         return gen()      
# p = gen()
# q = gen()
# print(p)
# print(q)
P = 94137154100507726830735364901574111383776390066901632454460525270544254702579637844760274414232039923022220956183437381257832573977102268744025387099959467714534577882757785335645070262481128876668808485339231132190292434562446464793728800357247972522468698860856595065750928558759075758078502123360252387
Q = 3194487899505935819030545923228784232960613239159040409512061777359323218820218015027803394753554616352127060647125900694847353967656888053619950642563654122203001488986162629218344670024336871631739734382530685422710292156968275473349735916654698604089374352639690860509501109896167576241440654818210947
NTildeA = P * Q
factorP = [3719780287, 3611255603, 2428090087, 2812173737, 2544198511, 3566965621, 3552973453, 2960878373, 3794291441, 3916911121, 2456739811, 2915553409, 3788959351, 4134543169, 3789317083, 2999151751, 4220909467, 4284131387, 2290083743, 3486433459, 3848437331, 3537836227, 3514449977, 2305642333, 2769646427, 3954685123, 3433180763, 3811126357, 3773056489, 3435125797, 2695185371, 3556647817]
factorQ = [2599164107, 3309061913, 2319043481, 3967790303, 3536465539, 3183896869, 2514116659, 2564751127, 2530435753, 4271775553, 3977440387, 2238337471, 3253744367, 3869342357, 2770127411, 3079116871, 2842712437, 2287406339, 2503649579, 3942391043, 2821574831, 3034841981, 3681663527, 3232812523, 2250061103, 2975500211, 2550127583, 2262185567, 3670285621, 2797722919, 2771168773, 3741646471]



Lambda = lcm(P-1, Q-1)
h1 = randbelow(NTildeA)
while pow(h1, Lambda, NTildeA) != 1:
    h1 = pow(h1, 2, NTildeA)
x_i = randbelow(Lambda)
while GCD(x_i, Lambda) != 1:
    x_i = randbelow(Lambda)
x_inv = pow(x_i, -1, Lambda)

h2 = pow(h1, x_i, NTildeA)
payload = json.dumps({
    "NTildeB": NTildeA,
    "h1B": h1,
    "h2B": h2,
    "dlnproof": [
        dlnproof.getDLNProof(h1, h2, x_i, Lambda, NTildeA),
        dlnproof.getDLNProof(h2, h1, x_inv, Lambda, NTildeA),
    ]
})

io.sendlineafter(b'Bob Public Key = ', payload.encode())
_n = json.loads(io.recvlineS().strip().split("=")[1])['N']
from sympy.ntheory import discrete_log
point = "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c2964fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"

io.sendlineafter(b'gBPoint (hex) = ', point.encode())
recv = json.loads(io.recvlineS().strip().split('=')[1])
from sage.all import *

Z = recv["proofA"]['Z']
U = recv["proofA"]['U']
W = recv["proofA"]['W']
S = recv["proofA"]['S']
S1 = recv["proofA"]['S1']
S2 = recv["proofA"]['S2']
c = recv["cA"]


FF = Zmod(NTildeA)
order = (P-1)*(Q-1)
ans1 = discrete_log(FF(Z), FF(h1), ord = order)
ans2 = discrete_log(FF(W), FF(h1), ord = order)
e = SHA512_256i([_n, _n + 1, c, Z, W, U]) % q
param = Matrix(FF,[
    [x_i, 0,0,1],
    [0,1,x_i, 0],
    [0,1,0,e],
    [e,0,2,0]
])

ans = vector(FF, [ans1, ans2, S1, S2])

res = (~param) * ans
print(long_to_bytes(int(res[-1])))

