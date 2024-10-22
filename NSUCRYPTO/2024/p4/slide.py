#!/usr/bin/env python3

import random
import itertools
from typing import List, Tuple, Callable

import des
import tables


PAIRS_COUNT = 126767
PAIRS_TRIES = 8

Pair = Tuple[des.Bytes, des.Bytes]
Oracle = Callable[[List[des.Bytes]], List[des.Bytes]]

INV_ROUND_PERMUTATION = [
    tables.ROUND_PERMUTATION.index(i + 1) + 1
    for i in range(len(tables.ROUND_PERMUTATION))
]

PC1_tmp = {y: x for x, y in enumerate(tables.PC1)}
INV_PC1 = [
    PC1_tmp.get(i + 1, -1) + 1
    for i in range(64)
]

PC2_tmp = {y: x for x, y in enumerate(tables.PC2)}
INV_PC2 = [
    PC2_tmp.get(i + 1, -1) + 1
    for i in range(56)
]

def permutate_bytes(block: des.Bytes, table: des.Table) -> des.Bytes:
    block_bits = des.block_to_bits(block)
    block_bits = des.permutate(block_bits, table)
    block = des.bits_to_block(block_bits, 8)

    return block


def extract_round_key_candidates(plaintext: des.Bytes, ciphertext: des.Bytes) -> List[des.Bits]:
    plaintext = des.block_to_bits(plaintext)
    ciphertext = des.block_to_bits(ciphertext)

    plaintext = des.permutate(plaintext, tables.INITIAL_PERMUTATION)

    left1, right1 = plaintext[:32], plaintext[32:]
    left2, right2 = ciphertext[:32], ciphertext[32:]
    assert right1 == left2

    new_right = des.xor(right2, left1)
    new_right = des.permutate(new_right, INV_ROUND_PERMUTATION)

    old_right = des.expand(right1, tables.EXPANSION)

    round_keys = []

    for i in range(8):
        # print(round_keys)
        round_key = sum([x[0] for x in round_keys], [])
        round_keys_part = []

        for value in range(2 ** 6):
            key_part = des.int_to_bits(value, 6)
            round_key_test = round_key + key_part + [0] * (48)

            old_right_test = des.xor(old_right, round_key_test)
            old_right_test = des.substitute(old_right_test, tables.SBOX)

            if old_right_test[:(i + 1) * 4] == new_right[:(i + 1) * 4]:
                round_keys_part.append(key_part)

        round_keys.append(round_keys_part)

    return round_keys
def bruteforce_master_key(round_key: des.Bits) -> des.Bits:
    round_key = des.permutate(round_key + [-1], INV_PC2)[:56]

    left, right = round_key[:28], round_key[28:]

    # in the challenge rotation == 0, so skip it:
    rotation = tables.KEY_ROTATION[0]
    left = left[-rotation:] + left[:-rotation]
    right = right[-rotation:] + right[:-rotation]

    round_key = left + right
    master_key = des.permutate(round_key + [-2], INV_PC1)[:64]

    indices1 = [i for i in range(len(master_key)) if master_key[i] == -1]
    indices2 = [i for i in range(len(master_key)) if master_key[i] == -2]
    candidates = []
    for key_part in range(2 ** 8):
        bits = des.int_to_bits(key_part, 8)

        candidate = master_key[:]

        for i, index in enumerate(indices1):
            candidate[index] = bits[i]
        candidates.append(candidate)
    return candidates
        
