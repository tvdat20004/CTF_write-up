from sage.all import discrete_log_lambda, GF
from pwn import * 
p = 171687271187362402858253153317226779412519708415758861260173615154794651529095285554559087769129718750696204276854381696836947720354758929262422945910586370154930700427498878225153794722572909742395687687136063410003254320613429926120729809300639276228416026933793038009939497928563523775713932771366072739767
r = remote("chall.lac.tf",31179)
# r = process(["python3", 'server.py'])
r.recvuntil(b'Powers of s: ')
ss = eval(r.recvuntilS(b'\n').strip())
r.recvuntil(b'Powers of alpha*s: ')
alphas = eval(r.recvuntilS(b'\n').strip())
alpha = discrete_log_lambda(GF(p)(alphas[0]), GF(p)(ss[0]), (0,2**40-1))
assert pow(ss[1],alpha,p) == alphas[1]
print(alpha)
# first slot
r.recvuntil(b'Coefficients of target polynomial: ')
target = eval(r.recvuntilS(b'\n').strip())
# construct the Polynomial
P = GF(p)['x']
x = P.gen()
f = sum(x**(7 - i)*target[i] for i in range(8))

r.sendlineafter(b"give me your evaluation of f(s) > ", b'12')
r.sendlineafter(b"give me your evaluation of h(s) > ", b'12')
r.sendlineafter(b"give me your evaluation of f(alpha * s) > ",b'12')
ts = int(r.recvlineS().strip().split()[-1])
s = (f - ts).roots()
for root in s:
	if int(root[0]).bit_length() <= 128:
		s = int(root[0])
		break
print(s)
# second slot
r.recvuntil(b'Coefficients of target polynomial: ')
target = eval(r.recvuntilS(b'\n').strip())
ts = sum([(pow(s,7 - i, p) * target[i]) % p for i in range(len(target))]) % p
h = 2 
f = pow(h,ts,p)
fa = pow(f, alpha, p)
r.sendlineafter(b"give me your evaluation of f(s) > ", str(f).encode())
r.sendlineafter(b"give me your evaluation of h(s) > ", str(h).encode())
r.sendlineafter(b"give me your evaluation of f(alpha * s) > ",str(fa).encode())
r.interactive()
# lactf{2kp_1s_ov3rr4t3d}