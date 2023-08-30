from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random
import secrets
from math import gcd
from hashlib import sha256

with open("flag.txt", "r") as f:
    flag = f.read().strip()

p=321745663660247264291912215381637140417426688166015765275016210974556618758108512916610772162708204242718465157404139876459846002727737598770450096642577891574129129971012786587775953761848931824322238298796689177818180751598982715142951891422895346040998252803256088344802677303563385039814682978344426511715095691285388244489299297982227614003912768214636964321398389670878817486572327863439909202202081589795055421943157234879795603541548858027867750020945742125759405585313
phip=321745663644137982453501751034221060149614281161498341317222863749664050347172052681857047928547879705531299049154183650170680637970523254049664158808042174556716753365060726738603147796721808427564722017179205844642415680516623360771297641357692292883806714929259580181939062408839661980293643073341981033892197854036112428722287761866221556690139833651293949000994649963638735512908155844345490505426385507145073171151591168489874072082195193477266931712000000000000000000000
q=517705423061 # enough for a 24h ctf hahahahahahahaha

h = random.randint(2, p-2)
g = pow(h, phip//q, p)
while g<=1 and gcd(h, p)==1:
    h = random.randint(2, p-2)
    g = pow(h, phip//q, p)

x = random.randint(100000000001, q-1)
y = pow(g, x, p)

assert pow(g, q, p) == 1
assert pow(h, phip, p) == 1

def signing(message: bytes):
    r = 0; s = 0
    while r==0 or s==0:
        k = random.randint(1, q-1)
        r = pow(g, k, p) % q
        s = (pow(k, q-2, q) * (int(sha256(message).hexdigest(),16) + x*r)) % q
    return r, s

def verification(message: bytes, r: int, s: int):
    if not (r in range(q) and s in range(q)):
        return False
    w = pow(s, -1, q)
    u1 = (int(sha256(message).hexdigest(),16) * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r

# let's test if it works

message = b"Hello, world!"
r, s = signing(message)
assert verification(message, r, s), "Something is wrong"

print("Here are the parameters:")
print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")
print(f"y = {y}")

sm = secrets.token_urlsafe(12)
print(f"I only trust the signer with public key y. \nPlease sign: {sm}")

r = int(input("r = "))
s = int(input("s = "))

if verification(sm.encode(), r, s):
    print(f"Here is your flag: {flag}")
else:
    print("Invalid signature. Byebye! See you never")
