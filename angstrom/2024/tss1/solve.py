from pwn import * 
from hashlib import sha256
import fastecdsa.curve
import fastecdsa.keys
import fastecdsa.point
curve = fastecdsa.curve.secp256k1

# r = process(["python3", "tss1.py"])
r = remote("challs.actf.co", 31301)

def send_point(point):
	r.sendlineafter(b'x: ', str(point.x).encode())
	r.sendlineafter(b'y: ', str(point.y).encode())

def hash_transcript(pk, R, msg):
	h = sha256()
	h.update(f'({pk.x},{pk.y})'.encode())
	h.update(f'({R.x},{R.y})'.encode())
	h.update(msg)
	return int.from_bytes(h.digest(), 'big') % curve.q
pk = eval(r.recvlineS().strip().split(':')[1])
pk = fastecdsa.point.Point(pk[0], pk[1], curve=curve)
fake_pk = -pk + curve.G 
send_point(fake_pk)
r.sendlineafter(b'message: ', b'11')
nonce = eval(r.recvlineS().strip().split(':')[1])
nonce = fastecdsa.point.Point(nonce[0], nonce[1], curve=curve)
fake_nonce = -nonce + curve.G
send_point(fake_nonce)

fake_c = hash_transcript(curve.G, curve.G, b'flag')
fake_s = (1 - fake_c) % curve.q
r.sendlineafter(b'c: ', str(fake_c).encode())
r.sendlineafter(b's: ', str(fake_s).encode())
r.interactive()
