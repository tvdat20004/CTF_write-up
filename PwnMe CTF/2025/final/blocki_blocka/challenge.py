#!/bin/env python3

import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randbytes
# from admin import FLAG
FLAG = b'hehehehehehehe'
PASSPHRASE = randbytes(16)

BLOCK_SIZE = 16
KEY = randbytes(BLOCK_SIZE)

def encrypt(plaintext):
    iv = randbytes(BLOCK_SIZE)
    padded = pad(plaintext + PASSPHRASE, BLOCK_SIZE)

    padded_iv = iv * int(len(padded) / BLOCK_SIZE)
    cipher = AES.new(KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(bytes(a ^ b for (a, b) in zip(padded, padded_iv)))
    return ciphertext.hex()


for i in range(32):
    message = bytes.fromhex(input("Enter your message: "))
    print(encrypt(message))

guess = bytes.fromhex(input("Did you get the passphrase?\n"))

if guess == PASSPHRASE:
    print(f"Well played! The flag is {FLAG}")
