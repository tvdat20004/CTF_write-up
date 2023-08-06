from pwn import *
from Crypto.Util.number import *
from sympy.ntheory import discrete_log 
r = remote("34.154.18.2", 6951)
data = r.recvuntil(b'Public: ')
def get_param(s : str):
	return [int(i) for i in s.split(' ')]

def solve(l1, l2):
	[s1,s2,m] = l1
	[_s1,_s2,_m] = l2 
	print(GCD(p-1,s1))
	print(GCD(p-1,_s1))
	gcd = GCD(s1,p-1)
	_gcd = GCD(_s1, p-1)
	a1 = (s2//gcd)  * pow(s1//gcd,-1,p-1)
	b1 = (m//gcd) * pow(s1//gcd,-1,p-1)
	a2 = (_s2//_gcd) * pow(_s1//_gcd,-1,p-1)
	b2 = (_m//_gcd) * pow(_s1//_gcd,-1,p-1)
	gcd = GCD(a1 - a2, p-1)
	k = ((b1 - b2)//gcd) * pow((a1 - a2) // gcd, -1, p-1) % (p-1)
	flag = (b1 - a1 * k) % (p-1)
	return long_to_bytes(flag)

p,g,A = eval(r.recvline().decode())
print(p)
print(g)
print(A)
l1 = get_param(r.recvline().decode())
l2 = get_param(r.recvline().decode())
# while True:
# 	try:
# 		flag = solve(l1,l2)
# 		print(flag)
# 		break
# 	except:
# 		l1 = get_param(r.recvline().decode())
# 		l2 = get_param(r.recvline().decode())
# 		continue
print(solve(l1,l2))
r.close()
