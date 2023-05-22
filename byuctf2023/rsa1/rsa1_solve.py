p =  18413880828441662521

q = 15631612382272805561 

e = 7
n = p*q
from Crypto.Util.number import long_to_bytes
c = 258476617615202392748150555415953446503
print(long_to_bytes(pow(c,pow(e,-1,(p-1)*(q-1)),n)))
# b'byuctf{too_smol}'
