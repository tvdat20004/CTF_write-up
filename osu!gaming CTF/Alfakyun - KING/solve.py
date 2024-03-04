fileFormat = b'osu file format '
from pwn import xor
# def xor(a,b):
# 	return bytes([i ^ j for i, j in zip(a,b)])
enc = open("flag.osu.enc", "rb").read()
key = xor(enc[:16], fileFormat)
print(key)
with open('flag.osu', "wb") as file:
	file.write(xor(enc, key))

