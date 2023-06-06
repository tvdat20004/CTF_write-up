import os
import sys
from math import ceil
from math import log2
from math import sqrt
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

# from shared.lattice import shortest_vectors
import logging
def shortest_vectors(B):
    """
    Computes the shortest non-zero vectors in a lattice.
    :param B: the basis of the lattice
    :return: a generator generating the shortest non-zero vectors
    """
    logging.debug(f"Computing shortest vectors in {B.nrows()} x {B.ncols()} matrix...")
    B = B.LLL()

    for row in B.rows():
        if not row.is_zero():
            yield row

def attack(a, s):
    """
    Tries to find e_i values such that sum(e_i * a_i) = s.
    This attack only works if the density of the a_i values is < 0.9048.
    More information: Coster M. J. et al., "Improved low-density subset sum algorithms"
    :param a: the a_i values
    :param s: the s value
    :return: the e_i values, or None if the e_i values were not found
    """
    n = len(a)
    d = n / log2(max(a))
    N = ceil(1 / 2 * sqrt(n))
    assert d < 0.9408, f"Density should be less than 0.9408 but was {d}."

    L = matrix(QQ, n + 1, n + 1)
    for i in range(n):
        L[i, i] = 1
        L[i, n] = N * a[i]

    L[n] = [1 / 2] * n + [N * s]

    for v in shortest_vectors(L):
        s_ = 0
        e = []
        for i in range(n):
            ei = 1 - (v[i] + 1 / 2)
            if ei != 0 and ei != 1:
                break

            ei = int(ei)
            s_ += ei * a[i]
            e.append(ei)

        if s_ == s:
            return e
B = [243873082678558120886143238109, 140121004360885317204645106697, 65971149179852778782856023084, 198367501585318217337192915461, 90780110766692265488675597096, 204457189038632581915443073067, 11843936715392553537334014601, 249714131767678082951811660354, 46864685536820768096162079781, 270615453249669076126135660113, 62422813932318315478542903448, 54340894478463039745320012710, 82166063070770734716784239617, 123360554027599432641005228613, 225930829813243714315757104718, 140931881774215407739681383827, 153511648985484571193029079380, 128333502017904902954574343976, 157971994970491620681977801348, 151995940102680832680366775791, 111930343189002833676566713355, 254629522353980890137482003596, 46122603870700121747541022366, 106621126674742413122499956117, 213619593425584289387962971025, 250029395347234943835276840576, 90157964719511330175905946756, 160955342950540531541477834386, 62686435507426271661129199824, 48684199759430660574537497320, 262348080860779266021957164776, 123406793114541556721282454859, 8323348282744522342656453505, 8204832183897468999773786370, 117068364683450498818799008726, 22742733514396961388718208907, 152588763365550382579175625426, 18880903696373297518512895359, 168999842801038138048571134864, 251946102324340921852977277387, 62739530425883979430660351271, 26189963743964979633698113800, 149052997409450695582768647188, 161035032125544665156226726161, 170005203789455944372862796495, 127446446141939678833034246067, 66890847724290458515749208331, 230355717600508139033028789245]
msg = 4096661050207034370558640511465
iv = bytes.fromhex("c3599b694d81ca069cefdbd7c8f06812")
ct = bytes.fromhex("8e291e6ea5eb6f186949c8d25c5e6dc30c1869a7abf1078d26792dc846f2ffb9b5793fe92036fe55c9f8a6c61f4f516e")
_bin = attack(B,msg)
sup_sec_num = int("".join(str(i) for i in _bin),2)
print(sup_sec_num.bit_length())

key = pad(long_to_bytes(sup_sec_num), 16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
pt = cipher.decrypt(ct)
print(pt)