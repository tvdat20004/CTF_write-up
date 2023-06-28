# LEAST COMMON GENOMINATOR?
<img width="417" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/2b44a317-f465-4b1e-8a94-1e95e23e1668">

- [Attachment](https://storage.googleapis.com/gctf-2023-attachments-project/4e90c59c2c12ac422f0b83094cca2c3e5c4c7cce464dddc5cb2ad391155f11c96a183290a289dfe1c64cc9e3cd467706f07e621904588ca4def3a4f6906234b7.zip)
- Generate.py:
``` python
from secret import config
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, isPrime

class LCG:
    lcg_m = config.m
    lcg_c = config.c
    lcg_n = config.n

    def __init__(self, lcg_s):
        self.state = lcg_s

    def next(self):
        self.state = (self.state * self.lcg_m + self.lcg_c) % self.lcg_n
        return self.state

if __name__ == '__main__':

    assert 4096 % config.it == 0
    assert config.it == 8
    assert 4096 % config.bits == 0
    assert config.bits == 512

    # Find prime value of specified bits a specified amount of times
    seed = 211286818345627549183608678726370412218029639873054513839005340650674982169404937862395980568550063504804783328450267566224937880641772833325018028629959635
    lcg = LCG(seed)
    primes_arr = []
    
    dump = True
    items = 0
    dump_file = open("dump.txt", "w")

    primes_n = 1
    while True:
        for i in range(config.it):
            while True:
                prime_candidate = lcg.next()
                if dump:
                    dump_file.write(str(prime_candidate) + '\n')
                    items += 1
                    if items == 6:
                        dump = False
                        dump_file.close()
                if not isPrime(prime_candidate):
                    continue
                elif prime_candidate.bit_length() != config.bits:
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

    # Create public key 'n'
    n = 1
    for j in primes_arr:
        n *= j
    print("[+] Public Key: ", n)
    print("[+] size: ", n.bit_length(), "bits")

    # Calculate totient 'Phi(n)'
    phi = 1
    for k in primes_arr:
        phi *= (k - 1)

    # Calculate private key 'd'
    d = pow(config.e, -1, phi)

    # Generate Flag
    assert config.flag.startswith(b"CTF{")
    assert config.flag.endswith(b"}")
    enc_flag = bytes_to_long(config.flag)
    assert enc_flag < n

    # Encrypt Flag
    _enc = pow(enc_flag, config.e, n)

    with open ("flag.txt", "wb") as flag_file:
        flag_file.write(_enc.to_bytes(n.bit_length(), "little"))

    # Export RSA Key
    rsa = RSA.construct((n, config.e))
    with open ("public.pem", "w") as pub_file:
        pub_file.write(rsa.exportKey().decode())
```
- Tóm tắt đoạn code trên:
    - Đoạn code trên tạo một object là LCG, trong đó có 3 số được giữ bí mật là m,n,c nhưng bù lại ta biết được giá trị seed. LCG có phương thức `next()` nhằm tạo ra các số có giá trị = `(state*m + c) % n` và lưu nó vào state mới cho các lần tính tiếp theo.
    - Đề bài đã tạo ra các số 512 bits bằng LCG, 6 giá trị đầu tiên tạo ra được lưu vào file `dump.txt`, nếu tạo được số nguyên tố thì lưu vào mảng `primes_arr`, nó sẽ generate cho đến khi `primes_arr` đủ 8 số.
    - Dùng `primes_arr` làm private key để mã hóa RSA, ghi kết quả mã hóa vào file `flag.txt` và export public key ra file `public.pem`.
- Để làm bài trên, ta phải tìm được 3 số m,n,c trong LCG, từ 6 số trong file `dump.txt`
- Tìm n: Giả sử 6 số trong `dump.txt` là x0 tới x5, ta có:
    $\begin{cases} x1 \equiv (x0.m + c)\text{(mod n)} \\ x2 \equiv (x1.m + c)\text{(mod n)} \\ x3 \equiv (x2.m + c)\text{(mod n)}\end{cases}$
    $\Rightarrow \begin{cases} (x2 - x1) \equiv  m(x1 - x0) (mod \ n)  \\ (x3 - x2)  \equiv  m(x2 - x1) (mod \ n) \end{cases}  \Rightarrow  (x2-x1)^2 - (x1-x0)(x3-x2)  \equiv 0 (mod \ n)$
    $\Rightarrow (x2 - x1)^2 - (x3 - x2)(x1 - x0) = kn$ 
    Tương tự: $(x4 - x3)^2 - (x3 - x2)(x5 - x4) = tn$
    Do đó n là ước của gcd 2 số trên.
    Ở bài này ta may mắn tìm được luôn n là gcd 2 số đó.
- Tìm m: Vì $(x2 - x1) \equiv  m * (x1 - x0) (mod \ n)$ nên $m = (x2-x1).(x1-x0)^{-1} (mod \ n)$
- Tìm c: Vì $x1 \equiv (x0*m + c)\text{(mod n)}$ nên $c = x1 - m.x0  \ (mod \ n)$
- Tìm được m,c,n rồi, ta chỉ cần nạp chúng vào LCG và để nó tự generate private key.
- Source code:
``` python
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
```
- Flag: CTF{C0nGr@tz_RiV35t_5h4MiR_nD_Ad13MaN_W0ulD_b_h@pPy}
# Primes
<img width="411" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/146d3d53-6bba-4c05-a046-74593ff27693">

- [Attachment](https://storage.googleapis.com/gctf-2023-attachments-project/3c5f79f4457ce1c12972d6028686a5ba7e028ac95f19081210208720f77cb02286519e3591215c3752a22cf5cd3cae275efb31f77edb209f01e8d93f0f77601c.zip)
- chall.sage
```python
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def to_bits(m):
    _bin = lambda b : [1 if b & (1 << n) else 0 for n in range(7)]
    return sum([_bin(b) for b in m], [])

def gen_primes(r, n):
    primes = Primes()[:n]
    bound = prod(primes[n - r:])
    return primes, next_prime(bound)

def prod_exp(p, q, b):
    return prod([p[i]^b[i] for i in range(len(p))]) % q

def encode(r, n, m):
    p, q = gen_primes(r, n)
    return p, q, prod_exp(p, q, to_bits(m))

m = b"I have a sweet flag for you: CTF{YkDOLIStjpjP5Am1SXDt5d2r9es3b5KZP47v8rXF}"
p, q, x = encode(131, 7*len(m), m)
print(f'q = 0x{q:X}\nx = 0x{x:X}')

# q = 0xD2F8711CB5502C512ACEA59BE181A8FCF12F183B540D9A6998BF66370F9538F7E39FC507545DAD9AA2E71D3313F0B4408695A0A2C03A790662A9BD01650533C584C90779B73604FB8157F0AB7C9A82E724700E5937D9FF5FCF1EE3BE1EDD7E07B4C0F035A58CC2B9DB8B79F176F595C1B0E90B7957309B96106A50A01B78171599B41C8744BCB1C0E6A24F60AE8946D37F4D4BD8CF286A336E1022996B3BA3918E4D808627D0315BFE291AEB884CBE98BB620DAA735B0467F3287D158231D
# x = 0x947062E712C031ADD0B60416D3B87D54B50C1EFBC8DBB87346F960B242AF3DF6DD47406FEC98053A967D28FE91B130FF0FE93689122931F0BA6E73A3E9E6C873B8E2344A459244D1295E99A241E59E1EEA796E9738E6B1EDEED3D91AE6747E8ECA634C030B90B02BAF8AE0088058F6994C7CAC232835AC72D8B23A96F10EF03D74F82C49D4513423DAC298698094B5C631B9C7C62850C498330E9D112BB9CAA574AEE6B0E5E66D5B234B23C755AC1719B4B68133E680A7BCF48B4CFD0924D
```
- Tóm tắt đề:
    - Đầu tiên, chuỗi bytes m sẽ được đưa vào hàm `to_bits` để đưa về chuỗi nhị phân bằng cách mỗi ký tự trong plaintext được đổi ra chuỗi nhị phân 7 bits theo thứ tự little edian và nối lại.
    - Số p chính là dãy gồm `7*len(flag) = 518` số nguyên tố đầu tiên, số bound trong hàm `next_primes` là tích của 131 số nguyên tố cuối cùng trong p, còn q là số nguyên tố nhỏ nhất lớn hơn bound (từ đó ta thấy p,q cố định do không phụ thuộc vào flag).
    - Tiếp theo hàm `prod_exp` sẽ tính x bằng cách lấy tích các `p[i]^b[i]` rồi mod q với `b = to_bits(m)`.
- Ở đây do có 1 phần plaintext đã biết nên mình sẽ làm các thao tác y như đề bài đã làm với plaintext, ta sẽ thu được số k (`k = prod_exp(p,q,to_bits(known_text))`)
- Tới đây mình nhận ra `k * prod_exp(p,q, to_bits(unknown_text)) = x mod q`, do đó mình sẽ tính $x*k^{-1} mod \ q$ để tính giá trị kia, nhưng thực ra nó không phải giá trị ta muốn tìm :') mà nó chỉ là đồng dư với giá trị cần tìm. Giả sử kết quả phép toán trên là tmp, ta cần tìm giá trị của `ct = prod_exp(p,q, to_bits(unknown_text))`, ta có:
    - $tmp\equiv ct (mod \ q)$ (1)(như đã nói ở trên)
    - ct là ước của maxx với maxx là tích của `7*len(unknow_text)` số nguyên tố cuối cùng trong p, điều này được suy ra bởi ct là một subset product của list các số nguyên tố trên. Do đó $maxx = t.ct$
    - Nhân vào 2 vế của (1) với t, ta được $maxx \equiv t.tmp (mod \ q)\Rightarrow  t = maxx.tmp^{-1} (mod \ q)$. Sau khi tìm được t, mình dễ dàng tìm được `ct = maxx // t`
    - Việc tìm trên cũng có khả năng ra kết quả không như mong muốn (cũng vì tìm nghiệm trong phương trình đồng dư có thể cho nhiều đáp án), tuy nhiên khi tính được giá trị ct mình đã check lại 2 điều kiện trên và nó pass :)) do đó việc ta phải làm bây giờ là khôi phục lại chuỗi bits và tìm plaintext thôi.
- solve.sage
``` python
q = 0xD2F8711CB5502C512ACEA59BE181A8FCF12F183B540D9A6998BF66370F9538F7E39FC507545DAD9AA2E71D3313F0B4408695A0A2C03A790662A9BD01650533C584C90779B73604FB8157F0AB7C9A82E724700E5937D9FF5FCF1EE3BE1EDD7E07B4C0F035A58CC2B9DB8B79F176F595C1B0E90B7957309B96106A50A01B78171599B41C8744BCB1C0E6A24F60AE8946D37F4D4BD8CF286A336E1022996B3BA3918E4D808627D0315BFE291AEB884CBE98BB620DAA735B0467F3287D158231D
x = 0x947062E712C031ADD0B60416D3B87D54B50C1EFBC8DBB87346F960B242AF3DF6DD47406FEC98053A967D28FE91B130FF0FE93689122931F0BA6E73A3E9E6C873B8E2344A459244D1295E99A241E59E1EEA796E9738E6B1EDEED3D91AE6747E8ECA634C030B90B02BAF8AE0088058F6994C7CAC232835AC72D8B23A96F10EF03D74F82C49D4513423DAC298698094B5C631B9C7C62850C498330E9D112BB9CAA574AEE6B0E5E66D5B234B23C755AC1719B4B68133E680A7BCF48B4CFD0924D
# x = 0x38FC218F4357A4211E5B658BFEDFC0FE390248200DE63E898F9965C369B50CD246AE6953A687BD8753F0FC2D279139C1B0F3889F81C2A12AFB5B70B68F16EF05E80D534DBD04A10B6EC0B0032D739C041D7E126D93C5F7CED5162456B45760173BED1FAD043DEE833F452B96356C46AF34AFCF616EBE261E625E3DBA60E1550460E037CE2B79FAD9FA01B8B6970D6F59B819B5198C9F351D1D0B30A2AD029D18BBD334A4CEE7AF14E01B893D37AA2854CF1DAAC81E7034756C6458B76B45D

def to_bits(m):
    _bin = lambda b : [1 if b & (1 << n) else 0 for n in range(7)]
    return sum([_bin(b) for b in m], [])
len_flag = 74
def gen_primes(r, n):
    primes = Primes()[:n]
    bound = prod(primes[n - r:])
    return primes, next_prime(bound)

def prod_exp(p, q, b):
    return prod([p[i]^b[i] for i in range(len(b))])

p,_ = gen_primes(131, 7*len_flag)
print(len(p))
known_text = b'I have a sweet flag for you: CTF{'
k = prod_exp(p,q,to_bits(known_text))

tmp = x * pow(int(k),-1,q)
bit = ""
maxx = prod(p[len(known_text)*7:])

# print((int(maxx) - int(tmp))//q)
t = maxx * pow(tmp,-1,q)
assert int(maxx) % int(t) == 0 
ct = int(maxx) // int(t)
assert int(ct) * int(k) % q == x
assert (int(tmp) - int(ct)) % q == 0
for i in p[len(known_text) * 7:]:
	if int(ct) % int(i) == 0:
		bit += '1'
	else:
		bit += '0'
print(bit)
flag = known_text
for i in range(0,len(bit),7):
	flag += int(bit[i:i+7][::-1],2).to_bytes()
print(flag)
# b'I have a sweet flag for you: CTF{w0W_c0Nt1nUed_fr4Ct10ns_suR3_Ar3_fUn_Huh}'
```
- Flag: CTF{w0W_c0Nt1nUed_fr4Ct10ns_suR3_Ar3_fUn_Huh}
WU bản đẹp: https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/Symscu__n
