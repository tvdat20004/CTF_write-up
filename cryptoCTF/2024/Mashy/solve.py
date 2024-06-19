from pwn import * 
from hashlib import md5  
r = remote("00.cr.yp.toc.tf", 13771)
h1 = bytes.fromhex("4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2")
h2 = bytes.fromhex("4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2")

for i in range(8):
	h1 += b'\0'
	h2 += b'\0'
	r.sendlineafter(b'input:  \n', h1.hex().encode())
	r.sendlineafter(b'input: \n', h2.hex().encode())

r.interactive()
# CCTF{mD5_h4Sh_cOlL!Si0N_CrYp7o_ch41lEnGe!!!}