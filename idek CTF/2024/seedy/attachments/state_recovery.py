import random
class Twister:
    N = 624
    M = 397
    A = 0x9908b0df

    def __init__(self):
        self.state = [ [ (1 << (32 * i + (31 - j))) for j in range(32) ] for i in range(624)]
        self.index = 0
    
    @staticmethod
    def _xor(a, b):
        return [x ^ y for x, y in zip(a, b)]
    
    @staticmethod
    def _and(a, x):
        return [ v if (x >> (31 - i)) & 1 else 0 for i, v in enumerate(a) ]
    
    @staticmethod
    def _shiftr(a, x):
        return [0] * x + a[:-x]
    
    @staticmethod
    def _shiftl(a, x):
        return a[x:] + [0] * x

    def get32bits(self):
        if self.index >= self.N:
            for kk in range(self.N):
                y = self.state[kk][:1] + self.state[(kk + 1) % self.N][1:]
                z = [ y[-1] if (self.A >> (31 - i)) & 1 else 0 for i in range(32) ]
                self.state[kk] = self._xor(self.state[(kk + self.M) % self.N], self._shiftr(y, 1))
                self.state[kk] = self._xor(self.state[kk], z)
            self.index = 0

        y = self.state[self.index]
        y = self._xor(y, self._shiftr(y, 11))
        y = self._xor(y, self._and(self._shiftl(y, 7), 0x9d2c5680))
        y = self._xor(y, self._and(self._shiftl(y, 15), 0xefc60000))
        y = self._xor(y, self._shiftr(y, 18))
        self.index += 1

        return y
    
    def getrandbits(self, bit):
        return self.get32bits()[:bit]

class Solver:
    def __init__(self):
        self.equations = []
        self.outputs = []
    
    def insert(self, equation, output):
        for eq, o in zip(self.equations, self.outputs):
            lsb = eq & -eq
            if equation & lsb:
                equation ^= eq
                output ^= o
        
        if equation == 0:
            return

        lsb = equation & -equation
        for i in range(len(self.equations)):
            if self.equations[i] & lsb:
                self.equations[i] ^= equation
                self.outputs[i] ^= output
    
        self.equations.append(equation)
        self.outputs.append(output)
    
    def solve(self):
        num = 0
        for i, eq in enumerate(self.equations):
            if self.outputs[i]:
                # Assume every free variable is 0
                num |= eq & -eq
        state = [ (num >> (32 * i)) & 0xFFFFFFFF for i in range(624) ]
        return state


from tqdm import trange
num = int(1337**1.337*1.337)
bit = 1
twister = Twister()
# outputs = [ random.getrandbits(bit) for _ in range(num) ]
equations = [ twister.getrandbits(bit) for _ in range(num)]
solver = Solver()
out = "00000000101111011001100010011101101010100001111011001100011001000110011001000110011100101111010111111110000000111011101001000000011111110110111010101111101111000000111110011000000011101110010000011100100110000110010100011000000100001001010100011011101111000010111101011000100000101010100011001110011011001111000111111011010101010101101110101110100111001100011101001011010000010010111101001011011001110100001110101011000001001110101100001101111100110110000110000101000111110100110011100101011011110110111111000011100101000110001110110000000111101101101100011000001000100101110001110110111010111000101100010010101110011111100001100101111000110000110000111111100001010110100111001011000001111101111001010011101110001010001010100111101111101011011000101001010010001011100011001101000001000000110110100001101101010100001011111000011010000101101101110111000100010011101111111011001110001010101000001001001100110010111000110001001101101100000001000111101010100111111001100111000001011001111010010101011011001100001110001111010000000110100110101100011111101101000001010110001110011110010001111000100000100010101110100111101010110000110000100010010001100111111100010110110110111111000110111101111111011010111000011111001001011000000001100111111010011110100000001111110010000001011000110100011101110110100111010000001101000010000101110001111001110001001011000110000000101011011111111100101011000110101110010100111000000000111011010100000101010100100001100001111011011100100100001110101111101101110010000111010000111001100111110111111110100001111110100101011000010010100011000000111111001101011010011101101010000010111111110100111100110000010100101000000010111100110110011101110000110010101110000101000111011111110001111101010101010011111000001101011011100011110011010010101100010111110011100000100010111101100101001111110010000010111100010100110110100110110101110001110111100000001001101111111000111110001101011110011101001101100110011001001011101100001001011000110100010011101010110110110010100010101011111110011001100011001100101101010000010100111010000100101101100000110011101001101100010000011100010000101011101100001000011110110011011110110100001100011101101010000001101101111100100011000110111100111111011111000110001110101110110111011110010111101011010000110100110000011001001101000011010001111011111111111101100000000101101010110000011111110010111111011011110011010110101001100111111011001101011001101111010011110001100101110000110010100111110011110011000011101000100011001111111001000110011000001111111101111111101001101111010011010110101111111000011010101011111011010001111001001100001010101100010001001010111110111101101101111100010101011111100010000101011111100111110111110110010111101001101001100000110111000100000000011001000000011111111001100101010110101111101100010110101110000011100101010101111010101111010011110110101100100001110011011110111101010100101010001000110110110011001101000111100110011000001100111110110100010111111100101101000110111001111011010011010001010010101000000100100111111010111100011011001010111111011010001000110000000001001001010001010011010010000111010101010011100010010111111100100111001000010100011100011011111101000000101101101111010110000110000000111011101011000110000101100010100101000001001100010101110011100111011110101010011001000000110101100001010000010011110111100111010000101000010000001000101100100001100100111000100010001001010000110111110010100001101100111011100000111110001001001100000101010100110110100011111011000111101000000001000011010011101000010000100001100011101001100001111100000100001110001100000101110010000011001000101100010111101000010000101110010010100000000100110111010111000011100110110010101000110011111000011110000100100101011011010000100111110000100011110000100000101010010100110111101001111101110110101010111010111111011101100100010101101010011110101011110110101001011000011111011101100101001101101010110010001100111010111010001010001010010101111101011011101001010010011101000011101001000001010001111010010011010111110011000010111111100000111110100101101000111001011101011101001110001000111100001101011110110010110011001001110110011110101101011010011100100010101111111111110100001110100000011110001101011110010000001111110100100111100111010110110011110011100000011110010110101000000011010011001110010001101010110100010001101010110011100001010000010111000101110110100101111111001010110010111000001100010000001000101010011100000101111110100110100000001011100100100000100011110110111111111101011111101000101001100110000111101101010101011011101011100010100010001011101010100111000111101001010011011100001101000010100010001000101001111010100101110011010101000100111110001101000000110100100010000011000101011100000111000110011010111101000000101111101101101111101011110111100011101000110100111110110010111011101010111000001011110101110000110010100111111001110010111100010101000010010001101110110001000011110111000100010101100101100011011001110110010001011111110001001010001101100001110110111110100011100111100110111111010010111101100010101010011101001010000000000001001100111110101010101100000110111111010100100110110010111010100110110001110100111101001101001101111110011100010100000001111111011000001101110011111001001001010100110001001010100111010011101001110010110000010100111001100100110011000111001100010101010100101100011111001101001110001001001111111111111101000000011101100100100001101010011010111011010110100100111000101110011111001011110001010100110010100111101101110100110001011100100100101001001110110110111011111100010011100101100000010001010010111111010011100011001010010000001101000000110000100111011010000101110000001000011101111100101011000011111001000100101101101001011000001011000111000000100000110111000010011100110101111111000000001100111101010000011001011100011010100101111000011011111101000000111011110101000101000110001100001000110010110010101010001010100011000001011001010010011011011111100111010110011111101110000111000001000010010011101011000000100010110101110111110110100110011011010010001010110111010000101101001111011101111111011110100101100001110001101101101001010000101011110000010111101100000000000111000011111011011101000001010010101111010100101011101101011000110000001101011001011100011111011101100111100111100001100001000111001101011001110010010010100101100111011101110010100111110011010010110110000001111110110111011011001101000101011000100101110101011101100111010100101101001011000101100010100101011011100111101011101001101000100000110010011110001010110101011100110010011101010001010000110000111111000000101001110001000010011100000001010100100111010010101000110000100010110010100001100110011000000011110100010100011101111010000001111110111110110011010000001010011001111010000001011111110110100011010101110000000101100010011011000110001100100000001110100011010011011111100001110010011110101100100011101000110010101101111001011000010000000110010010000001110111000010010010101110000110001001001001101010001011110101000000010111001000110000001001111101100101000100010001010111100011100111111101101111101100010001110101110010100011011000101001110111010000000010110100110101111100001110110101000111000000000010101101101100011011001100000011000111001110100011111011011011111111111000111110110101110111100110001001101011101010110110100101010001111100010010100000000111111010110010011111000110000001100010000110011001100100101000111110101100010101011010010000100011001001011101011001100111001101001110011110111011000111111011000001111100110100110010010010101110110010110000101001101101110110101110010111101000000011110011110110101000110011011110111100011101111000010000001111110001011111010010101100100100010010110110100110010000000010111000111111110111010111010100001111110100110010101000010100011100100000111100110111010100000110101110101011111110110100011010001101000100111110111010011011001001001011010010100000011110000011000110010000100101100001100111111110001100101010000001100101101110100101101001111000101011010111111011011000000001011001110011101111100111010010001010001011010110100011101111111110000110010111110010011011000011110001111100001010100000110111010001011011110101111010010000000100001010100110100000010011100111110110001000011101001110100101010100101100001001111001011110000111011011001011011101101100111001011100101101010010001111110011101110010011101010101101001011001011000110010010010001010111010110100010111011010100010101010011111100100101011100001100010111110110000111101110010001010010000101100000101001110001111010011000100001010001010101110000101101100111111001111000101110001111000011001011110101110111110011011011101000110100000001001111010001000111000101000010010001000001100011111101001011011000000001111101111001101111100110101000100110100111001011101001000111010111110011110101010000001011110010011110110111001111110000011110011001110111001010010100011010010110110011010010000010100000000011110110011011101010111000011001000001011101100011011000100110100110001011100100111111100111111100001011000000001101011100100000001011010001101101000100110010011111010100001011111110000011000000001110000110111011011100101001110001101011000101111110101001101110110011000101010001110000000001010111000010011101000010000100111101100001010011011011100011000001010101001100010010001100111110101101000000010100000010110111010010011000100011100101100101000001000100000101000111000000010100000110111110010110011000001111011000001000000101010111000000100110101100111111001010110001101111111000111011011001010101001110011111110011000101001100001001101001011111101011101001100111011111101111100000010101000111110011000100100001100001101010010110101011000000011101111011100111111010010100011111110011111100010001101010101001110010110100011010001111110011001010011001110010110011111011101010011000101101000100110000101011111000100100000100000010111110101101100101000001010011111011100100011100011111011001011101101001111100100001100101011010110011111001100111111001111001100100010011010110100001100100100001000010010011111010101011101101011111010010011000011111000110010011111000100000011000011111111000011111011111010111111110101011010011010011000101011100000110101011010100101011001010100100010110001100011100100111010100100001101001110110101001011110001000011111001111110101101100111111111000100101100100100111111101011000100101100010010011000101000011100001011101111101000011010011010111010000111100110100110110000110101101111110111110001111110010111110010010110111011101110010011011010000001101110100101010101011000111100011111001001110101000111001110001000110000010010101110001011000010110010110010011011000100110110000001010010111010101110110110111110111010101110011010101000110001101100111010111011110100011010000011010100010010101000101010110110100001011101101010010110010100100110101100000101001000111111110111000011101111101000011010000000111000011100110101110011011100100101110001111101010111011001000011100011111010100100000100100101001010110111111000010111110111111010000101001010100011110010100100110110001011001101010010100100010010001110101010110000111111110010011000011000111001001001011101100111111101100011111100011000001011111001011100010101000110011010110001000010010101000001010011001001011011011110110000110011111010011010010011001000011100111111001010110100101010101011111011000110000100110111100110000011110010100100000000110001110010110101000010101000010101101010110100100001011100001100101110111011010100011010011011110101010010001110001010001000100101001000110110011011101101110011110010010000100111000101010010001010000001010111000000011010101101100001010100010101000001011011110111100111110101100011010000110001110111001001110011010001110010101010000101011011100100010110001000101001010100010100111010011110100111011100000001010101100000110010110011110001111011100110001100110010010100010000010000010001100101000001110111011010000110011100111110110000010101101001011101111100111011010111110001100101101110010101000000111011011110100010100001010111011110100110111101110110110101101100001000000000101000101011010101010111000100011111001001011000111010001101111001101010001101100010101111001100110100001100011001100011010011011010010000100001011101111110001110000011010011111111100101111111010010101111001100001110010110100101101010100011001000110001001010100110110111000011100010010100001001001100000011011001000011110110101110101111101101010100000011100101111000001100110001010001111001011110011010000110011101011111111111101000001110000100011000010100110001100111011001001101101000011110111101110001101000000110100010001110110111110110010000100010110011100100111110110100010001101011110111110100001111111101010010100111110000111101000111110100100001111111100010000000101001000100000010101100110011100011010010011010100001100110001101011011001111100001010111001111000000101011001011111111101110110011101101111100010100001111010100101111111100011010111010101111001010000011101011110011001111110101101100101011011001011110001000011010101101001101111011011001101100100111100001101110011000111000110110011110100011110011000000101001110110101011100110001011000111111001011111110001101000011010110110011011011111100011111111011000001010100111011101001001001000000001111101100111000001111010110011001000000111000101101100110111110111100000111010111111010010110001010101001011101111010011011111000110100011000011110001111101010101000001110100100110011011111010011111101110100011111010101010010010101011101000111110110111110111011111110010011000101000110000100111100110010110011101111100010010001000110000111001100100000010101100011100010111011010100100101001000110001100110010011000000111001010110000111110111000100101100111101001011111001010011001001011001000010111011011110011100001101101001001010111111100010001000011011111111101000111010100001010101101110111111011100001100110110101001010101101010111011011101110110011101111000101001000110111100000101110101011010110110110110000010011100000110010110101100001101100110100011111111000101100010100110010101010100101110010111010110000110001110101001000110101110011100000110100011110100100001100101110011111100111011100011011000110000101011000000001000001000001001110100111010100001101010100011000011011100110100010111110000010000111100111001000001010110100100110100010011111010001011011101110100100001001000101110101001100000100101001100010111111110110110001000110001011110001001111010100101110101110110111001110101111100000100000100011000001110011101100001001011000000100010100101111010101100110101111101111110110011111011000010101010011100100010001111001101101100011010110010010111111101111011010100100111100101000001110110111001111001110101011011111010100000000001100010110000000010100100001100100111000111101100001110110101110100010100000110011110001001101010011000110101010010011010001001011101111000100101010110100010110111100001001011000001110101011111000001011011101101000011110011110100001000101000101100101101000011100011111011011110100111010100001110011011001101011000001011001001111010101011000111001101010000011111100001000101011100111110001101101011011101100010100111010110101111111001001000011010111011011000010100010110110000110001100111111000010110010000010111001010010000010100101100000001000000101000001110101111111100111001001110111110010110010111011000101101101011101001011111011011000110111100111010101111001101101000010101111010010010111100110101011000110000111010100001010100000010011110000100100111101011110000010110100111010011100001001000101001010001101001101010010101101101011111001011100110001000010110001011001110000110001110011000010111100100111011001100010101110100001000100101001010000011001111100100011010111111111000100111011110110111000001110100111101001111100110001000101011100010000110111101100010111011101010100111000101111010111000101000000111011000100110110010000110111111000100111010100001010101000111010111011001110000010100010011111101000110001101100110011110101001001001001011111001010000011011010001111101101101000110000010101000111011011111010010001101011011011000001100111011000111111011111111000011110000010110011111001101001010100100010110111010110111111101101100101000001010011101101010100100111001000010100001001010111110011111111100100101001100010000100111101100000001010101001110100000010110010111100011000110110100101110001110001100011100110111100001000101010111101000101001010010010110000100010110110010010010110001000110011000000100111000000001010000110100001101000010001010100000010110010001111101011010001011010000100000101001110010001111110001001010010111010100110111110101100101000000111001000110110010111100110111001101101001111110001011010011101010010110101111101111001010001010110110010000101111111001101111101011001000000101101110100110110110100000011111101011100100101100000110101010010101010111101001001011001001010001100111110011101001110001011000100111111010010111101011001001000001011001010000001111100100101001111011000000001010110111110101000101010000001111111001100011001010101100010011101000111010101100111100001001101010000010011001101101011110101010010110111010000101010100110111000110001101101000010000011111000100001110111000101000101000010000000110111100110101111100101100110111001101011001111110101001001000000101010011011010101101100000000010110001101001110011011111001111110011110010101111111000001011101011101111001110110101010010111100110111001010111101000110001001001011100100011000100000101011001000100111000001100000001101110010101011100000101010011010101111000100011110011110100111010011101011000110111001000000110000100110101001111000101001000000101010010010001101101011110101000111010100000000001010110101000000010111001100111101010001000011010001101111111010000001011111000101000010111001111101111111110100011010100001011000010101101001100000000001101010110001101001011100110010010101001000110000011001111000010000011110100001010001000110010110100100000101101110000100110011000101100100111011000010011111101111011011001101101110100010100001010101001011001111101111101101001110111100111111010001000010101001001101100000011011111100000011001100100001001100010011011010011101101101010001110001001101110000110110111001101100110011000110100100110011101000101001000111000001011100101110001000100001100000010110010000111110010110111000110010101001000010110000000110101100010100001100101000100011100110101110000111000010110110100010000111001101001010011010001111011000011001100101000011111010111010111100001111010001011101000010100111001100101100111010100011111011010010101101100110101011111100111001110101110011101011011000011110001000000110000100011000101101100111110100101111110010011100011101001101111000000110011100111101011010101000011100011110001101000001011100111110001001010010001110000111010111010001101010011101101010001100101011110101101101101000000110111111001010111101110100101000001011101111000010010111010110100000011101101000001111010001011110000001110011010110101110000010100111111011100101100001110000110111010001001110011111111110000010000011110010110101001111111001110110001011010001011000001110001010000100111011001101111010110000011011111101101100110001010011001111110110110000010000001000010110110110010001110001011101111100000100000111010001111010101101011010010000001110111011111011100100111101000011010010100011110111111111111100010100011101101001000011010000100000100101111111010101011100001010010010000010101100010110000110011010000000010101111010111000000000001001110011111010000101110110111001011111010011100000111101010010110100111101111000011100000000111100101111011110011110001100010011110110110011011100011110011110011000111011111100101111100100010111000000110100111100101111001110101001000011111010110101100111001110011111010110001100100000111111001101110000110000000000100000100100001101101001011100110111111001000001000111010000010100000000101111100000100111111000111101100011000100000101000100101100000100101001010010100100011000110100110011001101010111110110101010011011001100111100110101000100100101110110011001101001110100110011110101000111111111010010010110000011001111111000101110001100111111010010101000001000011101000011010000111010110010100000001001011110111101010010111000111100001110100010010101001100101110110111111100011001000000101011000101111001101100110111011100011100100000001100011100111101001010110100100001111001000011011000100101000001010000010110001100111010100100010010110110111111101001000000001101100"
for i in trange(num):
    solver.insert(equations[i][0], int(out[i]))

state = solver.solve()
recovered_state = (3, tuple(state + [0]), None)
random.setstate(recovered_state)
print(recovered_state)
# state = (3, (0, 4105789988, 2067591534, 2432402800, 1433881788, 3003124887, 1495199749, 984335047, 547862992, 1620362539, 2319963362, 2503999060, 2577833387, 3085279240, 114339416, 3472849231, 716465497, 3100925111, 1531881806, 4238598057, 3618195854, 3591989825, 105677198, 298928123, 3751036512, 119244537, 1518968726, 722465279, 3596941776, 3774769659, 3898511397, 1285558913, 751089842, 3985096120, 2058640983, 2559207619, 1554664638, 750231873, 4090305221, 771516336, 1277265304, 3751627889, 3150013619, 1277974136, 1415705662, 189770590, 3818215044, 1304440841, 1660286548, 2907635430, 115261396, 3150259341, 3687104454, 1061386245, 1671413543, 2466543233, 122897383, 2396113571, 3617161978, 3259867688, 2327605124, 1244702447, 2818625743, 243997131, 1247921812, 4147580939, 1986345085, 590332311, 200465741, 1270944412, 1781408327, 2841115703, 2306950959, 1326820268, 660861642, 1151247748, 1791733079, 2502162905, 3289173354, 1930247131, 1624168709, 2677468227, 2589679657, 2279565241, 691317876, 3581952291, 2509322642, 1938528549, 427890173, 510397650, 2094950364, 2253545286, 2281838199, 2186846142, 2897623700, 1206442494, 1403545543, 3264778457, 4096137485, 1368542590, 468546664, 3175649264, 1049532107, 3566583184, 532824081, 3441120247, 337384806, 305171162, 3699566574, 2898010962, 1694051187, 363125370, 3975878675, 1761302102, 2149867823, 1104451694, 2877469118, 829795533, 1308089070, 3334437478, 1455040021, 3350934173, 1829959861, 2336557134, 777225410, 2575283344, 2702312652, 4079519746, 2814810987, 3702757010, 2504370789, 3013078342, 4189733797, 2824469765, 4112719081, 651508064, 3153045939, 2315731645, 3492347661, 1305273427, 1132462562, 3477273211, 1676060314, 835566660, 3096295714, 2200990729, 529514343, 1250415862, 63190046, 805938067, 811806385, 3169574177, 2473549477, 2425859370, 2790453957, 416844822, 871641356, 2573881572, 3394910391, 3856451555, 2809845697, 3032030011, 3187684230, 3042877608, 1316011489, 120605308, 1998471367, 2817367133, 4078110888, 3090054487, 2550725984, 1904000358, 4214813430, 352707580, 2603572685, 2663525362, 3378477703, 3802618596, 2417611433, 1067844862, 1470942005, 2039730967, 1645188080, 2278603158, 1707648031, 70476484, 2733429161, 268892346, 3923623743, 1869467816, 3070247121, 2491792332, 1478861924, 2394425102, 1422418463, 912632610, 2555712405, 949365163, 138218426, 1535691606, 3442388084, 3827556973, 2340377546, 2724480239, 910248640, 573359166, 1425073581, 4066331030, 1502758826, 3651675665, 527117737, 1760895042, 1550146593, 273414177, 3593695378, 4180461967, 1780687992, 4261992670, 3991908742, 1053857060, 3242178769, 369046495, 3142419764, 1363772701, 4048081969, 3774323319, 341842977, 945032421, 1993882967, 2858074001, 96810303, 989691594, 2456992510, 1379446363, 965915142, 2124080283, 4253529648, 1321992587, 4292998495, 3147842259, 2086503724, 2575778271, 1552786361, 3718049205, 3849936855, 967056442, 4285969027, 2566603199, 2214441425, 801009799, 991252266, 1861282828, 2199494470, 757272870, 756737134, 465581557, 4151629387, 3567855099, 3601890657, 1196011973, 1379778467, 2143897127, 1190655114, 2321008015, 110514200, 3958404014, 239702121, 854677999, 1070441860, 2331008741, 570283571, 170884152, 557975185, 3147767611, 2911488364, 3723067959, 3451109703, 1905599538, 4178071621, 3786037856, 526857901, 3929191976, 1261797932, 3623652736, 3393661082, 2568172821, 1426397998, 864812920, 4103243150, 525326124, 3617621711, 287117497, 1908468563, 3052604065, 862736164, 255630558, 3809349974, 2545627768, 4115508706, 865695813, 1535096004, 2534516883, 1186921415, 2384229689, 1253486662, 2021320229, 1389964746, 4190248527, 880280112, 1850826025, 1647088500, 2905883009, 425324314, 1259422001, 3353738620, 3184156186, 2268193758, 536127506, 1916525021, 1684741010, 1749501578, 202259276, 160225615, 2505815205, 3851056852, 4166350006, 1415203975, 1657116296, 3651000651, 3645030349, 1391094999, 3246228032, 848268091, 3789072779, 645605620, 3006203579, 263418293, 1078749835, 663411076, 388752538, 4090042559, 878932466, 1579716270, 848079794, 3805987987, 2480287254, 2293386910, 964418862, 174373917, 547559185, 3502313357, 3371223352, 2874281982, 1065068462, 3048631420, 104728535, 2902352142, 2511967253, 2426716438, 1793335076, 3409129847, 3243625393, 3161467187, 2987902173, 2056189239, 1537669591, 2791492834, 4010169773, 2085046148, 611826913, 2329043999, 3444297466, 3942306059, 3196111214, 2186667688, 119978682, 1441499139, 561972125, 881937966, 2002715140, 2451752101, 2374941825, 289851086, 249698079, 1545065499, 1745809095, 753263612, 204465415, 4198094834, 2868666650, 1204698671, 772683217, 1385871115, 1235160716, 303023112, 1760781780, 4147267522, 3408412739, 2934791156, 1110703618, 3472654945, 1729628227, 3267967648, 461026103, 1896448384, 588245927, 625638852, 421090606, 2614767084, 1042937102, 3482212990, 3369091170, 289045130, 1895348359, 4121154101, 248445160, 4157368174, 1989081397, 2365220591, 2665937082, 3933525465, 2585736521, 3989430748, 1435181224, 762291554, 1625259426, 1302846132, 737037456, 2035268883, 1923225678, 21674646, 3746177995, 922991566, 3628381727, 3697068048, 1035900410, 2598210815, 2075507559, 653301610, 437045042, 3901725058, 3886013162, 3594954986, 1179738091, 4042857752, 3981514714, 1870349719, 4064998966, 3555637952, 1472070909, 1906059173, 4218676849, 3901004608, 2456246273, 4260965906, 1697558184, 1491222780, 2369756485, 2483766583, 63931416, 3456825531, 1731646699, 2360265228, 4019753736, 3454617757, 641531034, 1038246617, 3378956260, 748450241, 1376727208, 3561771840, 3681085834, 2296018536, 1349909281, 2229885807, 801923397, 1956747583, 4099816471, 362760569, 1546725325, 1084426707, 1130162054, 2020364847, 1771089913, 274473022, 1804034190, 404449570, 1600214965, 300094536, 3710651896, 1061893042, 2727724276, 937491582, 1436478667, 4250178879, 3315532740, 1676215165, 2239482349, 168995494, 4108672866, 3669720109, 12839398, 2121166717, 928262555, 4130529543, 2313301983, 3292913087, 3341444638, 761292692, 3839444310, 897192773, 865082327, 1764997964, 1008935761, 642526567, 1185122336, 3312068013, 3143524457, 795628675, 1907433167, 1459722402, 1187491358, 2399797873, 3000182761, 3986901562, 3713135144, 350995268, 4022259078, 187419681, 1989548312, 1378866138, 1698454578, 3136172403, 2788422833, 373093553, 3727047934, 2984705754, 4200790360, 672115284, 2320992050, 306906876, 2556407580, 1372241020, 1515521357, 1466347022, 1228529466, 426380086, 715695443, 4062226718, 1048421952, 2857598327, 1423542059, 1300814240, 3141909693, 3677223531, 2241803262, 1132254070, 3938493189, 3648369175, 2317784221, 2130383931, 242438180, 4155101118, 1913287060, 368528257, 289757747, 3137643972, 2646856874, 871087832, 541933880, 3334074036, 1947050477, 2681527534, 2539368124, 1543855068, 3233481252, 2105281155, 3831270343, 2380685531, 2271041690, 962639125, 1361345162, 4185966738, 562401006, 3700402638, 2823766012, 2058110897, 2941494311, 3061119005, 1940483462, 2310018383, 3412465755, 322329080, 63307277, 299877164, 3500635689, 2026828896, 1223287729, 3718051052, 158066441, 1629183052, 1129169396, 13953419, 630499087, 3883544247, 2567923959, 1903470044, 3964705285, 4292398747, 1064567123, 3786641399, 1734227856, 4181466708, 1372149418, 1815842159, 3985667302, 3006098018, 2364798451, 2969338269, 3297142513, 4077061429, 1390862857, 1837035173, 3636607464, 0), None)