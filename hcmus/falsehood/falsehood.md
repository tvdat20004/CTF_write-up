# Faslehood
- Source code đề bài:
``` python
import os
import numpy as np
from sage.all import ComplexField, PolynomialRing
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
from binascii import hexlify

FLAG = os.getenv('FLAG', "FLAG{this is a real flag}")
bits = 1111
C = ComplexField(bits)
P = PolynomialRing(C, names='x')
(x,) = P.gens()

key_array = np.random.choice(256, size=(16,))
key = b''.join([int(i).to_bytes(1, 'big') for i in key_array])

f = sum([coeff * x**i for i, coeff in enumerate(key_array)])
hint = []
for _ in range(16):
    X = random.randint(10**8, 10**10)
    Y = int(abs(f(X)))
    while [X, Y] in hint:
        X = random.randint(10**8, 10**10)
        Y = int(abs(f(X)))
    hint.append([X, Y])


cip = AES.new(key, AES.MODE_CBC)
ct = cip.encrypt(pad(FLAG.encode(),16))
iv = cip.iv
with open('output.txt', 'w') as file:
    file.write(str(hint)+'\n')
    print(f"ct = {hexlify(ct).decode()}, iv = {hexlify(iv).decode()}", file=file)
```
- [output.txt](https://github.com/tvdat20004/CTF_write-up/blob/main/hcmus/falsehood/output.txt)
- Nhìn vào đoạn code, ta thấy FLAG được mã hóa bằng AES, trong đó ta đã biết iv, nên giờ chỉ cần tìm key là bài toán được giải quyết.
- key được tạo bằng cách tạo ra bằng cách chọn random các số từ 0 tới 255, chuyển mỗi số sang ký tự byte tương ứng để thu được chuỗi bytes chính là key. Chúng ta có một đa thức $f = a[0] + a[1].x + a[2].x^2 + ...+a[15].x^{15}$ với a là các giá trị trong key_array. Ta thấy hint chính là list của 16 cặp giá trị [X,f(X)], do đó công việc chúng ta chỉ là giải hệ phương trình tuyến tính 16 ẩn :v
- Source code giải mã:
``` python
from sage.all import *
hint = [[8833677163, 7159466859734884050485160017085648949938620549936739498951806707835448713685207536552299918328868591349533273061478374089984223260577742322460362334647], 
[1762352339, 226021067407224282748442153993506422184559341973942542463611713009302649608941949660293486972516731321467369225717344439888178648461773300463], 
[6814325828, 145915445591160853098610646953738314537732696913127480076359637783667652244881400087606152610739138506056218199806589240306741950875956525839170443027], 
[7865890147, 1255960511416167089973436987379886082394930531153251392262351559661203914293720867397614316726175343133363293139291718249474745356688772183204229822751],
[3446680058, 5293859406843167459297872689128502546567761548640003856519557803475599388573073027426285178678302790672452768542207529392596772806973985884693237], 
[5877771652, 15883583178415793156782570756223737797760371065858523945056072346852806064052610100332389954372845836435762293469821829936427366159434784004504398291], 
[5589586633, 7472281200056449019563455444999813482028446397663996508394508567670602924631065370355170602075256758870709465268255309886778027432655593535614166637], 
[1175276268, 518629639886914674796931012497083502361229856009622285824810204881645367508380387007577326543311405957619591605841895258801496781885398507], 
[3312651249, 2920072124198357353277671402963439479294095254775553378538026906919501392975483266953780010186413153114694525677661955925502702904273824951901573], 
[1690420045, 120969905638890571692249167310237577968012605711450331530578304692989016303379573026678222839813088165787719888874515256743894818676147474521], 
[8298141391, 2802013920829536770649820952830225273137583982204944734413323800249577243089166668778583649665043009034143120874987986020037964205143133245123290632883], 
[733386150, 439287044309927586596972381366960178061704411347096135895831191742005839221734048948610767236121358802659929070752762370822244956535801], 
[7897145685, 1332938401210287323326359805632057169759318295533885927320250339098837407040892547133970478663396358868892779722453565866390506758764909670000617998161], 
[9797888335, 33864534898740204255025855638155912349784294672865719351405048784504660475905319925895086755774471151890089727930776090169445401259844048317273142069811], 
[4557234547, 349364318043137479854576449493426376983315472777226775365310579193760250715517761090058069937282741206013319707277840448237966901906357292702335951], 
[7667001731, 855344863189641492213600127143839128290386097202448105626863527763958015786114563445357087338205788545215994676722500375202243293047596358065835329663]]
kq = []
heso = []
for x in hint:
	heso.append([x[0]^i for i in range(16)])
	kq.append(x[1])

A = Matrix(heso)
b = vector(kq)
key_array = A \ b
key = b''.join([int(i).to_bytes(1, 'big') for i in key_array])
from Crypto.Cipher import AES
import binascii
ct = "be205fd34ebe59af55ea11fec9aea50197fbf35d5b52c650a6c9563186625e8b6021ba31db538fa4b60c69a42c96ee3bebaba53ac9afa9c3c185d4d0b145bc8251d892c243f1aa4037aeea003714e24c"
iv = "370abc6fce33f812de7b88daaa82e4c4"

ct = binascii.unhexlify(ct)
iv = binascii.unhexlify(iv)

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)

print(pt)
```
Kết quả: 
![](https://github.com/tvdat20004/CTF_write-up/blob/main/hcmus/falsehood/ans.png)
HCMUS-CTF{just_because_you're_correct_doesn't_mean_you're_right}