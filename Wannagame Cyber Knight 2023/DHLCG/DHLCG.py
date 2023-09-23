from Crypto.Util.number import long_to_bytes as ltb , getPrime, isPrime, getRandomRange
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad 
import random
from secret import FLAG, hint
from hashlib import sha256 

def f(a, b, x, mod):
    return (a*x + b) % mod 

def Xn(a, b, x, n, mod):
    X = x 
    for i in range(n):
        X = f(a, b, X, mod)
    return X 
    #you may think:"How da heo can this compute such a large number?"
    #because I have a supercomputer, idiot :P

p = 253124343713187900774555463876030540737349270963561331390907876266826416285173608781046103998025571922987541328220629719904523466259089107010586433496746979699703152921471010925715339786724191668080154086619451623075539654108918173538947700048917690068763753304706837347078871045230506141231379595014672208368105497383
#print(p)
a = getRandomRange(1, p)
b = getRandomRange(1, p)

print(f"p : {p}")
print(f"a : {a}")
print(f"b : {b}")

random.seed(random.randint(1, 0x1337)) #to spice things up, I will random the x0, so you have to find it yourself

x = random.randint(1, p - 1)


AliceKey = getRandomRange(1, p)
BobKey = getRandomRange(1, p)
AlicePubkey = Xn(a, b,x, AliceKey, p)
BobPubkey = Xn(a, b, x, BobKey, p)

print(f"Alice Public Key : {AlicePubkey}")
print(f"Bob Public Key : {BobPubkey}")

assert(Xn(a, b, AlicePubkey, BobKey, p) == Xn(a, b, BobPubkey, AliceKey, p))

sharekey = Xn(a, b, AlicePubkey, BobKey, p)
#LCG is hard, so I will probaly give you some hint about flag
print(f"hint : {hint}")

#it's time for final part: encrypting
iv = get_random_bytes(16)
key = sha256(str(sharekey).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
encrypted = cipher.encrypt(pad(FLAG, 16))
print(f"iv : {iv.hex()}")
print(f"enc : {encrypted.hex()}")
print(f"complete!")
#another thing, you will probaly gonna receive a gift from me when you "decrypt the FLAG"
