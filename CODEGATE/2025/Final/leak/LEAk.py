import os
from copy import deepcopy
from typing import List, Tuple

# from secret import flag, banner
flag = b'hhhhhh'
WORD = 0xFFFFFFFF
rol = lambda x, r: ((x << r) | (x >> (32 - r))) & WORD
ror = lambda x, r: ((x >> r) | (x << (32 - r))) & WORD

_ROUNDS = 24
_DELTA = [0xC3EFE9DB, 0x44626B02, 0x79E27C8A, 0x78DF30EC]

KEY = os.urandom(16)

def key_schedule_128(key: bytes) -> List[List[int]]:
    assert len(key) == 16
    T = [int.from_bytes(key[i * 4 : (i + 1) * 4], "little") for i in range(4)]
    rks: List[List[int]] = []
    for i in range(_ROUNDS):
        t0 = rol(_DELTA[i & 3], i & 31)
        # if i == 23:
            # print(t0)
        t1 = rol(_DELTA[i & 3], (i + 1) & 31)
        t2 = rol(_DELTA[i & 3], (i + 2) & 31)
        t3 = rol(_DELTA[i & 3], (i + 3) & 31)
        T[0] = rol((T[0] + t0) & WORD, 1)
        T[1] = rol((T[1] + t1) & WORD, 3)
        T[2] = rol((T[2] + t2) & WORD, 6)
        T[3] = rol((T[3] + t3) & WORD, 11)
        rks.append([T[0], T[1], T[2], T[1], T[3], T[1]])
    return rks


def _round(state: List[int], rk: List[int]) -> None:
    x0, x1, x2, x3 = state
    state[0] = rol(((x0 ^ rk[0]) + (x1 ^ rk[1])) & WORD, 9)
    state[1] = ror(((x1 ^ rk[2]) + (x2 ^ rk[3])) & WORD, 5)
    state[2] = ror(((x2 ^ rk[4]) + (x3 ^ rk[5])) & WORD, 3)
    state[3] = x0

def encrypt_(pt: bytes, key: bytes) -> bytes:
    rk = key_schedule_128(key)
    state = [int.from_bytes(pt[i * 4 : (i + 1) * 4], "little") for i in range(4)]
    for r in rk:
        _round(state, r)
    return b"".join(int(w).to_bytes(4, "little") for w in state)

def encrypt_fault_(
    pt: bytes, key: bytes, fault_round: int, word_idx: int) -> Tuple[bytes, bytes]:
    assert 0 <= fault_round < _ROUNDS
    assert 0 <= word_idx < 4
    fault = int.from_bytes(os.urandom(4), "little")
    rk = key_schedule_128(key)
    state = [int.from_bytes(pt[i * 4 : (i + 1) * 4], "little") for i in range(4)]

    for i, r in enumerate(rk):
        if i == fault_round:
            tmp = state[word_idx]
            state[word_idx] = (state[word_idx] + fault) & WORD
            cc = tmp ^ state[word_idx]
        _round(state, r)
    return b"".join(int(w).to_bytes(4, "little") for w in state)

def split_block(x):
    return [int.from_bytes(x[i*4 : 4*(i+1)], 'little') for i in range(4)]

if __name__ == "__main__":
    print(banner)
    # pt = b'0' * 16
    # ct_correct, correct_states = encrypt(pt, KEY)

    # rk = key_schedule_128(KEY)
    # ct_faulty, delta, faulty_states = encrypt_fault(pt, KEY, 22, 0)
    # ct_faulty = split_block(ct_faulty)
    # ct_correct = split_block(ct_correct)
    # tmp = correct_states[23][3] ^ rk[23][1]
    # x22_0_k22_0 = correct_states[22][0] ^ rk[22][0]
    # print((x22_0_k22_0 - (x ^ delta)) % 2**32 == ror(ct_correct[3], 9) - ct_faulty[3])

    for _ in range(16):
        match int(input()):
            case 0:
                pt = bytes.fromhex(input())[:16]
                ct = encrypt_(pt, KEY)
                print(">", ct.hex())
            case 1:
                pt = bytes.fromhex(input())[:16]
                fault_round, word_idx = list(map(int, input().split()))
                ct = encrypt_fault_(pt, KEY, fault_round, word_idx)
                print(">", ct.hex())
            case _:
                pass

    if KEY == bytes.fromhex(input())[:len(KEY)]:
        print(flag)
