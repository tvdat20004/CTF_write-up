# Hack.lu CTF 2023 
> Vì thời gian diễn ra giải này và giải Duy Tân diễn ra hầu hết là trùng nhau nên sau khi ~~bị đề Duy Tân giã tan nát~~ giải Duy Tân kết thúc thì team mình chỉ có vài tiếng còn lại để làm. Tuy nhiên team mình cũng kịp làm được 2 câu và mình đóng góp được 1 câu crypto ~~siêu dễ~~ 😁. Sau đây là chi tiết write-up của mình cho câu đó. 
## Lucky number
![](https://hackmd.io/_uploads/BkgLw0sba.png)

- Source:
```python
#!/usr/bin/env python
#hacklu23 Baby Crypyo Challenge
import math
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os                                                   
    
def add(e): return e+(length-len(e)%length)*chr(length-len(e)%length)
def remove(e): return e[0:-ord(e[-1:])]
length=16 

def main():  
    flag= os.environ["FLAG"]
    print("Starting Challenge")
 
    key=get_random_bytes(32)
    message=add(flag)
    iv = get_random_bytes(length)
    cipher = AES.new(key,AES.MODE_CBC,iv) 
    cipher_bytes = base64.b64encode(iv+cipher.encrypt(message.encode("utf8")))
    print(cipher_bytes.decode())

    for l in range(0,5):
        A=[]
        print("You know the moment when you have this special number that gives you luck? Great cause I forgot mine")
        data2=input()
        print("I also had a second lucky number, but for some reason I don't remember it either :(")
        data3=input()
        v=data2.strip()
        w=data3.strip()
        if not v.isnumeric() or not w.isnumeric():
            print("You sure both of these are numbers?")
            continue
        s=int(data2)
        t=int(data3)
        if s<random.randrange(10000,20000):
            print("I have the feeling the first number might be too small")
            continue
        if s>random.randrange(150000000000,200000000000):
            print("I have the feeling the first number might be too big")
            continue
        if t>42:
            print("I have the feeling the second number might be too big")
            continue

        n=2**t-1
        sent=False
        for i in range(2,int(n**0.5)+1):
             if (n%i) == 0:
                print("The second number didn't bring me any luck...")
                sent = True
                break
        if sent:
            continue
        u=t-1
        number=(2**u)*(2**(t)-1)
        sqrt_num=math.isqrt(s)
        for i in range(1,sqrt_num+1):
            if s%i==0:
                A.append(i)
                if i != s//i and s//i != s:
                    A.append(s//i)      
        total=sum(A)
        if total==s==number:
            decoded=base64.b64decode(cipher_bytes)
            cipher=AES.new(key,AES.MODE_CBC,iv)
            decoded_bytes=remove(cipher.decrypt(decoded[length:]))
            print("You found them, well done! Here have something for your efforts: ")
            print(decoded_bytes.decode())
            exit()
        else:
            print("Hm sadge, those don't seem to be my lucky numbers...😞")
    
    print("Math is such a cool concept, let's see if you can use it a little more...")
    exit()
  
if __name__ == "__main__":
    main()
```
- Source bài này khá lan man, đơn giải bài này chỉ yêu cầu chúng ta nhập 2 số s và thỏa mãn các điều kiện sau:
    - $t<=42$ (1)
    - `20000 < s = (2**(t-1))*(2**(t)-1) < 150000000000`(2)
    - `2**t-1` là số nguyên tố (số nguyên tố dạng này còn có tên gọi là [mersenne prime](https://vi.wikipedia.org/wiki/S%E1%BB%91_nguy%C3%AAn_t%E1%BB%91_Mersenne)(3)
    - $s = 2^{t-1}.(2^t -1)$ là số hoàn hảo (4)
- Nghe điều kiện (4) có vẻ khá khoai 😥, tuy nhiên khi mình đọc về số hoàn hảo trên wiki thì mình phát hiện:
![](https://hackmd.io/_uploads/S12jnCi-T.png)
- Ồ, vậy ngon rồi :D, vậy ta chỉ cần tìm số t thỏa 3 điều kiện (1),(2),(3) (do t <= 42 nên chỉ cần brute-force), sau đó tính $s = 2^{t-1}.(2^t -1)$ rồi gởi lên server thôi :v 
- Solve.py
```python
from pwn import *
import base64
from Crypto.Util.number import isPrime
r = remote("flu.xxx", 10010)

for i in range(42):
	if isPrime(2**i - 1):
		t = i
		s = (2**(t-1))*(2**(t)-1)
		if 20000 < s < 150000000000:
			break

r.sendlineafter(b'You know the moment when you have this special number that gives you luck? Great cause I forgot mine\n', str(s).encode())
r.sendlineafter(b"I also had a second lucky number, but for some reason I don't remember it either :(\n", str(t).encode())

r.interactive()
```
![](https://hackmd.io/_uploads/rkKapCib6.png)
> Flag: flag{luck_0n_fr1d4y_th3_13th?}
