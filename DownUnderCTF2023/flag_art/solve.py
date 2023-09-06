template = open("output.txt", 'r').read()
palette = {
	'.' : 0,
	'=' : 1,
	'w' : 2,
	'-' : 3,
	'o' : 4,
	'^' : 5,
	'*' : 6,
}
mod = [2, 3, 5, 7]
from sympy.ntheory.modular import crt 
template = template.replace(' ','').replace('\n','')
assert len(template)%4 == 0
flag = ''
for i in range(0,len(template),4):
	idx = crt(mod, [palette[template[i]], palette[template[i+1]], palette[template[i+2]], palette[template[i+3]]])[0]
	flag += chr(idx)
print(flag)