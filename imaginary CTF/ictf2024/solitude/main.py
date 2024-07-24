#!/usr/bin/env  python3

import random

def xor(a: bytes, b: bytes):
	out  =  []
	for  m,n  in  zip(a,b):
		out.append(m^n)
	return  bytes(out)

class RNG():
	def __init__(self, size, state=None):
		self.size = size
		self.state = list(range(128+2))
		# random.shuffle(self.state)
		print(self.state)

	def next(self):
		# swap 128 voi so dung sau no
		idx = self.state.index(128)
		self.state.pop(idx)
		self.state.insert((idx+1) % (len(self.state)+1), 128)
		###
		# neu 128 o pos 0, dua no len pos 1
		if self.state[0] == 128:
			self.state.pop(0)
			self.state.insert(1, 128)
		###
		# lam tuong tu voi phan tu 129
		idx = self.state.index(129)
		self.state.pop(idx)
		self.state.insert((idx+1) % (len(self.state)+1), 129)
		###
		# neu 129 o pos 0, dua no len pos 2
		if self.state[0] == 129:
			self.state.pop(0)
			self.state.insert(1, 129)
		if self.state[1] == 129:
			self.state.pop(1)
			self.state.insert(2, 129)
		###
		# __(1)__128__(2)__129__(3)__ => __(3)__128__(2)__129__(1)__
		c1 = self.state.index(128)
		c2 = self.state.index(129)
		self.state = self.state[max(c1,c2)+1:] + [128 if c1<c2 else 129] + self.state[min(c1,c2)+1:max(c1,c2)]  +  [128  if  c1>c2  else  129]  +  self.state[:min(c1,c2)]
		###

		count = self.state[-1]
		if count in [128,129]:
			count = 128
		self.state = self.state[count:-1] + self.state[:count] + self.state[-1:]	
		idx = self.state[0]
		if idx in [128,129]:
			idx = 128
		out = self.state[idx]
		if out in [128,129]:
			out = self.next()
		return out

if __name__ == "__main__":
	# flag = open("flag.txt", "rb").read()
	flag = b'ictf{test_flag_039i3294i3294i923}'
	while True:
		i = int(input("got flag?"))
		for _ in range(i):
			rng = RNG(128)
			x = [rng.next() for _ in range(len(flag))]
			print(x)
			stream = bytes(x)
			print(list(xor(flag, stream)))
			print(xor(flag, stream).hex())