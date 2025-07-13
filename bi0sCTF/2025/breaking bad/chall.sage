import random
import string
import hashlib
from Crypto.Util.number import bytes_to_long

message = b'<REDACTED>'

n = 100
Bn = BraidGroup(n)
gs = Bn.gens()
K = 32

gen = gs[n // 2 - 1]
p_list = [gen] + random.choices(gs, k=K-1)
p = prod(p_list)
print(f"p: {list(p.Tietze())}")

a = prod(random.choices(gs[:n//2-2], k=K))
v = a * u * a^-1
print(f"q: {list(v.Tietze())}")

br = prod(random.choices(gs[n//2 + 1:], k=K))
w = br * u * br^-1
c = br * v * br^-1
assert c == a * w * a^-1
h = hashlib.sha512(str(prod(c.right_normal_form())).encode()).digest()
print(h.hex())
original_message_len = len(message)
pad_length = len(h) - original_message_len
left_length = random.randint(0, pad_length)
pad1 = ''.join(random.choices(string.ascii_letters, k=left_length)).encode('utf-8')
pad2 = ''.join(random.choices(string.ascii_letters, k=pad_length - left_length)).encode('utf-8')
padded_message = pad1 + message + pad2

d_str = ''.join(chr(m ^^ h) for m, h in zip(padded_message, h))
d = bytes_to_long(d_str.encode('utf-8'))

print(f"c1: {list(w.Tietze())}")
print(f"c2: {d}")
# print(c.Tietze())
# a*p*_a = a*_br * c1 * br*_a 



