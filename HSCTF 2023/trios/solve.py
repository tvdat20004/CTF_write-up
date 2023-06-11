mess = "8wnAPR2svyje{RbcAPRRbczwtwDE2svphjIqr}. uZbphjRbc 4mL2sv8rv IqruZb BRzuZbAPRzr1Rbc 2svphj RbcphjoZYQHJ8rvzwtIqrRbcHu0 InbRbcBRzBRz2svyjeRbc, tKO8wn 4mLRbc JEzphjuZb4mL tKOIqrBRz APR2svphjyje4zD2svyjeRbc, tKOBRz IqruZb 8wntKOphjHu0 2sv Hu0tKO8wn8wnRbcQHJRbcphjIqr zwtAPR2svtKOphjIqrRbcGawIqr uZb8wn IqrwDERbc BRz2svInbRbc APR2svphjyje4zD2svyjeRbc APRuZbphjyje RbcphjuZb4zDyjewDE IqruZb 8wntKOAPRAPR uZbphjRbc BRzwDERbcRbcIqr uZbQHJ BRzuZb, 2svphjHu0 IqrwDERbcphj 4mLRbc oZYuZb4zDphjIqr IqrwDERbc uZboZYoZY4zDQHJQHJRbcphjoZYRbcBRz uZb8wn Rbc2svoZYwDE APRRbcIqrIqrRbcQHJ. IqrBRz tKOAPRAPRRbcyje2svAPR IqruZb uZb4mLphj k7j4zDBRzIqr uZbphjRbc yje4zDtKOphjRbc2sv zwttKOyje tKOphj S4mLtKOIqr2stRbcQHJAPR2svphjHu0.".split(" ")
chars = [chr(i) for i in range(48, 58)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

alpha = []
i = 0

for word in mess:
	i = 0
	# print(word)
	while i < len(word):
		if word[i] in chars:
			if word[i:i+3] not in alpha:
				alpha.append(word[i:i+3])
				# print(word[i:i+3])
			i += 3
		else:
			i += 1

keyboard_chars = [chr(i) for i in range(97, 123)]
dic = {term: char for char, term in zip(keyboard_chars, alpha)}
dec = ""
for word in mess:
	i = 0
	# print(word)
	while i < len(word):
		if word[i] in chars:
			if word[i:i+3] in dic.keys():
				dec += dic[word[i:i+3]]
			i += 3
		else:
			i += 1

print(dec)


