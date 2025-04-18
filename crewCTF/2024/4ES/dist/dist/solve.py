from Crypto.Cipher import AES
from hashlib import sha256

from tqdm import tqdm
pt = bytes.fromhex('4145535f4145535f4145535f41455321')
ct = bytes.fromhex('edb43249be0d7a4620b9b876315eb430')
enc_flag = bytes.fromhex('e5218894e05e14eb7cc27dc2aeed10245bfa4426489125a55e82a3d81a15d18afd152d6c51a7024f05e15e1527afa84b')

chars = b'crew_AES*4=$!?'
keys = []
k = []
for i in chars:
	for j in chars:
		for h in chars:
			keys.append(sha256(bytes([i, j, h])).digest())
			k.append(bytes([i,j,h]))

candidate1 = []
for k1 in tqdm(keys):
	sample = AES.new(k1, AES.MODE_ECB).encrypt(pt)
	for k2 in keys:
		candidate1.append(AES.new(k2, AES.MODE_ECB).encrypt(sample))

candidate2 = []
for k3 in tqdm(keys):
	sample = AES.new(k3, AES.MODE_ECB).decrypt(ct)
	for k4 in keys:
		value = AES.new(k4, AES.MODE_ECB).decrypt(sample)
		candidate2.append(value)
candidate1_ = set(candidate1)
candidate2_ = set(candidate2)
common = candidate1_.intersection(candidate2_)
print(common)
# k1 = 792
# k2 = 1169
# k3 = 1044
# k4 = 142
for c in common:
	idx1 = candidate1.index(c)
	idx2 = candidate2.index(c)
	k1,k2 = idx1 // len(keys), idx1 % len(keys)
	k3,k4 = idx2 // len(keys), idx2 % len(keys)

x = AES.new(keys[k3], AES.MODE_ECB).encrypt(
			 AES.new(keys[k4], AES.MODE_ECB).encrypt(
				 AES.new(keys[k2], AES.MODE_ECB).encrypt(
					 AES.new(keys[k1], AES.MODE_ECB).encrypt(
						 pt
					 )
				 )
			 )
	)
assert x==ct
assert sha256(k[k1]).digest()==keys[k1]
key = sha256(k[k1] + k[k2] + k[k4] + k[k3]).digest()
print(AES.new(key, AES.MODE_ECB).decrypt(enc_flag))