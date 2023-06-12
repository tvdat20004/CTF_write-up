from pwn import *

conn = remote("win.the.seetf.sg", 3002)

p_line = conn.recvline().decode().strip()
g_line = conn.recvline().decode().strip()
y_line = conn.recvline().decode().strip() 

p = int(p_line.split('=')[1].strip())
g = int(g_line.split('=')[1].strip())
y = int(y_line.split('=')[1].strip())
def verify1(w):
	return pow(g,w,p)*pow(y,-1,p)

def verify2(r):
	return pow(g, r, p)

for i in range(1,31):
	data = conn.recvuntil(b':')
	if b'Enter w' in data:
		verify = verify1
	else: verify = verify2
	# data = conn.recvuntil(b':')
	conn.sendline(str(i).encode())
	data = conn.recvuntil(b':')
	conn.sendline(str(verify(i)).encode())
	data = conn.recvline()
	print(data)
print(conn.recv(2024).decode())
conn.close()