from pwn import *
from Crypto.Util.number import getPrime  
# r = process(["python3", "ally.py"])
r = remote("00.cr.yp.toc.tf", 13777)

def gen_prime(nbit):
	while True:
		p = getPrime(nbit)
		if (p-1) % 4 == 0:
			return p 
for i in range(20):
	r.recvuntil(b'Please send your')
	nbit = int(r.recvlineS().strip().split('-')[0])
	p = gen_prime(nbit)
	r.sendline(str(p).encode())
	y = (p - 1)//4
	x = 2*y + 1 
	assert p * (x - y)**3 == (x**2 + y) * (x + y**2) 
	r.sendlineafter(b')\n',(f'{x},{y}').encode())
r.interactive()
# CCTF{Di0phaNtinE_eQuaT1on_iZ_4n_equ4tion_wiTh_int3ger_solu7Ions_0nly!}