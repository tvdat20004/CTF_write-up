
from pwn import * 
r = remote("betta.utctf.live",4374)
r.recvline()
r.recvline()
r.recvline()
exec(r.recvlineS().strip())
exec(r.recvlineS().strip())
m = 2 
r.sendlineafter(b'Enter a message as an integer (enter 0 to stop): ', str(m * pow(2,e,n) % n).encode())
signature = int(r.recvlineS().strip().split(':')[1])
r.sendlineafter(b'Enter a message as an integer (enter 0 to stop): ', b'0')
r.sendlineafter(b'Enter a message: ', str(m-1).encode())
new_sig = signature * pow(2, -1, n) % n 
r.sendlineafter(b'Enter a signature: ', str(new_sig).encode())
r.interactive()