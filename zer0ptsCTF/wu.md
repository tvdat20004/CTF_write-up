# easy factoring
<img width="662" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/d5deff04-b45d-4661-b266-d7b730d0c6fb">

- [Attachment](https://storage.googleapis.com/zer0ptsctf2023/76af7ecc-3bba-4b69-a59b-9c9a1f16b4f8/easy_factoring_63618afc3b4df329032c7d719aacc071.tar.gz)
> server.py
```python
import os
import signal
from Crypto.Util.number import *

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

def main():
    p = getPrime(128)
    q = getPrime(128)
    n = p * q

    N = pow(p, 2) + pow(q, 2)

    print("Let's factoring !")
    print("N:", N)

    p = int(input("p: "))
    q = int(input("q: "))

    if isPrime(p) and isPrime(q) and n == p * q:
        print("yey!")
        print("Here you are")
        print(flag)
    else:
        print("omg")

def timeout(signum, frame):
    print("Timed out...")
    signal.alarm(0)
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    main()
    signal.alarm(0)

```
- Tóm tắt lại đoạn code thì ta thấy đơn giản server sẽ tạo 2 số nguyên tố p và q, sau đó cho ta giá trị `p**2 + q**2` và bắt chúng ta tìm ra 2 số p,q ban đầu. 
- Để tìm 2 số khi biết tổng bình phương 2 số đó thì mình sẽ dùng một hàm có sẵn trong sagemath là `two_square`. Docs nói về hàm đó mình để ở [đây](https://doc.sagemath.org/html/en/reference/rings_standard/sage/arith/misc.html#sage.arith.misc.two_squares)
- Tuy nhiên hàm này chỉ tìm được 1 cặp giá trị (a,b) sao cho tổng bình phương của nó = n chứ không đảm bảo được a và b là 2 số nguyên tố, thậm chí mình thử thì có một vài số nó còn không tìm được a,b 😐. Vậy nên mình sẽ cho chương trình kết nối nhiều lần và thử cho đến khi nhận flag, đến đây sẽ thử thách nhân phẩm của người chạy code :))
> solve.py
```python
from pwn import *
from Crypto.Util.number import isPrime
from sage.all import *

while True:
	r = remote("crypto.2023.zer0pts.com", 10333)
	data = r.recvuntil(b'N:')
	n = int(r.recvline().decode().strip())
	try:
		p,q = two_squares(n)
	except:
		r.close()
		continue

	if isPrime(int(p)) and isPrime(int(q)):
		data = r.recvuntil(b'p: ')
		r.sendline(str(int(p)).encode())
		data = r.recvuntil(b'q: ')
		r.sendline(str(int(q)).encode())
		flag = r.recv(2024)
		print(flag)
		r.close()
		break
	else:
		r.close()
```
- Kết quả:
![]([https://hackmd.io/_uploads/S1jIz7f5h.png](https://github.com/tvdat20004/CTF_write-up/blob/main/zer0ptsCTF/easy_factoring/Screenshot%202023-07-15%20154703.png))
> Lưu ý do mình in kết quả dạng bytes nên dấu nháy đơn (') sẽ có dấu \ ở trước, vì vậy khi nộp flag ta loại bỏ nó.
# squareRNG
<img width="665" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/7d85f3e1-95a0-44b0-8b08-a9bb67c057a1">

- [attachment](https://storage.googleapis.com/zer0ptsctf2023/aed5259d-bf93-4969-aa9a-d38524abf513/squarerng_1873b2fd7e7bb265e0f28924353ff2ad.tar.gz)
> server.py
```python
#!/usr/bin/env python3
import os
from Crypto.Util.number import getPrime, getRandomRange

def isSquare(a, p):
    return pow(a, (p-1)//2, p) != p-1

class SquareRNG(object):
    def __init__(self, p, sa, sb):
        assert sa != 0 and sb != 0
        (self.p, self.sa, self.sb) = (p, sa, sb)
        self.x = 0

    def int(self, nbits):
        v, s = 0, 1
        for _ in range(nbits):
            self.x = (self.x + 1) % p
            s += pow(self.sa, self.x, self.p) * pow(self.sb, self.x, self.p)
            s %= self.p
            v = (v << 1) | int(isSquare(s, self.p))
        return v

    def bool(self):
        self.x = (self.x + 1) % self.p
        t = (pow(self.sa, self.x, self.p) + pow(self.sb, self.x, self.p))
        t %= self.p
        return isSquare(t, self.p)

p = getPrime(256)

sb1 = int(input("Bob's seed 1: ")) % p
sb2 = int(input("Bob's seed 2: ")) % p
for _ in range(77):
    sa = getRandomRange(1, p)
    r1 = SquareRNG(p, sa, sb1)
    print("Random 1:", hex(r1.int(32)))
    r2 = SquareRNG(p, sa, sb2)
    print("Random 2:", hex(r2.int(32)))

    guess = int(input("Guess next bool [0 or 1]: "))
    if guess == int(r1.bool()):
        print("OK!")
    else:
        print("NG...")
        break
else:
    print("Congratz!")
    print(os.getenv("FLAG", "nek0pts{*** REDACTED ***}"))

```
- Tóm tắt đoạn code: 
    - Server yêu cầu ta nhập 2 số sb1 và sb2, sau đó random một số sa trong khoảng từ 1 đến p (là một số nguyên tố ngẫu nhiên). Tiếp theo server cho ta 2 số random1 và random2, nếu ta convert nó ra một số 32 bit thì bit thứ i của random1 là giá trị của hàm `isSquare` của $1 + sa.sb1 + sa^2.sb1^2 + ... + sa^i.sb1^i$, tương tự đối đối với random2 (thực ra bản chất hàm isSquare là hàm check xem 1 số có là quadratic residue mod p hay không).
    - Sau đó server bắt chúng ta đoán giá trị của hàm isSquare của giá trị $sa^{33} + sb1^{33}$(*)
    - Ta cần đoán đúng 77 lần liên tiếp để nhận được flag 😥
- Thoạt nhìn thì mình thấy biểu thức $sa^{33} + sb1^{33}$ chẳng có gì liên quan đến các tổng $1 + sa.sb1 + sa^2.sb1^2 + ... + sa^i.sb1^i$ cả. Tuy nhiên nên nhớ rằng mình có thể chọn số sb1 và sb2. Để đơn giản nhất thì mình chọn 2 số là 1 và -1. Thay vào (*) ta được $sa^{33} + 1$, mình thử phân tích thừa số nó ra thì được $sa^{33}+1 = (sa+1)(sa^{32}-sa^{31}+...-sa+1)$.Tới đây để ý một tí thì mình sẽ thấy sa+1 chính là bit đầu của random1, cục dài dài phía sau là bit cuối của random2. Vậy ta chỉ cần "nhân lại" là có được kết quả.
> Tại sao mình nói "nhân lại", vì trong hàm isSquare(a,p) thì họ check điểu kiện `pow(a, (p-1)//2, p) != p-1`, thực ra vế trái chính là giá trị của [Legendre symbol](https://en.wikipedia.org/wiki/Legendre_symbol) (những ai có làm các challenge đầu mục Mathematics trên Cryptohack thì chắc chắn biết :)) ). Nó chỉ nhận 3 giá trị là 1,-1,0 (chỉ xảy ra khi a là bội của p và nó chắc chắn không thể xảy ra). Nếu gọi `L(a) = pow(a, (p-1)//2, p))` thì ta có `L(ab) = L(a).L(b)` và do đó L(ab) = 1 (tức hàm isSquare ra kết quả True) khi và chỉ khi L(a) = L(b) = 1 hoặc L(a) = L(b) = -1
- Ý tưởng có rồi, bây giờ chỉ cần viết script để tự động hóa mọi thứ.
> solve.py
```python
from pwn import *

r = remote('crypto.2023.zer0pts.com', 10666)
def isSquare(a, p):
    return pow(a, (p-1)//2, p) != p-1


def get_para():
	data = r.recvuntil(b'1:')
	random1 = bin(int(r.recvuntil(b'\n').decode().strip()[2:], 16))[2:]
	data = r.recvuntil(b'2:')
	random2 = bin(int(r.recvuntil(b'\n').decode().strip()[2:], 16))[2:]
	while len(random1) < 32:
		random1 = '0' + random1
	while len(random2) < 32:
		random2 = '0' + random2
	return random1, random2

def guess(random1, random2):
	print(random1)
	print(random2)
	if random1[0] == '1':
		r1 = 1
	else:
		r1 = -1
	if random2[-1] == '1':
		r2 = 1
	else:
		r2 = -1
	print(r1,r2)
	if r1*r2 == 1:
		ans = 1
	else: 
		ans = 0
	data = r.recvuntil(b']: ')
	r.sendline(str(ans).encode())
	mess = r.recvline()
	print(mess)

data = r.recvuntil(b'seed 1: ')
r.send(b'1\n')
data = r.recvuntil(b'seed 2: ')
r.send(b'-1\n')
for i in range(77):
	random1, random2 = get_para()
	# print(random1)
	# print(random2)
	guess(random1, random2)
flag = r.recv(2024)
print(flag)
r.close()
```
![](https://github.com/tvdat20004/CTF_write-up/blob/main/zer0ptsCTF/squarerng/Screenshot%202023-07-15%20164438.png)
> https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/r1J55fG9h
