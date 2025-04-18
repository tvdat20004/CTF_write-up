from pwn import *
import threading 
import json
# io1 = process(["python3", "challenge.py"])
# io2 = process(["python3", "challenge.py"])
io1 = remote("54.78.163.105",31895)
io2 = remote("54.78.163.105",31895)

rets = []
def insert(io, f : str, i : int, j : str):
	io.sendlineafter(b'|  > ', b'i')
	data = json.dumps({
		'f' : f,
		'i' : i,
		'j' : j
	}).encode()
	io.sendlineafter(b'|  > (JSON) ', data)
	ret = bytes.fromhex(io.recvlineS().strip().split('0x')[1])
	uiv = io.recvlineS().strip()
	rets.append(ret)
	print(uiv)
	
add = 'a'*16*3
thread1 = threading.Thread(target=insert, args=(io1, 'flag', 0, add))
thread2 = threading.Thread(target=insert, args=(io2, 'flag', 100, add))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

for i in [0,1]:
	keystream1 = xor(rets[i][:len(add)], add.encode())
	enc_counter = [keystream1[i:i+16] for i in range(0, len(keystream1), 16)]
	enc = [rets[(i+1)%2][i:i+16] for i in range(0, len(rets[(i+1)%2]), 16)]

	print(b''.join(xor(counter, e) for counter, e in zip(enc_counter, enc)))
