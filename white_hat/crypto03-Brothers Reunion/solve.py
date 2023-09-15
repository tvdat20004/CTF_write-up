import base64
import binascii
seq = [78,6,1,65,0,57,1,78,0,28,1,99,0,23,1,78,0,9,1,2,1,33,1,78,0,6,1,81,0,39,1,78,0,9,1,2,1,50,0,40,1,16,1,82,0,25,1,77,0,45,1,103,0,49,0,41,1,16,1,77,0,42,1,78,0,6,1,23,1,15,1,79,0,5,1,77,0,50,0,28,1,28,1,1,1,15,1,79,0,68,0,31,1,53,0,25,1,9,1,2,1,49,0,29,1,44,1,77,0,50,0,27,1,45,1,107,0,50,0,29,1,5,1,77,0,52,0,52]
secret = 5
data = []
data.append(seq[0])
res = ""
idx = 0
for i in range(1,len(seq)-1,2):
	data.append(data[idx] * seq[i+1] + seq[i])
	idx += 1
for i in data:
	res += chr(i)


hex_str = base64.b64decode(res.encode('ascii')).decode()
stuff = binascii.unhexlify(hex_str).decode()
# print(stuff)
result = ""
for i in range(len(stuff)):
	
	char = stuff[i]
	if (char.isupper()):
		result += chr((ord(char) - pow(-1,i)*secret - 65) % 26 + 65)
	elif (char.islower()):
		result += chr((ord(char) - pow(-1,i)*secret - 97) % 26 + 97)
	elif (char.isdecimal()):
		result += chr((ord(char) - pow(-1,i)*secret - 48) % 10 + 48)
	else:
		result += char
print(result)
# K1n_0F_tH3_5T41n3d_B14d3