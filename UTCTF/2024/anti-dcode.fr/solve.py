encrypted = open("LoooongCaesarCipher.txt", "r").read()

from tqdm import tqdm, trange
def shift(char, n):
	if char.isalpha():
		new_char = chr(((ord(char) - ord('a')) + n) % 26 + ord('a'))
	else:
		new_char = char 
	return new_char

for n in trange(26):
	dec = ""
	for char in encrypted:
		dec += shift(char, n)
	if 'utflag{' in dec:
		open("flag.txt", "w").write(dec)
		break

# utflag{rip_dcode}