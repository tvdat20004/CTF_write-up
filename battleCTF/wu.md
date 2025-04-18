# Back to origin
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/f3b7d324-762e-4b84-a262-40079a5b7f47)

- Attachment: [Metaphysics.png](https://s1.fdow.nl/iHirl-Metaphysics.png)
 ![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/4dc23134-0573-439c-b9ec-53cefb1b4d7e)
- Đây là chữ tượng hình Ai Cập cổ đại, so tại [đây](https://bsmekhampha.com/2021/12/01/bang-chu-cai-chu-tuong-hinh-ai-cap-co-dai/).
# Blind
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/23c863da-bc58-450a-a1ef-2d1aeda6ef6a)

Attachment: [Chall_blind.txt](https://s1.fdow.nl/s2xI1-Chall_blind.txt)
- [CyberChef](https://gchq.github.io/CyberChef/): From Base 85 -> From Braille

![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/b646f236-82f3-49eb-8fa9-d12cad3c91b9)

# Rocyou
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/12a3e936-aa7c-4751-8a70-5b92cf899df2)

- Attachment: [rocyou.py](https://prequal.battlectf.online/files/fd548d9b49f15b22a0af02be2327b74b/rocyou.py)
- Rocyou.py
``` python
from Crypto.Util.number import bytes_to_long


FLAG = bytes_to_long('dsdf')

n = 14558732569295568217680262946946350946269492093750369718350618000766298342508431492935822827678025952146979183716519987777790434353113812051439651306232101
e = 65537

c = pow(FLAG, e, n)

print(f"c = {c}")

# c = 10924637845512114669339598787759482373871484619074241479073765261738618851409833137908272858354441670603598700617114497065118363300675413269144392865493504
```
- Thoạt nhìn thì mình thấy đây là một bài RSA khá đơn giản, tuy nhiên vì nó quá đơn giản nên nó đã làm khó mình lúc đầu. Sau một hồi tìm kiếm thì thấy được đây là một CVE-2017, chi tiết mình để ở [đây](https://crocs.fi.muni.cz/public/papers/rsa_ccs17), mình sẽ sử dụng tool từ [đây](https://gitlab.com/parfaittolefo23/astuces-et-write-up-ctf/-/blob/main/Tools/neca).
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/e9d75a0c-d587-4380-bcd5-ce21fc5233cd)

- Có p,q rồi thì ... Done :v 
- solve.py
``` py

n = 14558732569295568217680262946946350946269492093750369718350618000766298342508431492935822827678025952146979183716519987777790434353113812051439651306232101
e = 65537
c = 10924637845512114669339598787759482373871484619074241479073765261738618851409833137908272858354441670603598700617114497065118363300675413269144392865493504
from Crypto.Util.number import long_to_bytes
p = 127801155916875524149457561567678575565270601000365665873572024750823913157383 
q = 113917064871970833547038329106470040388258358281464605006613652518914797349747
print(long_to_bytes(pow(c,pow(e,-1,(p-1)*(q-1)),n)))
# b'battleCTF{ROCA_shork_me_0x0x0x}\n'
```
- Flag: `battleCTF{ROCA_shork_me_0x0x0x}`
# Gooss
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/704fdfe7-0c82-428f-8104-8d8cbca6758b)

- Attachment: [gooss.py](https://prequal.battlectf.online/files/03eb3f54c197cfdd7343ea3c217c3351/gooss.py)
- gooss.py
``` py
import random
flag = 'battleCTF{******}'
a = random.randint(4,9999999999)
b = random.randint(4,9999999999)
c = random.randint(4,9999999999)
d = random.randint(4,9999999999)
e = random.randint(4,9999999999)

enc = []
for x in flag:
    res = (2*a*pow(ord(x),4)+b*pow(ord(x),3)+c*pow(ord(x),2)+d*ord(x)+e)
    enc.append(res)
print(enc)

#Output: [1245115057305148164, 1195140205147730541, 2441940832124642988, 2441940832124642988, 1835524676869638124, 1404473868033353193, 272777109172255911, 672752034376118188, 324890781330979572, 3086023531811583439, 475309634185807521, 1195140205147730541, 2441940832124642988, 1578661367846445708, 2358921859155462327, 1099718459319293547, 773945458916291731, 78288818574073053, 2441940832124642988, 1578661367846445708, 1099718459319293547, 343816904985468003, 1195140205147730541, 2527132076695959961, 2358921859155462327, 2358921859155462327, 1099718459319293547, 72109063929756364, 2796116718132693772, 72109063929756364, 2796116718132693772, 72109063929756364, 2796116718132693772, 3291439457645322417]
```
- Ở đây để đơn giản là họ random 5 số a,b,c,d,e để tạo đa thức $f(x) =2ax^4 + bx^3 + c^2 + dx + e$, output chính là các `f(ord(x))` với x là các ký tự trong flag. 
- Đầu tiên, ta cần tìm giá trị a,b,c,d,e. Để ý rằng flag có format là battleCTF{...}, tức là mình đã biết được ít nhất 5 ký tự khác nhau trong flag, vậy là đủ để lập thành một hệ tuyến tính 5 ẩn a,b,c,d,e. Sau khi tìm được a,b,c,d,e mình sẽ tìm từng ký tự thứ i bằng cách giải phương trình `f(x) = output[i]`để tìm x. Việc giải phương trình và hệ phương trình thì SageMath hỗ trợ rất tốt.
- Solve.sage
``` python    
Output = [1245115057305148164, 1195140205147730541, 2441940832124642988, 2441940832124642988, 1835524676869638124, 1404473868033353193, 272777109172255911, 672752034376118188, 324890781330979572, 3086023531811583439, 475309634185807521, 1195140205147730541, 2441940832124642988, 1578661367846445708, 2358921859155462327, 1099718459319293547, 773945458916291731, 78288818574073053, 2441940832124642988, 1578661367846445708, 1099718459319293547, 343816904985468003, 1195140205147730541, 2527132076695959961, 2358921859155462327, 2358921859155462327, 1099718459319293547, 72109063929756364, 2796116718132693772, 72109063929756364, 2796116718132693772, 72109063929756364, 2796116718132693772, 3291439457645322417]

#f(x) = 2ax^4 + bx^3 + cx^2 + dx + e

coef = []

for x in "batle":
	coef.append([2*ord(x)^4, ord(x)^3, ord(x)^2, ord(x), 1])

coef = Matrix(coef)
res = vector([Output[0], Output[1],Output[2],Output[4],Output[5]])
flag = ''
(a,b,c,d,e) = coef \ res
x = var('x')
fx = 2*a*x^4 + b*x^3 + c*x^2 + d*x + e
for o in Output:
	root = solve(fx == o, x)
	# print(root)
	for r in root:
		try: 
			r = int(r.rhs())
		except:
			continue
		# print(r)
		flag += chr(abs(r))
		break
print(flag)
# battleCTF{Maths_W1th_Gauss_0x0x0x}
- Flag:`battleCTF{Maths_W1th_Gauss_0x0x0x}`
```
> https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/SJ139e1th
