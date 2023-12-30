#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long
from secrets import randbelow, randbits
# from FLAG import flag
flag = b'potluck{fake_flag_343223212}'
count = 8
size = 2048
lemonSize = size // 2 * count
prime = getPrime(size)
queries = 17

def pkcs16(msg):
	filledmsg = [0 for _ in range(count)]
	msg += b'A' * ((count * size // 8) - len(msg))
	cookedmsg = bytes_to_long(msg)
	for idx in range(count):
		cookedmsg, filledmsg[idx] = divmod(cookedmsg, prime)
	print(cookedmsg)
	return filledmsg

def encrypt(msg, key, iv):
	msgWithLemonAndLime = 0
	for idx in range(count):
		lemonSlice = key[idx]
		char = msg[idx]
		if (iv >> idx) & 1:
			char **= 2		
			char %= prime
		msgWithLemonAndLime += char * lemonSlice
		msgWithLemonAndLime %= prime
	return msgWithLemonAndLime

flag = pkcs16(flag)
print(f'Hello and welcome to the lima beans with lemon and lime cryptosystem. It it so secure that it even has a {lemonSize} bit encryption key, that is {lemonSize // 256} times bigger than an AES-256, and therefore is {lemonSize // 256} times more secure')
print(f'p: {prime}')
for turn in range(queries):
	print('1: Encrypt a message\n2: Encrypt flag\n3: Decrypt message')
	choice = input('> ')
	if choice not in ('1', '2', '3'):
		print('What?')
	if choice == '1':
		msg = input('msg: ').encode()
		if len(msg) * 8 > size * count:
			print('Hmmm a bit long innit?')
			continue
		msg = pkcs16(msg)
		key = [randbelow(2**(size - 48)) for _ in range(count)]
		iv = randbits(count)
		ct = encrypt(msg, key, iv)
		print(f'ct: {ct}')
		print(f'iv: {iv}')
		print(f'key: {",".join(map(str, key))}')
	elif choice == '2':
		key = [randbelow(2**(size//2)) for _ in range(count)]
		iv = randbits(count)
		ct = encrypt(flag, key, iv)
		print(f'ct: {ct}')
		print(f'iv: {iv}')
		print(f'key: {",".join(map(str, key))}')
	else:
		print('patented, sorry')