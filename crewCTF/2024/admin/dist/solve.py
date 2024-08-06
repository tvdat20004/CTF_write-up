from pwn import *  
import sys 
from Crypto.Util.Padding import pad
sys.path.append('/mnt/e/tvdat20004/CTF/tools/attacks/gcm/')
from forbidden_attack import * 
r = process(["python3", "prob.py"])

def get_token():
    r.sendlineafter(b'option(int): ', b'0')
    iv = b'0'*16
    r.sendlineafter(b'iv(hex): ', iv.hex().encode())
    curusername = r.recvline().strip().split(b' ')[2]
    data = bytes.fromhex(r.recvlineS())
    return curusername, data[:16], data[16:-16], data[-16:]
plain1, iv, enc1, tag1 = get_token()
plain2, iv, enc2, tag2 = get_token()
ct, tag = forgery_message([(plain1, enc1, b'', tag1),(plain2, enc2, b'', tag2)], pad(b'admin', 16))
r.sendlineafter(b'option(int): ', b'1')
print(ct)
print(tag)
payload = (b'0'*16) + ct + tag[0]
r.sendlineafter(b'token(hex): ', payload.hex().encode())
r.interactive()
