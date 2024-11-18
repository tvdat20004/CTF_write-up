from pwn import * 
io = remote("pad.ctf.intigriti.io", 1348)

def reverse(pt):
	out = []
	for b in pt: 
		b ^= 0xCA
		b = ((b << 1) | (b >> 7)) & 0xFF
		out.append(b)
	return bytes(out)

io.recvuntil(b"Encrypted (cat state=ERROR! 'cat not in box'):")
ct = bytes.fromhex(io.recvuntilS(b'\n'))
send = ct
io.sendlineafter(b"Anyway, why don't you try it for yourself?\n", send)
print(ct.hex())
recv = io.recvlineS().strip().split(': ')[1]
print(reverse(bytes.fromhex(recv)))
