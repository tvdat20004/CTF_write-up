M = 48743250780330593211374612602058842282787459461925115700941964201240170956193881047849685630951233309564529903

def new_hash(n):
    return n % M

def bytes_to_long(x):
    return int.from_bytes(x, byteorder="big")


# flag = open('flag.txt').read()
# flag = bytes_to_long(bytes(flag, 'utf-8'))
flag = bytes_to_long(b'flag{big_numbers_are_bad_numbers}')

sus = 11424424906182351530856980674107667758506424583604060548655709094382747184198
a = 19733537947376700017757804691557528800304268370434291400619888989843205833854285488738413657523737062550107458

t = new_hash(pow(flag, -1, M) * a)
exp = pow(sus,t,M)
thonk = new_hash(sus * exp)

print(thonk)
# Prints 1
