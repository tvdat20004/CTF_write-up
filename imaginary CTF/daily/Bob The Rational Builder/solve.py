
flag = b'ictf{'
p = 2**17 -1 
table = b'abcdefghijklmnopqrstuvwxyz0123456789{}_'
arr = [27804, 113082, 71154, 1, 108473, 46422, 70266, 9659, 5142, 116383, 49154, 127179, 16778]
hash = b'L3>\xb0C\xc0/(\xd9\xfa\xd3\xf2\xc4\x1a|\x18'

flag += bytes([flag[4] * pow(arr[2], -1, p) % p])
flag2 = b""
for i in range(4,len(arr)):
	for c1 in table:
		for c2 in table:
			if c1 * pow(c2,-1,p) % p == arr[i]:
				flag2 += bytes([c1,c2])



print(flag)
print(flag2)
import hashlib
for i in table:
	if hashlib.md5(flag + bytes([i])*2 + flag2).digest() == hash:
		print(flag + bytes([i])*2 + flag2)