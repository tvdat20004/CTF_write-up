from pwn import *
from tqdm import tqdm
from Crypto.Util.number import *
from collections import Counter

def get_challenge():
    io.sendlineafter(b"flag\n", b"1")
    return bytes.fromhex(io.recvline().strip().decode())

def decrypt(ct):
    io.sendlineafter(b"flag\n", b"2")
    io.sendlineafter(b"(hex) ct: ", ct.hex().encode())
    return bytes.fromhex(io.recvline().strip().decode())

def bitwise_complement(x, nbits=64):
    return x ^ (2**nbits - 1)

if __name__ == "__main__":
    io = remote("desfunctional.2024.ctfcompetition.com", 1337)

    enc  = get_challenge()
    decs = []
    for _ in tqdm(range(128)):
        x = decrypt(long_to_bytes(bitwise_complement(bytes_to_long(enc), 64*8)))
        decs.append(x)
   	
    ctr  = Counter(decs)
    cc   = ctr.most_common(1)[0][0]
    ans  = long_to_bytes(bitwise_complement(bytes_to_long(cc[:8]))) + cc[8:]

    io.sendlineafter(b"flag\n", b"3")
    io.sendlineafter(b"pt: ", ans.hex().encode())
    io.interactive()