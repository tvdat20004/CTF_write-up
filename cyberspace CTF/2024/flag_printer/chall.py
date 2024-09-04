from out import enc, R
from math import prod, log

flag = ''
def find_a_i(i):
    if i < 3:
        return i 
    return find_a_i(i - 3**int(log(i, 3))) + 1 
a = [0]
for i in range(355):
    # b = [_+1 for _ in a]
    # c = [_+1 for _ in b]
    # a += b + c

    if i%5 == 0:
        # print(a)
        flag += chr(enc[i//5] ^ prod([find_a_i(_) for _ in R[i//5]]))
        print(flag)

# print(find_a_i(20))
