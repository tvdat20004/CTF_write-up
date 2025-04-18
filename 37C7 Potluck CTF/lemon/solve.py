from pwn import * 
from Crypto.Util.number import long_to_bytes
# r = remote('challenge18.play.potluckctf.com',31337)
r = process(['python3', "final.py"])
r.recvuntil(b'p: ')
p = int(r.recvuntilS(b'\n').strip())

def get_para():
    r.recvuntil(b'ct: ')
    ct = int(r.recvuntilS(b'\n').strip())
    iv = int(r.recvlineS().strip().split(':')[1])
    r.recvuntil(b'key: ')
    key = list(map(int, r.recvlineS().strip().split(',')))
    return ct, iv, key

def encrypt(msg, lemon, lime):
	msgWithLemonAndLime = 0
	for idx in range(8):
		lemonSlice = lemon[idx]
		char = msg[idx]
		if (lime >> idx) & 1:
			char **= 2		
			char %= p
		msgWithLemonAndLime += char * lemonSlice
		msgWithLemonAndLime %= p
	return msgWithLemonAndLime
pos = [0] * 16
A = []
B = []
IV = []
# while all(pos):
for i in range(16):
    r.sendlineafter(b'> ', b'2')
    ct, iv, key = get_para()
    B.append(ct)
    IV.append(iv)
    row_A = []
    for idx in range(0,16,2):
        if (iv >> (idx//2)) & 1:
            pos[idx] = 1
            row_A.append(key[idx//2])
            row_A.append(0)
        else:
            pos[idx+1] = 1
            row_A.append(0)
            row_A.append(key[idx//2])
    A.append(row_A)


assert all(pos)
# print(A)
from sage.all import *  
from sympy.ntheory import sqrt_mod
matA = matrix(GF(p), A)
matB = matrix(GF(p),16,1, B)
X = (~matA)*matB 
X = [int(x[0]) for x in X]



pkcs16 = []
for i in range(0,16,2):

    if pow(X[i],2,p) == X[i+1]:
        pkcs16.append(X[i])
    elif pow(X[i+1],2,p) == X[i]:
        pkcs16.append(X[i+1])
    else:
        print('fail')
        exit()

t = 0
while True:
    flag = t
    print(t)
    for i in pkcs16[::-1]:
        flag = flag * p + i
    if b'potluck' not in long_to_bytes(flag):
        t += 1
        continue
    else:
        print(long_to_bytes(flag))
        break