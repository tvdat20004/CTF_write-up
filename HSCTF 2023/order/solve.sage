# from sympy.ntheory.residue_ntheory import discrete_log
from Crypto.Util.number import long_to_bytes
# from math import gcd
M = 48743250780330593211374612602058842282787459461925115700941964201240170956193881047849685630951233309564529903
sus = 11424424906182351530856980674107667758506424583604060548655709094382747184198
a = 19733537947376700017757804691557528800304268370434291400619888989843205833854285488738413657523737062550107458

R = Integers(M)
exp=pow(sus,-1,M)
exp = R(exp)
sus = R(sus)
t1 = exp.log(sus)

t2 = t1 + 1 
a_inv = pow(a,-1,M)
for i in range(1000):
    t = t1 + t2*i
    inverted_flag = ((t*a_inv)%M)
    
    flag = long_to_bytes(int(pow(inverted_flag,-1,M)))
    
        
    if b"flag" in flag:
        print((flag))
        break
# b'flag{big_numbers_are_bad_numbers}'