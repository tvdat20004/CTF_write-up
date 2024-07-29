from string import printable 
characters = printable
from pwn import *
from tqdm import trange
def f(suffix, plaintext):
	while len(suffix) and len(plaintext) and plaintext[-1] == suffix[0]:
		plaintext = plaintext[:-1]
		suffix = suffix[1:]
	return plaintext + suffix
# flag = b"justCTF{temporary-reverse-cryptographing-flag}"
# suffix = b'}galfflag}'
# print(f(suffix, flag))
# r = process(["python3", "task.py"])
# nc reversecryptographing.nc.jctf.pro 1337
r = remote("reversecryptographing.nc.jctf.pro", 1337)
r.sendline(b'')
resp = r.recvline()	
# flag = ""
flag = 'PP4h_r333bMer_yAwl4__krr4d_5i_yaD_n3w}'
double = False
triple = False
four_ple = False
for i in trange(50):
	for c in characters:
		tmp = c + flag
		if double:
			tmp = c + tmp 
		if triple:
			tmp = c + tmp 
		if four_ple:
			tmp = c + tmp
		suffix = tmp[::-1] + tmp 
		r.sendline(suffix.encode().hex().encode())
		if r.recvline() == resp:
			flag = tmp
			double = False
			triple = False 
			four_ple = False
			break
	else:
		if triple:
			four_ple = True
		if double:
			triple = True
		double = True

	print(flag)
print(flag)
# justCTF{y4d_yyyyPP4h_r333bMer_yAwl4__krr4d_5i_yaD_n3w}