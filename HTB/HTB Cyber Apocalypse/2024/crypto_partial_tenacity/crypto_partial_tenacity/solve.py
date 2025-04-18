n = 118641897764566817417551054135914458085151243893181692085585606712347004549784923154978949512746946759125187896834583143236980760760749398862405478042140850200893707709475167551056980474794729592748211827841494511437980466936302569013868048998752111754493558258605042130232239629213049847684412075111663446003
ct = bytes.fromhex('7f33a035c6390508cee1d0277f4712bf01a01a46677233f16387fae072d07bdee4f535b0bd66efa4f2475dc8515696cbc4bc2280c20c93726212695d770b0a8295e2bacbd6b59487b329cc36a5516567b948fed368bf02c50a39e6549312dc6badfef84d4e30494e9ef0a47bd97305639c875b16306fcd91146d3d126c1ea476')
p_half = "151441473357136152985216980397525591305875094288738820699069271674022167902643"
q_half = "15624342005774166525024608067426557093567392652723175301615422384508274269305"
sol = {(0,0)}
p,q = 0,0
for i in range(len(p_half + q_half)):
	# cur_sol = set()
	m = 10**(i+1)
	# for p,q in sol:
	if i % 2 == 0: 
		p = int(p_half[-1]) *10**i + p
		for c in range(10):
			tmp_q = c*10**i + q  
			if (tmp_q*p) % m == n % m:
				q = tmp_q
				break
		p_half = p_half[:-1]
	else:
		q = int(q_half[-1])*10**i + q
		for c in range(10):
			tmp_p = c * 10**i + p
			if (tmp_p * q) % m == n % m:
				p = tmp_p
				break
		q_half = q_half[:-1]
from Crypto.Util.number import * 
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.PublicKey import RSA 
assert isPrime(p) and isPrime(q) and p*q==n 
e = 65537
d = pow(e,-1,(p-1)*(q-1))
key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
flag = cipher.decrypt(ct)
print(flag)
# pt = long_to_bytes(pow(ct,pow(65537, -1, (p-1)*(q-1)), n))