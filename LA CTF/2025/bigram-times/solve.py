from sage.all import *
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"
enc = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
def bigram_multiplicative_shift(bigram):
    assert(len(bigram) == 2)
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]
def encrypt(s):
	shifted_flag = ""
	for i in range(0, len(s), 2):
	    bigram = s[i:i+2]
	    shifted_bigram = bigram_multiplicative_shift(bigram)
	    shifted_flag += shifted_bigram
	return shifted_flag
# print(encrypt('lactf{'))
flag = ""
for i in range(0, len(enc), 2):
	chr1, chr2 = enc[i:i+2]
	pos1 = characters.find(chr1) + 1 
	pos2 = characters.find(chr2) + 1
	_pos1 = Mod(pos1**2 * pow(pos2, -1, 67) % 67, 67).nth_root(3, all=True)
	chrs1 = [characters[x-1] for x in _pos1]
	chrs1.remove(not_the_flag[i])
	chrs1.remove(also_not_the_flag[i])
	print(chrs1)
	_pos2 = pos1 * pow((characters.find(chrs1[0]) + 1)**2, -1, 67) % 67 - 1
	flag += chrs1[0] + characters[_pos2]
print(flag)

