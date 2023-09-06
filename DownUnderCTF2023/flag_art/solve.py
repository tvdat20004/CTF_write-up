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
# Congratulations on solving this challenge! The mask has 900 X's so here are some random words to make the message long enough. Your flag is: DUCTF{r3c0nstruct10n_0f_fl4g_fr0m_fl4g_4r7_by_l00kup_t4bl3_0r_ch1n3s3_r3m41nd3r1ng?}
