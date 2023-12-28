output = []
caesar = lambda v, k: int("".join([str((int(c) - k) % 10) for c in v]))
from Crypto.Util.number import isPrime, long_to_bytes
from sage.all import is_prime
import string
with open("output.txt", 'r') as out:
	for i in out.readlines():
		para = i.split(' ')
		para = [p.strip() for p in para] 
		output.append(para)

flag = b""
for cnt in range(len(output)):
	ct, cp, cq = output[cnt] 
	breaker = 0
	for i_p in range(10):
		for i_q in range(10):
			if isPrime(caesar(cp,i_p)) and isPrime(caesar(cq,i_q)):
				p = caesar(cp,i_p) 
				q = caesar(cq,i_q)
				print(cnt)
				for i_ct in range(10):
					c = caesar(ct, i_ct)
					sub_flag = long_to_bytes(pow(c,pow(65537, -1, (p-1)*(q-1)), p*q))
					# print(sub_flag)
					if all(char in range(33,127) for char in sub_flag):
						flag+= sub_flag
						print(sub_flag)
						breaker = 1
						break
			if breaker:
				break 
		if breaker:
			break 
print(flag)
# b'ictf{rivest_shamir_adleman_is_evirfg_funzve_nqyrzna}'