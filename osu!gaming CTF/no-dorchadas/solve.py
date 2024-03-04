from pwn import * 
from base64 import * 
import HashTools

r = remote("chal.osugaming.lol", 9727)
dorchadas_slider = b"0,328,33297,6,0,B|48:323|61:274|61:274|45:207|45:207|63:169|103:169|103:169|249:199|249:199|215:214|205:254,1,450.000017166138,6|6,1:1|2:1,0:0:0:0:"
r.recvline()
PoW = r.recvlineS()
print(PoW)
sol = input("Solution: ")
r.sendlineafter(b'solution: ', sol.encode())
r.sendlineafter(b'Enter your option: ', b'1')

beatmap = b64encode(b'1')
r.sendlineafter(b'Enter your beatmap in base64: ', beatmap)
signature = r.recvlineS().strip().split()[-1]
# Hash length extension attack
magic = HashTools.new("md5")
new_beatmap, new_sig = magic.extension(secret_length=244, original_data=b'1', append_data=dorchadas_slider, signature=signature)
r.sendlineafter(b'Enter your option: ', b'2')
r.sendlineafter(b'Enter your beatmap in base64: ', b64encode(new_beatmap))
r.sendlineafter(b'Enter your signature for that beatmap: ', new_sig.encode())
r.interactive()

