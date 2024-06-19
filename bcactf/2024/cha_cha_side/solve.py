from pwn import * 

r = remote("challs.bcactf.com", 31594)
r.recvline()
enc_secret = bytes.fromhex(r.recvlineS().strip())
r.sendlineafter(b'Enter your message:\n', b'0'*32)
r.recvuntil(b'Encrypted:\n')
enc_msg = bytes.fromhex(r.recvlineS().strip())

secret = xor(b'0'*32,xor(enc_secret, enc_msg))
r.sendlineafter(b'Enter decrypted secret message:\n', secret)
r.interactive()

