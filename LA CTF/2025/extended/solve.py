ct = open("chall.txt", 'rb').read()
flag = [bytes([c ^ 0b10000000]) for c in ct]
print(b''.join(flag))