

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_96446191626393604009054111437713980755082681332020571709789032122186639773874753631630024642568257679734714430483780317122960230235124140242511126339536047435591010087751700582288534654352742251068909342986464462021206713195415006300821397979265537607226612724482984235104418995222711966835565604156795231519 = Integer(96446191626393604009054111437713980755082681332020571709789032122186639773874753631630024642568257679734714430483780317122960230235124140242511126339536047435591010087751700582288534654352742251068909342986464462021206713195415006300821397979265537607226612724482984235104418995222711966835565604156795231519); _sage_const_21859725745573183363159471 = Integer(21859725745573183363159471); _sage_const_5170537512721293911585823686902506016823042591640808668431139 = Integer(5170537512721293911585823686902506016823042591640808668431139); _sage_const_2408746727412251844978232811750068549680507130361329347219033 = Integer(2408746727412251844978232811750068549680507130361329347219033); _sage_const_22853109242583772933543238072263595310890230858387007784810842667331395014960179858797539466440641309211418058958036988227478000761691182791858340813236991362094115499207490244816520864518250964829219489326391061014660200164748055767774506872271950966288147838511905213624426774660425957155313284952800718636 = Integer(22853109242583772933543238072263595310890230858387007784810842667331395014960179858797539466440641309211418058958036988227478000761691182791858340813236991362094115499207490244816520864518250964829219489326391061014660200164748055767774506872271950966288147838511905213624426774660425957155313284952800718636); _sage_const_5 = Integer(5); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_4 = Integer(4); _sage_const_204 = Integer(204); _sage_const_512 = Integer(512); _sage_const_20 = Integer(20); _sage_const_10 = Integer(10)
from Crypto.Util.number import *
import itertools
N = _sage_const_96446191626393604009054111437713980755082681332020571709789032122186639773874753631630024642568257679734714430483780317122960230235124140242511126339536047435591010087751700582288534654352742251068909342986464462021206713195415006300821397979265537607226612724482984235104418995222711966835565604156795231519 
e = _sage_const_21859725745573183363159471 
l_dp = _sage_const_5170537512721293911585823686902506016823042591640808668431139 
l_dq = _sage_const_2408746727412251844978232811750068549680507130361329347219033 
ct = _sage_const_22853109242583772933543238072263595310890230858387007784810842667331395014960179858797539466440641309211418058958036988227478000761691182791858340813236991362094115499207490244816520864518250964829219489326391061014660200164748055767774506872271950966288147838511905213624426774660425957155313284952800718636 
given = int(N).bit_length()//_sage_const_5 
def bivariate_small_roots(f, bounds, m=_sage_const_1 , d=None):
	if not d:
		d = f.degree()

	R = f.base_ring()
	N = R.cardinality()
	
	# f /= f.coefficients().pop(0)
	f = f.change_ring(ZZ)

	G = Sequence([], f.parent())
	for i in range(m+_sage_const_1 ):
		base = N**(m-i) * f**i
		for shifts in itertools.product(range(d), repeat=f.nvariables()):
			g = base * prod(map(power, f.variables(), shifts))
			G.append(g)

	B, monomials = G.coefficient_matrix()
	monomials = vector(monomials)

	factors = [monomial(*bounds) for monomial in monomials]
	for i, factor in enumerate(factors):
		B.rescale_col(i, factor)

	B = B.dense_matrix().LLL()

	B = B.change_ring(QQ)
	for i, factor in enumerate(factors):
		B.rescale_col(i, _sage_const_1 /factor)

	H = Sequence([], f.parent().change_ring(QQ))
	for h in filter(None, B*monomials):
		H.append(h)
		I = H.ideal()
		if I.dimension() == -_sage_const_1 :
			H.pop()
		elif I.dimension() == _sage_const_0 :
			roots = []
			for root in I.variety(ring=ZZ):
				root = tuple(R(root[var]) for var in f.variables())
				roots.append(root)
			return roots

	return []

def solve(f, X, m, t): 
    F = []
    S = []
    for j in range(m+_sage_const_1 ):
        h = f**j*k**(m-j)*N**(max(_sage_const_0 ,t-j))
        F.append(h)
        S.append(x**j)
    MAT = Matrix(ZZ, len(F))
    for i in range(len(F)):
        f = F[i]
        f = f(x*X)
        coeffs = (f.coefficients())
        for j in range(len(coeffs), len(F)):
            coeffs.append(_sage_const_0 )
        coeffs = vector(coeffs)
        MAT[i] = coeffs
    MAT = MAT.LLL()
    ret = []
    for j in range(len(F)):
        f = _sage_const_0 
        for i in range(len(S)):
            f += MAT[j,i]//S[i](X)*S[i]
            roots = f.roots()
            if roots != []:
                ret.append(roots[_sage_const_0 ][_sage_const_0 ])
        return ret


def find_k_l(given, e, l_dp, l_dq, N):
	P = PolynomialRing(Zmod(_sage_const_2 **given * e),_sage_const_2 , names=('x', 'y',)); (x, y,) = P._first_ngens(2)
	A = -e**_sage_const_2  * l_dq * l_dp + e*l_dp + e*l_dq - _sage_const_1 
	f = (N-_sage_const_1 )*x*y - (e*l_dq - _sage_const_1 )*x - (e*l_dp - _sage_const_1 )*y + A 
	bound = (e,e)
	r = bivariate_small_roots(f,bound,_sage_const_3 ,_sage_const_4 )[_sage_const_0 ]
	k,l = r
	return int(k)


k = find_k_l(given, e, l_dp, l_dq, N)
R = QQ['x']; (x,) = R._first_ngens(1)
a = QQ((e*l_dp + k - _sage_const_1 ) * pow(e*_sage_const_2 **_sage_const_204 ,-_sage_const_1 ,k*N))
f = x + a

for h_dp in solve(f, X=_sage_const_2 **(_sage_const_512 -_sage_const_204 ), m=_sage_const_20 , t=_sage_const_10 ):
    p = gcd(int(f(x=h_dp)), N)
    if is_prime(p):
        q = N//p
        d = pow(e, -_sage_const_1 , (p-_sage_const_1 )*(q-_sage_const_1 ))
        flag = int(pow(ct, d, N))
        print(long_to_bytes(flag))
        break

