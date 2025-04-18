from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, isPrime
from math import gcd
# from secret import config

# Đọc file .pem chứa public key RSA
with open('public.pem', 'r') as f:
    key = RSA.importKey(f.read())

# Lấy public key RSA từ file .pem
n = key.publickey().n
e = key.publickey().e

with open("flag.txt", 'rb') as ct:
    ct = ct.read()
ct = int.from_bytes(ct, byteorder='little')
with open("dump.txt", "r") as dump:
    dump = dump.read().strip().split('\n')
    dump = [int(d) for d in dump]
seed = 211286818345627549183608678726370412218029639873054513839005340650674982169404937862395980568550063504804783328450267566224937880641772833325018028629959635
n_lcg = gcd((dump[2] - dump[1])**2 - (dump[1] - dump[0]) * (dump[3] - dump[2]), (dump[4] - dump[3])**2 - (dump[3]-dump[2])*(dump[5]-dump[4]))
m_lcg = (dump[2]-dump[1])*pow((dump[1]-dump[0]), -1, n_lcg) % n_lcg
c_lcg = (dump[1] - dump[0]*m_lcg) % n_lcg

class LCG:
    lcg_m = m_lcg
    lcg_c = c_lcg
    lcg_n = n_lcg

    def __init__(self):
        self.state = seed
    def next(self):
        self.state = (self.state * self.lcg_m + self.lcg_c) % self.lcg_n
        return self.state
lcg = LCG()
primes_arr = []
bdump = True
items = 0
primes_n = 1
while True:
    for i in range(8):
        while True:
            prime_candidate = lcg.next()
            if bdump:
                items += 1
                if items == 6:
                    bdump = False
            if not isPrime(prime_candidate):
                continue
            elif prime_candidate.bit_length() != 512:
                continue
            else:
                primes_n *= prime_candidate
                primes_arr.append(prime_candidate)
                break
    
    # Check bit length
    if primes_n.bit_length() > 4096:
        print("bit length", primes_n.bit_length())
        primes_arr.clear()
        primes_n = 1
        continue
    else:
        break
assert n == primes_n
phi = 1
for k in primes_arr:
    phi *= (k - 1)
print(long_to_bytes(pow(ct,pow(e,-1,phi),n)))
# b'CTF{C0nGr@tz_RiV35t_5h4MiR_nD_Ad13MaN_W0ulD_b_h@pPy}'