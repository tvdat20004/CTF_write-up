
wordlist = []
with open("Dex_dictionary.txt", "r") as file:
    for w in file.readlines():
        wordlist.append(w.strip())

MNEMONIC_TEMPLATE = "BIP-39 SECP256k1 {word1} 5eed r4nd0m {word2} g00d 5olve c0ffe {word3} pe4nut 5mart"

import hashlib
from itertools import product
from tqdm import *
import hmac
import unicodedata
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
print(hex(d)[2:])
for word1, word2, word3 in tqdm(t):
    mnemonic = MNEMONIC_TEMPLATE.format(word1=word1, word2=word2, word3=word3)
    seed = mnemonic_to_seed(mnemonic, "")
    master_key = seed_to_master_key(seed)
    master_private_key = master_key[:32]
    if master_private_key.hex() == hex(d)[2:]:
        print(word1, word2, word3)
        break
