# SEETF 2023
## baby RC4
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/2fd783af-2207-4395-b814-0b1ecc895dff)
- [Attachment](https://github.com/tvdat20004/CTF_write-up/blob/main/SEETF%202023/baby_RC4/chall.py)
- Source code:
``` py
from Crypto.Cipher import ARC4
from os import urandom
key = urandom(16)
flag = b'SEE{?????????????????????????????????}'[::-1]

def enc(ptxt):
    cipher = ARC4.new(key)
    return cipher.encrypt(ptxt)

print(f"c0 = bytes.fromhex('{enc(flag).hex()}')")
print(f"c1 = bytes.fromhex('{enc(b'a'*36).hex()}')")

"""
c0 = bytes.fromhex('b99665ef4329b168cc1d672dd51081b719e640286e1b0fb124403cb59ddb3cc74bda4fd85dfc')
c1 = bytes.fromhex('a5c237b6102db668ce467579c702d5af4bec7e7d4c0831e3707438a6a3c818d019d555fc')
"""
```
- Đây là một bài mã hóa RC4 với static key, ở đây mình tham khảo source code trên repo [này](https://github.com/gexxxter/RC4StaticKeyAttack/blob/master/rc4Cracker.py):D
- Solve:
```python
#! /usr/bin/python
from argparse import ArgumentParser
import sys

def main():
    knownPlaintext = b'a'*36
    knownCiphertext = bytes.fromhex('a5c237b6102db668ce467579c702d5af4bec7e7d4c0831e3707438a6a3c818d019d555fc')
    unknownCiphertext = bytes.fromhex('b99665ef4329b168cc1d672dd51081b719e640286e1b0fb124403cb59ddb3cc74bda4fd85dfc')

    decrypted = bytearray()
    for i in range(0, len(unknownCiphertext)):
        p = knownPlaintext[i % len(knownPlaintext)]
        c1 = knownCiphertext[i % len(knownCiphertext)]
        c2 = unknownCiphertext[i] 
        decrypted.append(p ^ c1 ^ c2)
        
    sys.stdout.buffer.write(decrypted[::-1])


if __name__=='__main__':
	main()
```
- flag: SEE{n3vEr_reU53_rC4_k3y5ss5s:cafe2835}
## dumb-chall
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/3e682135-fdd1-42f8-a73d-d5ec23c1e265)
- [Attachment](https://github.com/tvdat20004/CTF_write-up/blob/main/SEETF%202023/dumb-chall/main.py)
- Source code:
``` python
import random
import time
from Crypto.Util.number import bytes_to_long, isPrime

from secret import FLAG


def fail():
    print("You have disappointed the pigeon.")
    exit(-1)


def generate_prime_number(bits: int = 128) -> int:
    num = random.getrandbits(bits)
    while not isPrime(num):
        num += 1
    return num


def generate_random_boolean() -> bool:
    return bool(random.getrandbits(1))


def first_verify(g, p, y, C, w, r) -> bool:
    assert w
    return ((y * C) % p) == pow(g, r, p) 


def second_verify(g, p, y, C, w, r) -> bool:
    assert r
    return pow(g, r, p) == C


p = generate_prime_number()
g = random.getrandbits(128)
x = bytes_to_long(FLAG.encode())
y = pow(g, x, p)

print(f"p = {p}")
print(f"g = {g}")
print(f"y = {y}")

print("Something something zero-knowledge proofs blah blah...")
print("Why not just issue the challenge and the verification at the same time? Saves TCP overhead!")

seen_c = set()
for round in range(30):
    w, r = None, None
    choice = generate_random_boolean()
    if not choice:
        w = int(input("Enter w: "))
        C = int(input("Enter C: "))
        if C in seen_c:
            fail()
        seen_c.add(C)
        verify = first_verify
    else:
        r = int(input("Enter r: "))
        C = int(input("Enter C: "))
        if C in seen_c:
            fail()
        seen_c.add(C)
        verify = second_verify
    if not verify(g, p, y, C, w, r):
        fail()
    else:
        print(f"You passed round {round + 1}.")
time.sleep(1)
print(
    "You were more likely to get hit by lightning than proof correctly 30 times in a row, you must know the secret right?"
)
print(f"A flag for your troubles - {FLAG}")
```
- Đây là một chủ yếu thử thách về kỹ năng socket programing của chúng ta. Họ tạo ta một thử thách gồm 30 round, nhiệm vụ mỗi round có 2 dạng:
    - Dạng 1 yêu cầu ta nhập w và C sao cho pass được hàm `first_verify`
    - Dạng 2 yêu cầu ta nhập r và C sao cho pass được hàm `second verify`
- Thêm vào đó, các giá trị C ta nhập vào phải không được trùng nhau.
- Điểm chung 2 dạng là đều yêu cầu ta nhập vào 2 giá trị để thỏa mãn một biểu thức modulo được định nghĩa trong 2 hàm verify. Ở đây mình sẽ cho các giá trị w hoặc r bằng i ở round thứ i, từ đó tính C. Mục đích của mình như vậy là do w và r đều nằm trên mũ, nếu ta cho C và tính giá trị w hoặc r thì nó sẽ đưa về bài toán discrete log. Việc giải nó sẽ tốn nhiều thời gian và tài nguyên hơn và vẫn chưa có thuật toán hiệu quả nào giải quyết được bài toán này nói chung. Còn khi cho trước giá trị r hoặc w, việc tính C là khá đơn giản
    - `first_verify`: $y.C = g^r\text{(mod p)} \Leftrightarrow C = g^r . y^{-1} \text{(mod p)}$
    - `seconf_verify`: $C = g^r \text{(mod p)}$
- Việc còn lại là code một chương trình tự động kết nối socket và lấy flag.
- Source code:
``` python
from pwn import *

conn = remote("win.the.seetf.sg", 3002)

p_line = conn.recvline().decode().strip()
g_line = conn.recvline().decode().strip()
y_line = conn.recvline().decode().strip() 

p = int(p_line.split('=')[1].strip())
g = int(g_line.split('=')[1].strip())
y = int(y_line.split('=')[1].strip())
def verify1(w):
	return pow(g,w,p)*pow(y,-1,p)

def verify2(r):
	return pow(g, r, p)

for i in range(1,31):
	data = conn.recvuntil(b':')
	if b'Enter w' in data:
		verify = verify1
	else: verify = verify2
	# data = conn.recvuntil(b':')
	conn.sendline(str(i).encode())
	data = conn.recvuntil(b':')
	conn.sendline(str(verify(i)).encode())
	data = conn.recvline()
	print(data)
print(conn.recv(2024).decode())
conn.close()
```
![image](https://github.com/tvdat20004/CTF_write-up/blob/main/SEETF%202023/dumb-chall/Screenshot%202023-06-10%20222121.png)
## OpenEndedRSA
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/23ac0934-121e-43fa-b28c-f732f246f380)
- [Attachment](https://github.com/tvdat20004/CTF_write-up/blob/main/SEETF%202023/open_ended_RSA/chall.py)
- Source code:
```python
from Crypto.Util.number import *
from gmpy2 import iroot # this helps with super accurate square root calculations!

flag = b'????????????????????????'
m = bytes_to_long(flag)
e = 0x10001
pp = bytes_to_long(b'????????????????')
s = 1
assert isPrime(pp)

while not isPrime(s):
    p = getPrime(512)
    s = p**2 + pp**2 

assert iroot(s-pp**2,2) == (p, True)  # quick demo on how to use iroot()
assert s%2 == 1                       # duh, s is a prime number after all!

q = getPrime(512)
n = p*q
c = pow(m,e,n)

print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')
print(f's = {s}')

"""
n = 102273879596517810990377282423472726027460443064683939304011542123196710774901060989067270532492298567093229128321692329740628450490799826352111218401958040398966213264648582167008910307308861267119229380385416523073063233676439205431787341959762456158735901628476769492808819670332459690695414384805355960329
e = 65537
c = 51295852362773645802164495088356504014656085673555383524516532497310520206771348899894261255951572784181072534252355368923583221684536838148556235818725495078521334113983852688551123368250626610738927980373728679163439512668552165205712876265795806444660262239275273091657848381708848495732343517789776957423
s = 128507372710876266809116441521071993373501360950301439928940005102517141449185048274058750442578112761334152960722557830781512085114879670147631965370048855192288440768620271468214898335819263102540763641617908275932788291551543955368740728922769245855304034817063220790250913667769787523374734049532482184053
"""
```
- Đây là một bài có dạng tương tự một bài ở giải HCMUS CTF 2023, write-up mình đã viết ở [đây](https://github.com/tvdat20004/CTF_write-up/blob/main/hcmus/M_side.md)
- Source code:
```python
n = 102273879596517810990377282423472726027460443064683939304011542123196710774901060989067270532492298567093229128321692329740628450490799826352111218401958040398966213264648582167008910307308861267119229380385416523073063233676439205431787341959762456158735901628476769492808819670332459690695414384805355960329
e = 65537
c = 51295852362773645802164495088356504014656085673555383524516532497310520206771348899894261255951572784181072534252355368923583221684536838148556235818725495078521334113983852688551123368250626610738927980373728679163439512668552165205712876265795806444660262239275273091657848381708848495732343517789776957423
s = 128507372710876266809116441521071993373501360950301439928940005102517141449185048274058750442578112761334152960722557830781512085114879670147631965370048855192288440768620271468214898335819263102540763641617908275932788291551543955368740728922769245855304034817063220790250913667769787523374734049532482184053
from Crypto.Util.number import *
from gmpy2 import iroot
def find_p():
	a = 1
	while pow(a,(s-1)//2,s) != s-1:
		a += 1
	x = pow(a, (s-1)//4, s)
	# print(x)
	p = s
	while p > iroot(s,2)[0] or x > iroot(s,2)[0]:
		p,x = max(x,p%x), min(x,p%x)
	q = iroot(s-p**2,2)[0]
	assert p**2 + q**2 == s
	if n%p == 0:
		return p
	elif n%q == 0:
		return q
	else:
		return None
p = find_p()
q = n//p
phi = (p-1)*(q-1)
print(long_to_bytes(pow(c,pow(e,-1,phi),n)))

# b'SEE{0dd_3vEN:deadbeef}'
```
- Flag: SEE{0dd_3vEN:deadbeef}
> https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/SkLsfJHvh
