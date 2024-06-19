from pwn import *  
from Crypto.Util.number import *
r = remote("01.cr.yp.toc.tf", 17113)
while True:
	try:
		r.recvuntil(b'We know: ')
		data = r.recvlineS().strip().split(' ')
		a = int(data[3])
		b = int(data[8])
		x,y = b - a + 1, b - a 
		r.sendlineafter(b'comma: \n', (str(x) + ',' + str(y)).encode())
	except:
		r.interactive()