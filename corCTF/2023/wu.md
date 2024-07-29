# fizzbuzz100
<img width="611" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/4652eef6-0f23-442a-8ca0-54989c0ad057">

- [Attachment](https://static.cor.team/uploads/e23d864efe7fa74f8c5a309f8c8b380e520242cdc62b817b10534dae40516d23/fizzbuzz100.py)
- fizzbuzz100.py
```python
#!/usr/local/bin/python
from Crypto.Util.number import *
from os import urandom

flag = open("flag.txt", "rb").read()
flag = bytes_to_long(urandom(16) + flag + urandom(16))

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{ct = }")

while True:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    if not out:
        out = pt
    print(out)

```
- Đây là một bài liên quan đến hệ mã RSA, cụ thể là server sẽ decrypt bất cứ giá trị ct nào mà chúng ta gởi và gởi lại cho mình giá trị plaintext nếu nó không chia hết cho 3 và 5.
- Ở đây mình chỉ cần gởi `ct * 2**e % n` , khi đó giá trị mình nhận lại sẽ là `2*flag`. Từ đó dễ dàng tìm được flag.
- solve.py
```python
from pwn import *
from Crypto.Util.number import long_to_bytes

while True:
	r = remote("be.ax", 31100)
	
	data = r.recvuntil(b'n = ')
	n = int(r.recvline().decode().strip())
	data = r.recvuntil(b'ct = ')
	ct = int(r.recvline().decode().strip())
	e = 65537
	print(n)
	print(ct)
	send = ct * pow(2,e,n) % n
	data = r.recvuntil(b'> ')
	r.sendline(str(send).encode())
	# x = r.recvline()
	try:
		flag = int(r.recvline().decode().strip())
		print(long_to_bytes(flag//2))
		r.close()
		break
	except:
		r.close()
```
![image](https://github.com/tvdat20004/CTF_write-up/assets/117071011/b47190da-cf2d-4acb-885d-de6a6660960a)
> Flag: corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}
# eyes
<img width="600" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/20348d1d-e31f-4dbf-989f-cf85f70928e5">

- [main.sage](https://static.cor.team/uploads/53b043b3956ab33fbf528e4155f67258164bd06125ded61c675c206ce5355ea7/main.sage), [out.txt](https://static.cor.team/uploads/961ccc36f25a5c09984361183d3b45b3415db5e78596f7a218366d95137eb65b/out.txt)
- main.sage
```python
from Crypto.Util.number import bytes_to_long, getPrime

# my NEW and IMPROVED secret sharing scheme!! (now with multivariate quadratics)

with open('flag.txt', 'rb') as f:
    flag = f.read()

s = bytes_to_long(flag)
p = getPrime(len(bin(s)))
print(p)
F = GF(p)
N = 1024

conv = lambda n: matrix(F, N, 1, [int(i) for i in list(bin(n)[2:][::-1].ljust(N, '0'))])

A = random_matrix(F, N, N)

for i in range(0, N):
    for j in range(0, i):
        A[i, j] = 0
B = random_matrix(F, N, 1)
C = matrix(F, [F(s)])

fn = lambda x: (x.T * A * x + B.T * x + C)[0][0]

L = []
for i in range(7):
    L.append(fn(conv(i + 1)))

print(L)
```
- Bài này không khác gì bài kiểm tra đại số tuyến tính gì mấy :)), bài này chỉ yêu cầu ta biết nhân ma trận là đủ. Vì quá trình biến đồi khá dài nên mình hơi lười trình bày ở đây 🥲, kết quả của quá trình tính toán trên mình đã thể hiện trong code solution. 
- solve.py
```python
# from sage.all import *
p = 1873089703968291141600166892623234932796169766648225659075834963115683566265697596115468506218441065194050127470898727249982614285036691594726454694776985338487833409983284911305295748861807972501521427415609

l = [0, 676465814304447223312460173335785175339355609820794166139539526721603814168727462048669021831468838980965201045011875121145342768742089543742283566458551844396184709048082643767027680757582782665648386615861, 1472349801957960100239689272370938102886275962984822725248081998254467608384820156734807260120564701715826694945455282899948399224421878450502219353392390325275413701941852603483746312758400819570786735148132, 202899433056324646894243296394578497549806047448163960638380135868871336000334692955799247243847240605199996942959637958157086977051654225700427599193002536157848015527462060033852150223217790081847181896018, 1065982806799890615990995824412253076607488063240855100580513221962298598002468338823225586171107539104635808108356492123167315175110515086192932230998426512947581115358738651206273178867911944034690138825583, 1676559204037482856674710667663849447914859348633288513196735253002541076530170853584406282605482862202276451646974549657672382936948091649764874334064431407644457518190694888175499630744741620199798070517691, 13296702617103868305327606065418801283865859601297413732594674163308176836719888973529318346255955107009306239107173490429718438658382402463122134690438425351000654335078321056270428073071958155536800755626, 1049859675181292817835885218912868452922769382959555558223657616187915018968273717037070599055754118224873924325840103339766227919051395742409319557746066672267640510787473574362058147262440814677327567134194]

tmp1 = l[1] + l[4] - l[5] # C - A02
tmp2 = l[3] + l[4] - l[7] # C -A12 - A02
tmp3 = l[2] + l[4] - l[6] # C - A12
A12 = tmp1 - tmp2 
C = A12 + tmp3
from Crypto.Util.number import *
print(long_to_bytes(C % p))
# b'corctf{mind your ones and zeroes because zero squared is zero and one squared is one}\n'
```
> flag: corctf{mind your ones and zeroes because zero squared is zero and one squared is one}
# cbc
<img width="608" alt="image" src="https://github.com/tvdat20004/CTF_write-up/assets/117071011/bd6c29be-45b2-4dfe-b76a-0f3e84226f54">

- [cbc.py](https://static.cor.team/uploads/b34e0f3a8f593c51dc28844decc71e2a37a3e6316aa763853aed394d4602e17c/cbc.py), [cbc_output.txt](https://static.cor.team/uploads/5e93945f70c7b38bb7fca87cf7be309d0f7fd3ea7899b52c152b8094b714290b/cbc_output.txt)
- cbc.py
```python
import random

def random_alphastring(size):
    return "".join(random.choices(alphabet, k=size))

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])

def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i+klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext
    
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

message = open("message.txt").read().upper()
message = "".join([char for char in message if char in alphabet])
flag = open("flag.txt").read()
flag = flag.lstrip("corctf{").rstrip("}")
message += flag
assert all([char in alphabet for char in message])

key = random_alphastring(bs)
iv, ct = cbc(key, pad(bs, message))
print(f"{iv = }")
print(f"{ct = }")
```
- Đây là dạng mã hóa khối theo mode [cbc](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation). Sơ đồ mã hóa có dạng như sau:
![](https://hackmd.io/_uploads/ByntLULi3.png)
Nhưng ở bài này, phép xor và hàm mã hóa trong sơ đồ thì được thay thế bằng phép `add_key`. Hàm add_key nhận vào 2 chuỗi key và block, khi đó block[i] sẽ được dịch (như trong Caesar cipher) với giá trị shift bằng chỉ số của key[i] trong alphabet.
- Đầu tiên mình sẽ viết 1 hàm ngược lại với `add_key`, đặt là `cut_key` :v
```python
def cut_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])
```
![](https://hackmd.io/_uploads/BJ-LMDLj3.png)

- Ở trên là sơ đồ decrypt CBC mode, vì chưa biết giá trị key nên mình chỉ `cut_key` từng block ciphertext cho iv (lưu ý phải cập nhật iv bằng block ciphertext trước đó). Chuối plaintext thu được ta đưa vào https://www.guballa.de/vigenere-solver để tìm ra đoạn mess cần tìm. 
```python

def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])
def cut_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])

def decrypt(key, ct):
    block = [cut_key(key, ct[i:i+16]) for i in range(0, len(ct), 16)]
    return "".join(block)
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
iv = 'RLNZXWHLULXRLTNP'
ct = 'ZQTJIHLVWMPBYIFRQBUBUESOOVCJHXXLXDKPBQCUXWGJDHJPQTHXFQIQMBXNVOIPJBRHJQOMBMNJSYCRAHQBPBSMMJWJKTPRAUYZVZTHKTPUAPGAIJPMZZZDZYGDTKFLWAQTSKASXNDRRQQDJVBREUXFULWGNSIINOYULFXLDNMGWWVSCEIORQESVPFNMWZKPIYMYVFHTSRDJWQBTWHCURSBPUKKPWIGXERMPXCHSZKYMFLPIAHKTXOROOJHUCSGINWYEILFIZUSNRVRBHVCJPVPSEGUSYOAMXKSUKSWSOJTYYCMEHEUNPJAYXXJWESEWNSCXBPCCIZNGOVFRTGKYHVSZYFNRDOVPNWEDDJYITHJUBVMWDNNNZCLIPOSFLNDDWYXMYVCEOHZSNDUXPIBKUJIJEYOETXWOJNFQAHQOVTRRXDCGHSYNDYMYWVGKCCYOBDTZZEQQEFGSPJJIAAWVDXFGPJKQJCZMTPMFZDVRMEGMPUEMOUVGJXXBRFCCCRVTUXYTTORMSQBLZUEHLYRNJAAIVCRFSHLLPOANFKGRWBYVSOBLCTDAUDVMMHYSYCDZTBXTDARWRTAFTCVSDRVEENLHOHWBOPYLMSDVOZRLENWEKGAWWCNLOKMKFWWAZJJPFDSVUJFCODFYIMZNZTMAFJHNLNMRMLQRTJJXJCLMQZMOFOGFPXBUTOBXUCWMORVUIIXELTVIYBLPEKKOXYUBNQONZLPMGWMGRZXNNJBUWBEFNVXUIAEGYKQSLYSDTGWODRMDBHKCJVWBNJFTNHEWGOZFEZMTRBLHCMHIFLDLORMVMOOHGXJQIIYHZFMROGUUOMXBTFMKERCTYXFIHVNFWWIUFTGLCKPJRFDRWDXIKLJJLNTWNQIOFWSIUQXMFFVIIUCDEDFEJNLKLQBALRKEYWSHESUJJXSHYWNRNPXCFUEFRJKSIGXHFTKNJXSYVITDOGYIKGJIOOHUFILWYRBTCQPRPNOKFKROTFZNOCZXZEYUNWJZDPJDGIZLWBBDGZJNRQRPFFGOTGFBACCRKLAPFLOGVYFXVIIJMBBMXWJGLPOQQHMNBCINRGZRBVSMLKOAFGYRUDOPCCULRBE'
blocks = [ct[i:i+16] for i in range(0,len(ct),16)]
prev_block = iv
pt = ""
for b in blocks:
    pt += cut_key(prev_block, b)
    prev_block = b
print(pt)
```

```
pt:IFGKLLEKCBSKNPSCRLBSMXHTSJNIJPSUHCQOHMKGJBEAWKMETQXIEAGWPFRESHZATIKKEAGWPLQWXKUCRGZUGLEALXJASVNAANIYGYBVYKTLQWRJIPRNEAGWPFRJTVZLORBHTLBPYPXOYGLSNVLYMKXNXYTPWCSFETXDHLAGJCQAJENKPQKUGLHHSCTHQAESNEQYHFBPYDMQXARREOJQWWNUWCTHGASFEIKKVGKGDFAOXJDJLWQYEAMKWPZJIXHRANPOLLXOULLLTPDLTUZEFHKKKFMCFHTJLQPQLVXHAKDZGAOMSKUCTFREGJOQYGQSSGOIKMGCELCEKKDBVGOIBGGQXQGALPTQYUQUFWOGJVCWDYHRHQRJKWTNAWHJLKSRHTLKZZTRWZTHNCQRUTKEYWOGFQRPMGUCRUFEGGYIFRVDNEGGSYFTXDRWKBCPTFZWIULVMWGESIKAINHLUZXDWETPQLEEYUTQETPQKWGQLXVWWGSFAVFJBKUCKFBWQNXRHGDDNKRULBLZJXDJORBTUQMJWDMQUTNHEEQJAWKGJBZHQAHQANFDNPTPVQGAXGOCORIUTJXWKFMCNVASTKQYLBNULXOWWVNDTJBIRKMGEQGADWRCLKKKQALVZBJAWPDJTJBFKGZTSJHJYJDQYUQUFLACLXKHTEZREUQXXETEZFMAXTDQOWOSXKMQLEDKYJDPPTLWKSFULEZPDQTPUPQXXCXTFBKEXCMCSUBDMATNHXQPTHZLORBHTLBPYPXOYGLZUVRIXDXUKYXEYUDJFKQSTFHPDVEQSESGOPFDMZXEGKSACVNDAELCIDXVWLOAWCSGNIPOLLXODFMQCKRLOTJQEDRWKBCESENKBKKQMAHPOFSDYJDENWLFXJTVAKFODUSCMVEUPZHNWPXOYGLGSDXIBUTNDVFJZYHRHNFDNPTFVBCKWIMSLKKKQSENLEDOTEZJLGABBFNZVFRPWKASTKLDLSKGJBZHQACGSVOYUMMKGKRKKIMSLKKKQSGAOXXDJTDAOOBIMZXHDXFEYUDTETVJAAGISCSAWVGGSCQBXSLVAQRJTVZEEPBHBUKQLQGEWVDCNEEQEDXPYBHCZGRQ
```
![](https://hackmd.io/_uploads/rJYbww8oh.png)
- Để ý ở gần cuối có cụm `THEFLAGITSEVERYTHINGAFTERTHIS`, vậy phần phía sau cụm đó là flag.
- Flag: corctf{ATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS}
> Fun fact: bài này mình đã tìm được flag nhưng không thấy flag trong lúc diễn ra giải =)))
> https://hackmd.io/@GNF6eq5FT3W48I2WRj0Wlg/r19hvxLs2
