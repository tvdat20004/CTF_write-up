def boolean_function(x1, x2, x3, x4, x5, x6, x7, x8):
    clause1 = (x1 or x2 or not x5)
    clause2 = (not x1 or not x2 or x5)
    clause3 = (x1 or x3 or not x5)
    clause4 = (not x1 or not x3 or x5)
    clause5 = (x2 or x3 or not x5)
    clause6 = (not x2 or not x3 or x5)
    clause7 = (x1 or x2 or not x6)
    clause8 = (not x1 or not x2 or x6)
    clause9 = (x1 or x4 or not x6)
    clause10 = (not x1 or not x4 or x6)
    clause11 = (x2 or x4 or not x6)
    clause12 = (not x2 or not x4 or x6)
    clause13 = (x1 or x3 or not x7)
    clause14 = (not x1 or not x3 or x7)
    clause15 = (x1 or x4 or not x7)
    clause16 = (not x1 or not x4 or x7)
    clause17 = (x3 or x4 or not x7)
    clause18 = (not x3 or not x4 or x7)
    
    clause19 = (x2 or x3 or not x8)
    clause20 = (not x2 or not x3 or x8)
    clause21 = (x2 or x4 or not x8)
    clause22 = (not x2 or not x4 or x8)
    clause23 = (x3 or x4 or not x8)
    clause24 = (not x3 or not x4 or x8)
    return (clause1 and clause2 and clause3 and clause4 and clause5 and clause6 and
            clause7 and clause8 and clause9 and clause10 and clause11 and clause12 and
            clause13 and clause14 and clause15 and clause16 and clause17 and clause18 and
            clause19 and clause20 and clause21 and clause22 and clause23 and clause24)
mapping = dict()
import itertools
for x1, x2, x3, x4, x5, x6, x7, x8 in itertools.product([False, True], repeat=8):
    result = boolean_function(x1, x2, x3, x4, x5, x6, x7, x8)
    if result == 1:
        l1 = "".join(map(str,(map(int, [x1, x2, x3, x4]))))
        l2 = "".join(map(str,(map(int, [x5, x6, x7, x8]))))
        mapping[l1] = l2 

def recover(K1, K2):
    if all(c == "X" for c in K2): 
        if 'X' in K1:
            # case when K2 is full of X
            # replace X in K1 with 0 and 1
            K1_0 = K1.replace('X', '0')
            K1_1 = K1.replace('X', '1')
            if K1_0 in mapping.values(): 
                # check if K1_0 is one of the output of the boolean function
                return mapping[K1_0]
            else: 
                # if not, then K1_1 must be one of the output of the boolean function
                return mapping[K1_1]
        else:
            return mapping[K1]
    elif 'X' not in K2:
        # case when K2 is cleared
        return K2
    else:
        # case when K2 has 1 character X
        # replace X in K2 with 0 and 1
        K2_0 = K2.replace('X', '0')
        K2_1 = K2.replace('X', '1')
        if K2_0 in mapping.values(): 
            # check if K2_0 is one of the output of the boolean function
            return K2_0
        else:
            # if not, then K2_1 must be one of the output of the boolean function
            return K2_1




K_1702 = ("0101 1001 1111 0011 00X1 X111 1X00 00X0 111X X000 XXXX XXXX XXXX XXXX XXXX XXXX").split(" ")
K_1703 = ("XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX X111 000X X010 01X1 0X10 0101 0000 1111").split(" ")
recovered = ''
ciphertext = 0b1001100000111101011000111101010110110011101101110000000010000011
for i in range(len(K_1702)):
    recovered += recover(K_1702[i], K_1703[i])
K_1704 = ""
for i in range(0, len(recovered), 4):
    K_1704 += mapping[recovered[i:i+4]]
print(K_1704)
plaintext = ciphertext ^ int(K_1704, 2)
import struct
latitude = plaintext >> 32
longtitude = plaintext % (1<<32)

latitude = struct.unpack('!f', struct.pack('!I', latitude))[0]
longtitude = struct.unpack('!f', struct.pack('!I', longtitude))[0]
print(latitude, longtitude)