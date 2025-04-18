from pwn import *
from Crypto.Util.number import long_to_bytes
connect = remote("morphing.chal.uiuc.tf", 1337)
g = 2
data = connect.recvuntil(b'p = ')
p = int(connect.recvuntil(b'\n').decode().strip())
data = connect.recvuntil(b'A = ')
A = int(connect.recvuntil(b'\n').decode().strip())
data = connect.recvuntil(b'c1_ = ')
connect.sendline(b'2')
data = connect.recvuntil(b'c2_ = ')
connect.sendline(str(A).encode())
data = connect.recvuntil(b'm = ')
m = int(connect.recvuntil(b'\n').decode().strip())

print(long_to_bytes(m))
# b'uiuctf{h0m0m0rpi5sms_ar3_v3ry_fun!!11!!11!!}'