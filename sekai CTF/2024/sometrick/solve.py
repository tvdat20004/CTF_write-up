# from sage.all import *
from tqdm import *
import random
seed = 53444883986185431629144081032650309850416419200452362289618896824062068081976
random.seed(seed)
GSIZE = 8209
GNUM = 79
LIM = GSIZE**GNUM
bob_encr = 312545625873170892308163869515943307301231502475852614905674790627946355094679578902106318043941679870032244815665149954437897203470526027870123051436610479364624380210176422471993266821616923229819921701593994162342255677040734718750007416890268245896162537019030562304134726502204977668329146055282387991346
alice_encr = 171560164741024909730168834685065325715243872990112040443845309463799552761345992408211104339245750785930823458920423418834154069752907334172583033134193525006736648679149105788417815570741918224495147740486590116231908068637079452224147455855480712616200651917743785636943448988803579641151992543040678343241
bob_decr = 217235637198670078579388997431841297584452656994210571008488830933844024929846972742743271633868264920013855061197126921245898175201282130556685685256066865227990928170303723508349870026095861691461287149854118294907834122423272894657993076166952214845977369907285074465738596466825871531826099308778936151510

def gen(n):
    p, i = [0] * n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)

def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res
def mul(a,b):
	return tuple(a[i] for i in b)

def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res
def recover_key(plain, cipher, G):
	key = 0
	for i in range(len(G)):
		ct = cipher % GSIZE
		pt = plain % GSIZE
		x = gexp(G[i], pt).index(ct)
		print(x)
		key += x * GSIZE**i
		cipher = cipher // GSIZE
		plain = plain // GSIZE
	return key 
def decrypt(cipher, key, G):
	plain = 0
	for i in range(len(G)):
		ct = cipher % GSIZE
		k = key % GSIZE
		tmp = tuple(G[i])
		for j in range(GSIZE):
			tmp = mul(tmp, G[i])
			if tmp[k] == ct:
				if j + 1 == GSIZE:
					return plain
				print(j+1)
				plain += (j + 1)*GSIZE**i
				break
		cipher = cipher // GSIZE
		key = key // GSIZE
	return plain 
def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod

G = [gen(GSIZE) for i in range(GNUM)]
inverse_G = [inverse(i) for i in G]

bob_key = recover_key(alice_encr, bob_decr, inverse_G)
print(bob_key)
k = bob_key % GSIZE
ct = bob_encr % GSIZE
from Crypto.Util.number import *

x = decrypt(bob_encr, bob_key, G)
for i in range(x.bit_length()):
	flag_pad = x % 2**i
	# if b'SEKAI' in long_to_bytes(flag_pad):
	# 	print(long_to_bytes(flag_pad)) 
	for j in range(flag_pad.bit_length()):
		flag = flag_pad >> j
		if b'SEKAI' in long_to_bytes(flag):
			print(long_to_bytes(flag))