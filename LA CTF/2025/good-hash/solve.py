from Utils import * 
from pwn import * 
from Crypto.Util.number import *
# io = process(["python3", "server.py"])
io = remote('chall.lac.tf', 32222)
# io.recvline()
print(io.recvlineS())
def get_mac(leftextend, rightextend):
	io.sendline(b'1')
	io.sendlineafter(b'input > ', leftextend.hex().encode())
	io.sendlineafter(b'input > ', rightextend.hex().encode())
	return bytes_to_long(bytes.fromhex(io.recvlineS().strip()))
m1 = b'\0'*16
m2 = b'\0'*15 + b'\x01'
tag1 = int2field(get_mac(m1, b''))
tag2 = int2field(get_mac(m2, b''))
tag3 = int2field(get_mac(b'', m1))
ct1_ct2 = int2field(bytes_to_long(xor(m1, m2)))

H = ((tag1 + tag2) / ct1_ct2).nth_root(3)
ct = field2int((tag1 + tag3) / (H**3 + H**2))
io.sendline(b'2')
io.sendlineafter(b'guess > ', long_to_bytes(ct).hex().encode())
io.interactive()
