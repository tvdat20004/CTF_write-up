from pwn import xor
from random import randint
from hashlib import sha256
# from FLAG import flag
flag = b'CSCTF{test_flag_3929r92ir932i932i94i29i}'
# cc = [randint(-2**67, 2**67) for _ in range(9)]
# key = sha256("".join(str(i) for i in cc).encode()).digest()
# enc = xor(key, flag)
cc = [-24994672392226112460, 52076559868776142619, -2886520569997652450, 5173607328856093183, 18843099102067101600, 44263034914294883858, 730645205313637392, 27323005442529582383, -22499905574259647074]
assert all(-2**67 < c < 2**67 for c in cc)
def superfnv():
    x = 2093485720398457109348571098457098347250982735
    k = 1023847102938470123847102938470198347092184702
    for c in cc:
        x = k * (x + c)
    return x % 2**600

# print(f"{enc.hex() = }")
print(f"{superfnv() = }")

# enc.hex() = '4ba8d3d47b0d72c05004ffd937e85408149e13d13629cd00d5bf6f4cb62cf4ca399ea9e20e4227935c08f3d567bc00091f9b15d53e7bca549a'
# superfnv() = 2957389613700331996448340985096297715468636843830320883588385773066604991028024933733915453111620652760300119808279193798449958850518105887385562556980710950886428083819728334367280