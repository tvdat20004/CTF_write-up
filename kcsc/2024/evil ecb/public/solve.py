from pwn import * 
from json import * 
r = remote("103.163.24.78", 2003)

data = b'aa{"username":"admin", "isAdmin": true          }\x01' 
# payload = b'{"username": "%s", "isAdmin": false}' % (data)
# block = [payload[i : i+16] for i in range(0, len(payload), 16)]
# print(block)

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'Username: ', data)
token = bytes.fromhex(r.recvlineS().strip().split(':')[1])
new_token = token[16 : 16*4]
r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'Token: ', new_token.hex().encode())
r.interactive()