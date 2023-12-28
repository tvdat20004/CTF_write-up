from numpy import matrix

vectors = []
with open("enc.txt", "r") as file:
	for line in file.readlines():
		# print(line)
		vectors.append(matrix(eval(line.strip())))

pubkey = matrix([
    [47, -77, -85],
    [-49, 78, 50],
    [57, -78, 99]
])
flag = "H"
v12 = (vectors[1] - vectors[2]) * pubkey.I
print(round(v12[0,0]))
for i in range(0,len(vectors) - 1):
	vij = (vectors[i] - vectors[i + 1]).dot(pubkey.I)
	next_char = chr(ord(flag[-1]) - round(vij[0, 0]))
	flag += next_char
print(flag)