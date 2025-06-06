# M side
- Source code đề bài:
``` python
from Crypto.Util.number import getStrongPrime, bytes_to_long as b2l, isPrime
import os


FLAG = os.getenv('FLAG', 'FLAG{hue_hue_hue}').encode()
p = getStrongPrime(512)
q = getStrongPrime(512)
while not isPrime(4 * p * p + q * q):
    p = getStrongPrime(512)
    q = getStrongPrime(512)

hint = 4 * p * p + q * q
e = 65537
print(f"hint: {hint}")
# n for wat?
print(f"ct: {pow(b2l(FLAG), e, p * q)}")

"""
hint: 461200758828450131454210143800752390120604788702850446626677508860195202567872951525840356360652411410325507978408159551511745286515952077623277648013847300682326320491554673107482337297490624180111664616997179295920679292302740410414234460216609334491960689077587284658443529175658488037725444342064697588997
ct: 8300471686897645926578017317669008715657023063758326776858584536715934138214945634323122846623068419230274473129224549308720801900902282047728570866212721492776095667521172972075671434379851908665193507551179353494082306227364627107561955072596424518466905164461036060360232934285662592773679335020824318918
"""
```
- Nhìn vào code, ta thấy đề bài không cho `n = p*q` như các bài RSA thường thấy, thay vào đó lại cho giá trị `hint = 4*p*p + q*q`. Mặt khác, giá trị hint là số nguyên tố nên ta sẽ liên tưởng đến "Định lý Fermat về tổng của hai số chính phương", định lý này phát biểu:
"Một số nguyên tố biểu diễn được dưới dạng tổng 2 số chính phương khi và chỉ khi số nguyên tố đó đồng dư với 1 modulo 4".
- Có một thuật toán khá hiệu quả để biểu diễn số nguyên tố dạng p = 4k+1 thành tổng 2 số chính phương, chi tiết như sau: Tìm số x thỏa mãn $x^2 \equiv -1\text{ (mod n)}$. Ta làm được việc đó bằng cách tìm một [Quadratic non-residue](https://en.wikipedia.org/wiki/Quadratic_residue) theo modulo p (a là một Quadratic non-residue mod p khi và chỉ khi $a^{\frac{p-1}{2}} \equiv -1 \text{ (mod p)}$), gọi là q, khi đó $x = a^{\frac{p-1}{4}}\text{ (mod p)}$. Áp dụng thuật toán Euclid để tìm UCLN của 2 số với 2 số p và x. Lấy 2 số dư đầu tiên mà nhỏ hơn căn bậc 2 của p, gọi là a và b. Khi đó $a^2 + b^2 = p$
- Trở lại bài toán, sau khi áp dụng thuật toán tên, ta tìm được 2 số, khi đó số chẵn chính là 2p, số lẻ chình là q. Có p và q, công việc còn lại trở nên rất nhẹ nhàng phải không nào ^^
- Sau đây là source code giải mã:
``` python
import gmpy2
from Crypto.Util.number import long_to_bytes

hint = 461200758828450131454210143800752390120604788702850446626677508860195202567872951525840356360652411410325507978408159551511745286515952077623277648013847300682326320491554673107482337297490624180111664616997179295920679292302740410414234460216609334491960689077587284658443529175658488037725444342064697588997
ct = 8300471686897645926578017317669008715657023063758326776858584536715934138214945634323122846623068419230274473129224549308720801900902282047728570866212721492776095667521172972075671434379851908665193507551179353494082306227364627107561955072596424518466905164461036060360232934285662592773679335020824318918
t = hint
# find Quadratic non-residue 
def check(a,p):
	if pow(a,(p-1)//2,p) == p-1:
		return True

for i in range(hint):
	if check(i,hint) == True:
		x = i
		break
x = pow(x,(hint-1)//4,hint)
# assert pow(x,2,hint) == hint - 1
c = gmpy2.iroot(hint,2)[0]

while hint > c or x > c:
	hint,x = max(x, hint % x) , min(x,hint % x)
p = hint // 2
q = x
n = p * q
phi = (p-1)*(q-1)
print(long_to_bytes(pow(ct,pow(65537,-1,phi),n)))
```
Kết quả: 

<img width="598" alt="Screenshot 2023-05-09 002419" src="https://user-images.githubusercontent.com/117071011/236989031-b5e8deca-1375-4fe6-aee4-daf544b51152.png">
> https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/Sk9fz2LE3
