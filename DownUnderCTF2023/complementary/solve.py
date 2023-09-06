from sage.all import divisors
from Crypto.Util.number import long_to_bytes
n = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278

for factor in divisors(n):
	other = n//factor
	flag1 = long_to_bytes(factor)
	flag2 = long_to_bytes(other)
	if b'DUCTF{' in flag1 or b'DUCTF{' in flag2:
		print(flag1 + flag2)
		print(flag2 + flag1)
		break
# DUCTF{is_1nt3ger_f4ct0r1s4t10n_h4rd?}
