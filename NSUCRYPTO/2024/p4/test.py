from tqdm import trange
import math
import slide
import des
import tables
pt = open("Book.txt", "rb").read()
ct = open("Book_cipher.txt", "rb").read()

pt_block = [pt[8 * i: 8 * (i + 1)] for i in range(len(pt) // 8)]
ct_block = [ct[8 * i: 8 * (i + 1)] for i in range(len(ct) // 8)]

pt_block = [slide.permutate_bytes(pt[8 * i: 8 * (i + 1)], tables.INITIAL_PERMUTATION) for i in range(len(pt) // 8)]
ct_block = [slide.permutate_bytes(ct[8 * i: 8 * (i + 1)], tables.INITIAL_PERMUTATION) for i in range(len(ct) // 8)]
ct_block = [ct[4:] + ct[:4] for ct in ct_block]

pair = [(p, c) for p, c in zip(pt_block, ct_block)]

def check_condition(x, x_):
    assert len(x) == len(x_)
    n = len(x)
    return x[:n // 2] == x_[n // 2:]

for i in trange(len(pair)):
    pt, ct = pair[i]
    for j in range(len(pair)):
        pt_, ct_ = pair[j]

        if check_condition(pt, pt_) and check_condition(ct, ct_):
            print(i, j)
# rk = [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0]
# [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0]