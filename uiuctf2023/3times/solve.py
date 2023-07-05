with open('c1', 'rb') as c1:
	c1 = c1.read()
with open('c2', 'rb') as c2:
	c2 = c2.read()
with open('c3', 'rb') as c3:
	c3 = c3.read()

with open('p2','rb') as p2:		
	p2 = p2.read()
def xor(a,b):
	# assert len(a) == len(b)
	return bytes(i^j for i,j in zip(a,b))
key = xor(c2,p2)
print(xor(c1,key))
print(xor(c3,key))
# b'before computers, one-time pads were sometimes'
# b'uiuctf{burn_3ach_k3y_aft3r_us1ng_1t}'
