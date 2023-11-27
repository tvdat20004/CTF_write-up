from pwn import * 

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

r = remote('chall.glacierctf.com', 13379)
r.recvuntil(b'The spirit of the glacier gifts you a flag!\n')
nonce = bytes.fromhex(r.recvuntilS(b',').strip()[:-1])
ct = bytes.fromhex(r.recvuntilS(b',').strip()[:-1])
tag = bytes.fromhex(r.recvuntilS(b'\n').strip())
enc = b""
numOfBlock = len(ct) // 16
for i in range(numOfBlock):
	cipher_input = nonce + (i + 1).to_bytes(1, 'little')
	r.sendlineafter(b'Offer your message:', cipher_input.hex().encode())
	r.recvuntil(b'The spirit of the glacier has blessed your message!\n\n')
	enc += bytes.fromhex(r.recvlineS().split(',')[2])

print(xor(ct, enc))
r.interactive()