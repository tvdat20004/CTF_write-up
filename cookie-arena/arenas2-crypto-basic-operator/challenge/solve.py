from sympy.ntheory import sqrt_mod, discrete_log
from Crypto.Util.number import *

mod = 0xffffffff + 1
x = 3442055609
y = 2898124289
p = 1341161101353773850779
e = 2
cipher  = [752589857254588976778, 854606763225554935934, 102518422244000685572, 779286449062901931327, 424602910997772742508, 1194307203769437983433, 501056821915021871618, 691835640758326884371, 778501969928317687301, 1260460302610253211574, 833211399330573153864, 223847974292916916557]

def xor_shift_right_func(data,bit_loc):
	return (data^(data>>bit_loc))&0xffffffff
def rexor_shift_right_func(data):
	bit = bin(data)[2:]
	ans = '' + bit[0]
	for i in range(1,len(bit)):
		ans += str(int(bit[i],2)^int(ans[-1],2))
	return int(ans,2)

def recover(data):

	for tmp in sqrt_mod(data,p,all_roots=True):

		t = discrete_log(p,tmp,e)
		a = rexor_shift_right_func(t)
		# assert tmp % mod == xor_shift_right_func(x,1)
		b = a * pow(y, -1,mod) % mod
		c = (b - x) % mod
		try:
			a = long_to_bytes(c).decode()
			print(a[::-1])
			return c
		except:
			continue
flag = b''
for c in cipher:
	flag += long_to_bytes(recover(c))[::-1]
print(flag)
