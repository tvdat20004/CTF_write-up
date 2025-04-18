from pwn import * 
r = remote("challs.nusgreyhats.org",32222)

enc = r.recvlineS().split(':')[1].strip()
blocks = [enc[i:i+32] for i in range(0, len(enc), 32)]
send = ""
for i in range(5):
	send += blocks[i]*2

r.sendlineafter(b'> ', send.encode())
r.interactive()