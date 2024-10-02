from pwn import * 
from Crypto.Util.number import long_to_bytes
from tqdm import trange
import threading
# r = process(["python3", "server.py"])
r = remote("83.136.255.40", 53718)

# flagbin_len = 214 
flagbin_len = 470
flagbin = '100100001010100010000100111101101100100010010010111001101110100011100100110100101100010011101010111010001100101011001000101111101100101011100100111001001101111011100100101111101101110011011100111010001011111011000010011001000111000011'
# print(r.recvlineS())
try:
	for i in trange(234,flagbin_len):
		for j in trange(20):
			r.sendlineafter(b'Specify the index of the bit you want to get an encryption for : ', str(i).encode())
			r.recvline()
			r.recvline()
			# A = int(r.recvlineS().strip().split('=')[1])
			b = int(r.recvlineS().strip().split('=')[1])
			if b < 0 or b >= 256:
				# print(b)
				# print(j)
				flagbin += '1'
				break
		else:
			flagbin += '0'
except: 
	print(i)
	print(flagbin)
print(flagbin)	
print(long_to_bytes(int(flagbin, 2)))
# HTB{dIstributed_error_nnt_a28e6d90029751923dcd0c9d00f32e81}
