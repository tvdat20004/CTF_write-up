from math import gcd
from Crypto.Util.number import getPrime, getRandomNBitInteger, bytes_to_long
# from secret import flag
flag = b'fake_flag'
lcm = lambda u, v: u*v//gcd(u, v)

bits = 1024
given = bits // 5 # 204
e_bits = bits // 12 # 85

mask = (1 << given) - 1 # 25711008708143844408671393477458601640355247900524685364822015

while True:
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    N = p * q

    if N.bit_length() != bits:
        continue
    l = lcm(p - 1, q - 1)
    e = getRandomNBitInteger(e_bits)

    if gcd(e, l) > 1:
        continue

    d = pow(e, -1, l)

    dp = int(d % (p - 1))
    dq = int(d % (q - 1))

    break

l_dp = dp & mask 
l_dq = dq & mask 
print(((dp - l_dq)//2**204).bit_length())
print(f'{N = }')
print(f'{e = }')
print(f'{l_dp = }')
print(f'{l_dq = }')

flag = bytes_to_long(flag)

ct = pow(flag, e, N)
print(f'{ct = }')
