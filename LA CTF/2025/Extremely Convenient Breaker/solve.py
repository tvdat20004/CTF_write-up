from pwn import * 
# io = process(["python3", "chall.py"])
io = remote("chall.lac.tf", 31180)
io.recvline()
flag_enc = bytes.fromhex(io.recvlineS().strip())
n = len(flag_enc)
blocks = [flag_enc[i:i+16] + b'\0'*(64-16) for i in range(0, n, 16)]
flag = b''
for block in blocks:
	io.sendlineafter(b'What ciphertext do you want me to break in an extremely convenient manner? Enter as hex: ', block.hex().encode())
	flag += io.recvline()[2:18]
print(flag)

