from pwn import xor 
from hashlib import sha256
LENGTH = 32 
enc = bytes.fromhex("fd94e649fc4c898297f2acd4cb6661d5b69c5bb51448687f60c7531a97a0e683072bbd92adc5a871e9ab3c188741948e20ef9afe8bcc601555c29fa6b61de710a718571c09e89027413e2d94fd3126300eff106e2e4d0d4f7dc8744827731dc6ee587a982f4599a2dec253743c02b9ae1c3847a810778a20d1dff34a2c69b11c06015a8212d242ef807edbf888f56943065d730a703e27fa3bbb2f1309835469a3e0c8ded7d676ddb663fdb6508db9599018cb4049b00a5ba1690ca205e64ddc29fd74a6969b7dead69a7341ff4f32a3f09c349d92e0b21737f26a85bfa2a10d")
known = b'Great and Noble Leader of the Tariaki'
key = xor(enc[:32], known[:32])

flag = b''

for i in range(0, len(enc), 32):
	chunk = enc[i:i+32]
	flag += xor(key, chunk)
	key = sha256(key).digest()
print(flag)