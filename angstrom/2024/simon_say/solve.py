from z3 import *

def S(x, j):
    j = j % 64
    return ((x << j) | LShR(x, (64 - j))) & 0xffffffffffffffff

def SS(x,j):
    j = j % 64
    return ((x << j) | (x >> (64 - j))) & 0xffffffffffffffff

ct1 = bytes.fromhex('fd76dbfc85e68362be3231c4a07fedcd90bf361ac3943de5a86b4e57d0fdcf5a12e56301ac4867392dca08a972a10431')
ct2 = bytes.fromhex('96dbd7e58120984bfd76dbfc85e68362645aa36f6ec1238490bf361ac3943de5ece6b9fdbfc4ea0f12e56301ac486739')
ct3 = bytes.fromhex('429338f593432bb30002f715f77e7bdf2ce179c9be5c8659233df19bed12382e27da9c498275da7bcb8dec1a8d003e19')
k0 = 0
def f(x, y, k):
    return y ^ (S(x,1) & S(x,8)) ^ S(x,2) ^ k, x 

k1 = BitVec('k1', 64)
k2 = BitVec('k2', 64)
k3 = BitVec('k3', 64)
s = Solver()

def add_block(offset):
    x1, y1 = int.from_bytes(ct1[offset:offset+8], "big"), int.from_bytes(ct1[offset+8:offset+16], "big")
    x2, y2 = int.from_bytes(ct2[offset:offset+8], "big"), int.from_bytes(ct2[offset+8:offset+16], "big")
    x3, y3 = int.from_bytes(ct3[offset:offset+8], "big"), int.from_bytes(ct3[offset+8:offset+16], "big")

    k0 = y1 ^ (SS(x1,1) & SS(x1,8)) ^ SS(x1,2) ^ x2

    # Add constraints for the solver
    x_next, y_next = f(BitVecVal(x2, 64), BitVecVal(y2, 64), k1)
    x_next, y_next = f(x_next, y_next, k2)
    x_next, y_next = f(x_next, y_next, k3)
    s.add(x_next == BitVecVal(x3, 64))
    s.add(y_next == BitVecVal(y3, 64))
    return k0

# Add blocks
k0 = add_block(0)
k0 = add_block(16)
k0 = add_block(32)

# Function to get all solutions
def get_all_solutions(s, variables):
    solutions = []
    while s.check() == sat:
        m = s.model()
        solution = {v: m[v] for v in variables}
        solutions.append(solution)
        
        # Add a constraint to block the current solution
        block = []
        for v in variables:
            block.append(v != m[v])
        s.add(Or(block))
    
    return solutions

# Get all solutions for k1, k2, k3
solutions = get_all_solutions(s, [k1, k2, k3])
candidate = []
for sol in solutions:
    k1_val = sol[k1].as_long()
    k2_val = sol[k2].as_long()
    k3_val = sol[k3].as_long()
    candidate.append([k0,k1_val, k2_val, k3_val])
print(candidate)
def S(x, j):
    j = j % 64
    return ((x << j) | (x >> (64 - j))) & 0xffffffffffffffff
z = 0b01100111000011010100100010111110110011100001101010010001011111
def reKey(k):
    k = [0]*68 + k 
    for i in range(67, -1, -1):
        tmp = S(k[i+3], -3) ^ k[i+1]
        tmp ^= S(tmp, -1)
        zi = (z >> (i % 62)) & 1
        k[i] = k[i+4] ^ tmp ^ zi ^ 0xfffffffffffffffc
    return k 
class Simon:
    n = 64
    m = 4
    z = 0b01100111000011010100100010111110110011100001101010010001011111

    def __init__(self, k, T):
        self.T = T
        self.k = self.schedule(k)

    def S(self, x, j):
        j = j % self.n
        return ((x << j) | (x >> (self.n - j))) & 0xffffffffffffffff

    def schedule(self, k):
        k = k[:]
        for i in range(4, self.T):
            tmp = self.S(k[i - 1], -3)
            tmp ^= k[i - 3]
            tmp ^= self.S(tmp, -1)
            zi = (self.z >> ((i - 4) % 62)) & 1
            k.append(k[i - 4] ^ tmp ^ zi ^ 0xfffffffffffffffc)
        return k

    def encrypt(self, x, y):
        for i in range(self.T):
            tmp = x
            x = y ^ (self.S(x, 1) & self.S(x, 8)) ^ self.S(x, 2) ^ self.k[i]
            y = tmp
        return x, y
    def decrypt(self, x, y):
        for i in range(self.T - 1, -1, -1):
            tmp = y
            y = x ^ (self.S(y, 1) & self.S(y, 8)) ^ self.S(y, 2) ^ self.k[i]
            x = tmp
        return x, y
for key in candidate:
    key = reKey(key)
    cipher = Simon(key[:4], 72)
    pt = b""    
    for i in range(0, len(ct3), 16):
        x = int.from_bytes(ct3[i:i+8], 'big')
        y = int.from_bytes(ct3[i+8:i+16], 'big')
        x,y = cipher.decrypt(x,y)
        pt += x.to_bytes(8, "big")
        pt += y.to_bytes(8, "big")
    if b'actf{' in pt:
        print(pt)