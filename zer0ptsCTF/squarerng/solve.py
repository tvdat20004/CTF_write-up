from pwn import *

r = remote('crypto.2023.zer0pts.com', 10666)
def isSquare(a, p):
    return pow(a, (p-1)//2, p) != p-1



def get_para():
	data = r.recvuntil(b'1:')
	random1 = bin(int(r.recvuntil(b'\n').decode().strip()[2:], 16))[2:]
	data = r.recvuntil(b'2:')
	random2 = bin(int(r.recvuntil(b'\n').decode().strip()[2:], 16))[2:]
	while len(random1) < 32:
		random1 = '0' + random1
	while len(random2) < 32:
		random2 = '0' + random2
	return random1, random2

def guess(random1, random2):
	print(random1)
	print(random2)
	if random1[0] == '1':
		r1 = 1
	else:
		r1 = -1
	if random2[-1] == '1':
		r2 = 1
	else:
		r2 = -1
	print(r1,r2)
	if r1*r2 == 1:
		ans = 1
	else: 
		ans = 0
	data = r.recvuntil(b']: ')
	r.sendline(str(ans).encode())
	mess = r.recvline()
	print(mess)

data = r.recvuntil(b'seed 1: ')
r.send(b'1\n')
data = r.recvuntil(b'seed 2: ')
r.send(b'-1\n')
for i in range(77):
	random1, random2 = get_para()
	# print(random1)
	# print(random2)
	guess(random1, random2)
flag = r.recv(2024)
print(flag)
r.close()
