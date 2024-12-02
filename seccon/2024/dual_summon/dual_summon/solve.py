from Crypto.Cipher import AES 
from pwn import * 
from Crypto.Util.number import *
from Utils import *
# io = process(["python3", "server.py"])
io = remote("dual-summon.seccon.games", 2222)
def summon(pt, number):
	io.sendlineafter(b'[1] summon, [2] dual summon >', b'1')
	io.sendlineafter(b'summon number (1 or 2) >', str(number).encode())
	io.sendlineafter(b'name of sacrifice (hex) >', pt.hex().encode())
	# gg = int2field(bytes_to_long(bytes.fromhex(io.recvlineS().strip())))
	# print(field2int(gg**2))
	io.recvuntil(b'tag(hex) = ')
	return bytes.fromhex(io.recvlineS().strip())

m1 = 16*b'1'
m2 = 16*b'2'
tag1 = summon(m1, 1)
tag2 = summon(m2, 1)
tag3 = summon(xor(m1, m2), 1)
ad = int2field(0)
len_ = int2field(16)

comb = int2field(bytes_to_long(xor(tag1, tag2)))
ct1_ct2 = int2field(bytes_to_long(xor(m1, m2)))
H1 = comb * (1/ct1_ct2)
H1 = H1.nth_root(2)
enc_nonce1 = (H1**3*ad + H1**2 * ct1_ct2 + H1*len_) + int2field(bytes_to_long(tag3))


tag1 = summon(m1, 2)
tag2 = summon(m2, 2)
tag3 = summon(xor(m1, m2), 2)

comb = int2field(bytes_to_long(xor(tag1, tag2)))
H2 = comb * (1/ct1_ct2)
H2 = H2.nth_root(2)
enc_nonce2 = (H2**3*ad + H2**2 * ct1_ct2 + H2*len_) + int2field(bytes_to_long(tag3))

print(enc_nonce1)
ct = (ad*(H1**3 - H2**3) + len_*(H1 - H2) + enc_nonce1 - enc_nonce2)/ (H2**2 - H1**2)
print(field2int(H1**3*ad + H1**2 * ct + H1*len_ + enc_nonce1))
print(field2int(H2**3*ad + H2**2 * ct + H2*len_ + enc_nonce2))

ct = long_to_bytes(field2int(ct))
print(ct)
print(bytes_to_long(summon(ct, 1)))
print(bytes_to_long(summon(ct, 2)))

io.sendlineafter(b'[1] summon, [2] dual summon >', b'2')
io.sendlineafter(b'name of sacrifice (hex) >', ct.hex().encode())
io.interactive()
