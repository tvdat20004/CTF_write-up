enc = 'AFCNUUOCGIFIDTRSBHAXVHZDRIEZMKTRPSSXIBXCFVVNGRSCZJLZFXBEMYSLUTKWGVVGBJJQDUOXPWOFWUDHYJSMUYMCXLXIWEBGYAGSTYMLPCJEOBPBOYKLRDOJMHQACLHPAENFBLPABTHFPXSQVAFADEZRXYOXQTKUFKMSHTIEWYAVGWWKKQHHBKTMRRAGCDNJOUGBYPOYQQNGLQCITTFCDCDOTDKAXFDBVTLOTXRKFDNAJCRLFJMLQZJSVWQBFPGRAEKAQFUYGXFJAWFHICQODDTLGSOASIWSCPUUHNLAXMNHZOVUJTEIEEJHWPNTZZKXYSMNZOYOVIMUUNXJFHHOVGPDURSONLLUDFAGYGWZNKYXAGUEEEGNMNKTVFYZDIQZPJKXGYUQWFPWYEYFWZKUYUTXSECJWQSTDDVVLIYXEYCZHYEXFOBVQWNHUFHHZBAKHOHQJAKXACNODTQJTGC'


SHIFT = 65
MOD = 26
BLOCKLENGTH = 20

def get_blocks(s):
	blocks = []
	i = 0
	while(i + BLOCKLENGTH < len(s)):
		blocks.append(s[i:i + BLOCKLENGTH])
		i = i + BLOCKLENGTH
	blocks.append(s[i:len(s)])
	return(blocks)
def sub(block1,block2):
	assert(len(block1)<= len(block2))
	assert(len(block2)<= BLOCKLENGTH)
	b1upper = block1.upper()
	b2upper = block2.upper()
	b1 = [ord(b1upper[i])-SHIFT for i in range(len(block1))]
	b2 = [ord(b2upper[i])-SHIFT for i in range(len(block1))]
	s = [(b1[i] - b2[i]) % MOD for i in range(len(block1))]
	slist = [chr(s[i]+SHIFT) for i in range(len(block1))]
	sum = ''.join(slist)
	return(sum)

blocks = get_blocks(enc)
print(blocks)
new_cipher = ""
for i in range(len(blocks)-1, 0, -1):
	new_cipher = sub(blocks[i], blocks[i-1]) + new_cipher
print(len(new_cipher))

a = "THISISAVERYLONGFLAGWITHMANYBLOCKSTOHIDEANDALLINCAPITALSTHEFLAGENDSHERENOWFOLLOWSALONGTEXTTHETEXTWASWRITTENONLYINORDERTOGIVEYOUMOREINFORMATIONFORBREAKINGVIGENERESCIPHERSINCEITSOMETIMESTAKESSOMETEXTTOGETTHESTATISTICSRIGHTDOESNTITITVIGENERESCIPHERWASLONGTHOUGHTTOBEUNBREAKABLEHUNDREDSOFYEARSPASSEDUNTILKASISKIBROKEITSINCETHENITISNOTSECUREANYMOREANDITSEEMSTHATNOTEVENCBCCANSAVEITDOYOUBELIEVETHATCOUNTERMODEISANYBETTERIHONESTLYDOUBTITSINCEITISSTILLJUSTASUM"
print(a[:70])