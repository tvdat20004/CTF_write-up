from pwn import * 
r = remote("00.cr.yp.toc.tf", 13377)


def get_para():
	r.recvuntil(b'Also, f(')
	x1 = int(r.recvuntilS(b') = ').strip()[:-3])
	y1 = int(r.recvuntilS(b',').strip()[:-1])
	r.recvuntil(b'f(')
	x2 = int(r.recvuntilS(b')').strip()[:-1])
	y2 = int(r.recvlineS().strip().split(' ')[1])
	assert (y1 - y2) % (x1 - x2) == 0
	a = (y1 - y2) // (x1 - x2)
	b = y1 - a*x1
	return a,b  
	
a,b = get_para()
while True:
	try:
		r.recvuntil(b'f(')
		x3 = int(r.recvuntilS(b')').strip()[:-1])
		ans = a*x3 + b 
		r.sendlineafter(b':\n', str(ans).encode())
	except:
		break
r.interactive()
# CCTF{A_funCti0nal_3qu4tiOn_iZ_4_7yPe_oF_EquAtioN_tHaT_inv0lVe5_an_unKnOwn_funCt!on_r4tH3r_thAn_juS7_vArIabl3s!!}
