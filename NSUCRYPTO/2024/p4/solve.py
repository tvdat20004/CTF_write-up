import slide
import tables
import des
import itertools
pt = open("book.txt", "rb").read()
ct = open("Book_cipher.txt", "rb").read()
pt_block = [pt[i:i+8] for i in range(0, len(pt), 8)]
ct_block = [ct[i:i+8] for i in range(0, len(ct), 8)]

pt1 = pt_block[0] 
ct1 = ct_block[0]
pt2 = pt_block[99283]
ct2 = ct_block[99283]
pt2 = slide.permutate_bytes(pt2, tables.INITIAL_PERMUTATION)

candidates = slide.extract_round_key_candidates(pt1, pt2)
static_des = des.DES(b'AAAAAAAA')
for candidate in itertools.product(*candidates):
	candidate = sum(candidate, [])
	static_des.round_keys = [candidate] * len(static_des.round_keys)

	if static_des.encrypt(pt1) == ct1:
		round_key = candidate
		break 
print(round_key)
master_keys = slide.bruteforce_master_key(round_key)
possible_key = []
for master_key in master_keys:
	indices = [i for i in range(len(master_key)) if master_key[i] < 0]
	for i in range(2 ** 8):
		key_part = des.int_to_bits(i, 8)
		candidate = list(master_key)
		for i, index in enumerate(indices):
			candidate[index] = key_part[i]
		key = des.bits_to_block(candidate, 8)
		cipher = des.DES(key)
		if cipher.round_keys[0] == round_key:
			possible_key.append(key)
print(len(possible_key))
ct = bytes.fromhex("86991641D28259604412D6BA88A5C0A6471CA7222C52482BF2D0E841D4343DFB877DC8E0147F3D5F20FC18FF28CB5C4DA8A0F4694861AB5E98F37ADBC2D69B35779D9001BB4B648518FE6EBC00B2AB10")
ct_block = [ct[8 * i: 8 * (i + 1)] for i in range(len(ct) // 8)]
for key in possible_key:
	pt = b""
	cipher = des.DES(key)
	cipher.reversed_round_keys = [cipher.round_keys[0]] * len(cipher.round_keys)
	for ct in ct_block:
		pt += cipher.decrypt(ct)
	print(pt)