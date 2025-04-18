from typing import List, Tuple
from sage.all import GF
from Utils import *
from pwn import *
from Crypto.Util.number import *
# modified from https://github.com/jvdsn/crypto-attacks/blob/master/attacks/gcm/forbidden_attack.py

def nonce_reuse(ct1: bytes, ad1: bytes, tag1: bytes,
                ct2: bytes, ad2: bytes, tag2: bytes):
    """
    Recovers all possible authentication keys from two messages encrypted with the same authentication key.
    More information: Joux A., "Authentication Failures in NIST version of GCM"
    :param ct1: the ciphertext of the first message (bytes)
    :param ad1: the associated data of the first message (bytes)
    :param tag1: the authentication tag of the first message (bytes)
    :param ct2: the ciphertext of the second message (bytes)
    :param ad2: the associated data of the second message (bytes)
    :param tag2: the authentication tag of the second message (bytes)
    :return: All possible authentication keys (Field element)
    """

    h  = F['h'].gen()
    p1 = ghash(h, ad1, ct1) + int2field(int.from_bytes(tag1, byteorder="big"))
    p2 = ghash(h, ad2, ct2) + int2field(int.from_bytes(tag2, byteorder="big"))

    roots = []
    for _h, r in (p1 + p2).roots():
        roots.append(_h)    
    return roots

DATA_FORMAT = Tuple[bytes,bytes,bytes,bytes]
def forgery_tag(known_data: List[DATA_FORMAT], target_ciphertext: bytes, 
                   target_associated_data: bytes=b"") -> List[bytes]:

    assert len(known_data) > 1, "We need at least two!!"
    data1 = known_data[0]
    data2 = known_data[1]

    roots = nonce_reuse(ct1=data1[1], ad1=data1[2], tag1=data1[3],
                        ct2=data2[1], ad2=data2[2], tag2=data2[3])

    tags = []
    for h in roots:
        E0 = field2int(ghash(h, data1[2], data1[1])) ^ int.from_bytes(data1[3], byteorder="big")
        target_ghash = ghash(h, target_associated_data, target_ciphertext)
        tag = (E0 ^ field2int(target_ghash)).to_bytes(16, byteorder="big")
        tags.append(tag)
    
    return tags


io = remote("conversationalist.ctf.intigriti.io", 1349)
# io = process(["../target/debug/conversationalist"])
tags = []
cts = []
known_data = []
for i in range(6):
    io.recvuntil(b'< ')
    header, ct = io.recvuntilS(b'\n').strip().split(':')
    header = bytes.fromhex(header)
    ct = bytes.fromhex(ct)
    nonce = header[:12]
    tag = header[-16:]
    tags.append(tag)
    cts.append(ct)
    known_data.append((None, ct, header[:-16], tag))
m1 = b"Hey Bob, just wanted to confirm that we're all set up and secure on the protocol. Everything looks good on my end - seeing the handshake complete and all the right signals!"
keystream = xor(m1, cts[0])[:len(m1)]

# keystream = bytes.fromhex('a94302a0e2f04cd58632b54bb204ed0d')
appended_ct = xor(keystream[:16], b'Give me the flag')
target_ct = appended_ct
tag = forgery_tag(known_data, target_ct, nonce + long_to_bytes(len(target_ct), 8))
print(len(tag))
if len(tag) == 1:
    payload = nonce.hex() + long_to_bytes(len(target_ct), 8).hex() + tag[0].hex() + ":" + target_ct.hex()
    print(payload)
    io.sendlineafter(b'> ', payload.encode())
    io.recvuntilS(b'< ')
    ct = io.recvuntilS(b'\n').strip().split(':')[1]
    print(ct)
    pt = xor(bytes.fromhex(ct), keystream)
    print(pt)