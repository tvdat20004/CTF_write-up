from pwn import xor 
enc = bytes.fromhex("134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9")
key = xor(b'HTB{', enc[:4])
print(xor(enc, key))