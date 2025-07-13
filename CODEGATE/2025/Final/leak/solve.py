from pwn import * 
from LEAk import *
from z3 import * 
from itertools import product
# io = process(['python3', 'LEAk.py'])
io = remote("43.201.153.112", 10955)
def solve_pow():
	print(io.recvlineS())
	print(io.recvlineS())
	print(io.recvlineS())
	print(io.recvlineS())
	sol = input()
	io.sendlineafter(b'Solution?', sol.encode())

solve_pow()
# rk5 = int(io.recvlineS())
for _ in range(14):
	io.recvlineS()
def get_all_solutions(s, variables) -> dict:
	solutions = []
	cnt = 0
	while s.check() == sat:
		cnt += 1  
		# print(cnt)
		m = s.model()
		solution = {v: m[v] for v in variables}
		solutions.append(int(solution[variables[0]].as_long()))
		block = []
		for v in variables:
			block.append(v != m[v])
		s.add(Or(block))
	return solutions

def reduce_list(l):
	return list(set(l))

def encrypt(pt):
	io.sendline(b'0')
	io.sendline(pt.hex().encode())
	ct = bytes.fromhex(io.recvlineS().strip()[1:])
	return ct
_DELTA = [0xC3EFE9DB, 0x44626B02, 0x79E27C8A, 0x78DF30EC]

def encrypt_fault(pt, fault_round, word_idx):
	io.sendline(b'1')
	io.sendline(pt.hex().encode())
	io.sendline(f'{fault_round} {word_idx}'.encode())
	ct = bytes.fromhex(io.recvlineS().strip()[1:])
	# print(ct)
	return ct
def split_block(x):
	return [int.from_bytes(x[i*4 : 4*(i+1)], 'little') for i in range(4)]
def get_bit(n, i):
	return (n >> i) & 1
def recover_key_from_last_round(rk23_words: list[int]) -> bytes:

    T = list(rk23_words)

    for i in range(24 - 1, -1, -1):
        t0 = rol(_DELTA[i & 3], i & 31)
        t1 = rol(_DELTA[i & 3], (i + 1) & 31)
        t2 = rol(_DELTA[i & 3], (i + 2) & 31)
        t3 = rol(_DELTA[i & 3], (i + 3) & 31)
        prev_T0 = (ror(T[0], 1) - t0) & WORD
        prev_T1 = (ror(T[1], 3) - t1) & WORD
        prev_T2 = (ror(T[2], 6) - t2) & WORD
        prev_T3 = (ror(T[3], 11) - t3) & WORD
        T = [prev_T0, prev_T1, prev_T2, prev_T3]
    master_key = b"".join(int(w).to_bytes(4, "little") for w in T)
    return master_key

pt = b'0' * 16
ct_correct = encrypt(pt)
ccc = ct_correct
ct_correct = split_block(ct_correct)
x23_0 = ct_correct[3]
candidate = []
s = Solver()
k = BitVec('k', 32)
for i in range(4):
	ct_fault0 = split_block(encrypt_fault(pt, 23, 0))
	s.add((BitVecVal(ct_correct[3], 32) ^ k) - (BitVecVal(ct_fault0[3], 32) ^ k) == BitVecVal(ror(ct_correct[0], 9) - ror(ct_fault0[0],9), 32))
candidate = get_all_solutions(s, [k])
ct_fault = [split_block(encrypt_fault(pt, 23, 1)) for _ in range(3)]
rk0s = candidate.copy()
rk1_rk2s = []
x23_1_k2s = []
# x23_1_k1s = []

for rk0 in rk0s:
	s = Solver()
	x = BitVec('x', 32) # = x23_1 ^ k2
	for i in range(3):
		x23_1_k1 = (ror(ct_correct[0], 9) - (x23_0 ^ rk0)) % 2**32
		# x23_1_k1s.append(x23_1_k1)
		delta_X1 = ((ror(ct_fault[i][0], 9) - (x23_0 ^ rk0)) % 2**32) ^ x23_1_k1 
		s.add(x - (x ^ BitVecVal(delta_X1, 32)) == BitVecVal(rol(ct_correct[1], 5) - rol(ct_fault[i][1], 5), 32))
	sol = get_all_solutions(s, [x])
	if len(sol) == 0:
		candidate.remove(rk0)
	for cc in sol:
		x23_1_k2s.append(cc)
		rk1_rk2s.append(cc ^ x23_1_k1)
rk0s = candidate.copy()
x23_2_k1s = [(rol(ct_correct[1],5) - i) % 2**32 for i in x23_1_k2s]

# assert rk5 in rk0s
ct_fault = [split_block(encrypt_fault(pt, 23, 2)) for i in range(4)]
x23_2_k1s = list(set(x23_2_k1s))
tmp = x23_2_k1s.copy()
x23_2_k4s = []
for x23_2_k1 in tmp:
	s = Solver()
	x = BitVec('x', 32) # x23_k4
	for i in range(4):
		delta_X2 = x23_2_k1 ^  ((x23_2_k1 - (rol(ct_correct[1], 5) - rol(ct_fault[i][1], 5))) % 2**32)
		s.add(x - (x ^ BitVecVal(delta_X2, 32)) == BitVecVal(rol(ct_correct[2], 3) - rol(ct_fault[i][2], 3), 32)  )
	sol = get_all_solutions(s, [x])
	if len(sol) == 0:
		x23_2_k1s.remove(x23_2_k1)

	x23_2_k4s.extend(sol)


x23_2_k4s = list(set(x23_2_k4s))
k1_k4s = []
for k1 in x23_2_k1s:
	for k4 in x23_2_k4s:
		k1_k4s.append(k1 ^ k4)
k1_k4s = reduce_list(k1_k4s)

# assert rk5 in k1_k4s
# print(len(x23_2_k4s))
x23_3_k1s = reduce_list([(rol(ct_correct[2], 3) - i) % 2**32 for i in x23_2_k4s])

ct_fault = [split_block(encrypt_fault(pt, 22, 0)) for i in range(4)]

t0 = rol(_DELTA[23 & 3], 23 & 31)
rk22_0s = [(ror(i, 1) - t0) % 2**32 for i in rk0s]

x22_0_k22_0s = []
tmp = x23_3_k1s.copy()
# x22_0_k22_0 = states[22][0] ^ rk5
for x23_3_k1 in tmp:
	s = Solver()
	x = BitVec('x', 32) # x22_0_k22_0
	for i in range(4):            
		delta_X3 = x23_3_k1 ^ ((x23_3_k1 - (rol(ct_correct[2], 3) - rol(ct_fault[i][2], 3)) ) % 2**32)
		s.add(x - (x ^ BitVecVal(delta_X3,32)) == BitVecVal(ror(ct_correct[3],9) - ror(ct_fault[i][3], 9),32 ))
	sol = get_all_solutions(s, [x])
	if len(sol) == 0:
		x23_3_k1s.remove(x23_3_k1)

	x22_0_k22_0s.extend(sol)

x22_0_k22_0s = reduce_list((x22_0_k22_0s))
x22_0s = []
for x in x22_0_k22_0s:
	for rk in rk22_0s:
		x22_0s.append(x ^ rk)
x22_0s = reduce_list(x22_0s)
k1s = reduce_list([i ^ j for i,j in product(x22_0s, x23_3_k1s)])
k4s = reduce_list([i ^ j for i,j in product(k1s, k1_k4s)])
k2s = reduce_list([i ^ j for i, j in product(k1s, rk1_rk2s)])
print(len(k1s), len(k2s), len(k4s))
from tqdm import *
for k0 in tqdm(rk0s):
	for k1 in k1s:
		for k2 in k2s:
			for k3 in k4s:
				key = recover_key_from_last_round([k0, k1, k2, k3])
				if encrypt_(pt, key) == ccc:
					io.sendline(key.hex().encode())
					io.interactive()
