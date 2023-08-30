from pwn import *
from sage.all import *
def split_output(out):
	out = out.strip("[").strip().strip(']').split()
	out = [int(num) for num in out if num]
	return out


def get_matrix():
	mat = []
	while True:
		try:
			row = r.recvline().decode()
			# print(row)
			if not row.startswith('['):
				break
			else:
				mat.append(split_output(row))
		except:
			return mat
	return mat

r = remote("64.227.131.98",10001)

r.sendlineafter(b'(y/n)',b'y')
data = r.recvline()
data = r.recvline()
rot_matrix = matrix(ZZ, get_matrix())
flag_out = matrix(ZZ, get_matrix())
mat_f = (~rot_matrix) * flag_out * (~(rot_matrix.T))
flag = ''
for i in range(mat_f.ncols()):
	flag += chr(int(pow(mat_f[i][i],1/2)))
print(flag)
r.close()