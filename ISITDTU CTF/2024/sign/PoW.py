#!/usr/bin/env python3
import hashlib
import sys

prefix = sys.argv[1]
#difficulty = int(sys.argv[2])
zeros = '000000'
def is_valid(digest):
    if sys.version_info.major == 2:
        digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    
    return bits[:6] == '000000'


i = 0
while True:
    i += 1
    s = prefix + str(i)
    target = hashlib.sha256(s.encode()).digest().hex()[:6]
    if (target == '000000'):
        print(s)
        print(i)
        print(hashlib.sha256(s.encode()).digest())
        exit(0)