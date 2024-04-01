from pwn import * 
from z3 import * 
from tqdm import trange
# r = process(["python3", "main.py"])
r = remote(b'betta.utctf.live', 7496)
def test(i,b,x, st):
	response = 1
	for t in range(5):
		a = ord(st[t]) - ord('a')
		response = (response*(a-b[t])) % 31
	return response == x[i]

payload = ["abcde", "fghij", "otjgs", "rpqjk", "wwdao"]
def brute():
	x = []
	for i in range(5):
		r.sendlineafter(b"What's your guess?\n", payload[i].encode())
		x.append(int(r.recvlineS().strip()))

	for b0 in trange(26):
		for b1 in range(26):
			for b2 in range(26):
				for b3 in range(26):
					for b4 in range(26):
						if all(test(i, [b0,b1,b2,b3,b4],x, payload[i]) for i in range(5)):
							answer = "".join(map(chr, [b0 + 97, b1+97, b2+97, b3+97, b4+97]))
							r.sendlineafter(b"What's your guess?\n", answer.encode())
							print(r.recvline())
							return

for i in range(3):
	brute()
r.interactive()



