from Crypto.PublicKey import RSA
from Crypto.Util.number import * 
from gmpy2 import iroot
def readKey(file):
    with open(file, 'r') as pem_file:
        pem_data = pem_file.read()
    public_key = RSA.import_key(pem_data)
    return public_key.n, public_key.e 

n1,e1 = readKey("pk1.pem")
n2,e2 = readKey("pk2.pem")
n3,e3 = readKey("pk3.pem")

c1 = bytes_to_long(open("file1.txt", "rb").read()) # m^17
c2 = bytes_to_long(open("file2.txt", "rb").read()) # m^65537
c3 = bytes_to_long(open("file3.txt", "rb").read())
x = pow(c1,e2//e1, n1) # m ^ 65535 
x = c2 * pow(x, -1, n1) % n1 #m^2 
x = pow(x,8,n1) # m^16 
x = c1 * pow(x, -1, n1) % n1 
print(long_to_bytes(x))

