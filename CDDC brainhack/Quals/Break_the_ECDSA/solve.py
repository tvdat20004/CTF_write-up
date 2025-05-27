from sage.all import * 
import hashlib
from itertools import permutations
from tqdm import *
import hmac
import unicodedata
from itertools import product
from Crypto.Util.number import * 
wordlist = []
with open("Dex_dictionary.txt", "r") as file:
	for w in file.readlines():
		wordlist.append(w.strip())
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000007)
E = EllipticCurve(K, (a, b))
G = E(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
E.set_order(0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 * 0x1)
n =E.order()
r = 81210355722750344493541519494641458710145722871994877785183554697310523407018
h1 = 45643200378651069483892104393394606812504455659831083323743202489147422538955
h2 = 74831345439009646272332597737070016777412939113737083148228963710487431876647
s1 = 110764343964105699917226529930289538481215574456544978805357332521308340464732
s2 = 90138993253633063487274662700800979929978777245182171200537527514756442604713

k = (h1 - h2) * pow(s1 - s2, -1, n) % n 
d = (s1 * k - h1) * pow(r, -1, n) % n 
assert int((G * k)[0]) == r
print(hex(d))
MNEMONIC_TEMPLATE = "BIP-39 SECP256k1 {word1} 5eed r4nd0m {word2} g00d 5olve c0ffe {word3} pe4nut 5mart"

def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:

    mnemonic_normalized = unicodedata.normalize("NFKD", mnemonic)
    passphrase_normalized = unicodedata.normalize("NFKD", passphrase)
    salt = "mnemonic" + passphrase_normalized
    seed = hashlib.pbkdf2_hmac(
        "sha512",
        mnemonic_normalized.encode("utf-8"),
        salt.encode("utf-8"),
        2048,
        dklen=64
    )
    return seed

def seed_to_master_key(seed: bytes) -> bytes:

    return hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()

t = list(product(wordlist, repeat=3))
d = 0x9f9068a0cc25f39b9c5fba5bb88d75bc5e4503a8406101a3195dc395194ea690
for word1, word2, word3 in tqdm(t):
    mnemonic = MNEMONIC_TEMPLATE.format(word1=word1, word2=word2, word3=word3)
    seed = mnemonic_to_seed(mnemonic, "")
    master_key = seed_to_master_key(seed)
    master_private_key = master_key[:32]
    if master_private_key.hex() == hex(d)[2:]:
        print(word1, word2, word3)
        break

