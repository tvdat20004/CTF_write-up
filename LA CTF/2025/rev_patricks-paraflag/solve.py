
target = 'l_alcotsft{_tihne__ifnlfaign_igtoyt}'
v3 = len(target)
flag = [None] * v3
v4 = v3 >> 1 
v5 = 0 
while 1:
	flag[v5] = target[2*v5]
	flag[v4 + v5] = target[2*v5 + 1]
	v5 += 1
	if v5 >= v4:
		break
print(''.join(flag))