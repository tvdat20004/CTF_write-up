

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_13588728652719624755959883276683763133718032506385075564663911572182122683301137849695983901955409352570565954387309667773401321714456342417045969608223003274884588192404087467681912193490842964059556524020070120310323930195454952260589778875740130941386109889075203869687321923491643408665507068588775784988078288075734265698139186318796736818313573197531378070122258446846208696332202140441601055183195303569747035132295102566133393090514109468599210157777972423137199252708312341156832737997619441957665736148319038440282486060886586224131974679312528053652031230440066166198113855072834035367567388441662394921517 = Integer(13588728652719624755959883276683763133718032506385075564663911572182122683301137849695983901955409352570565954387309667773401321714456342417045969608223003274884588192404087467681912193490842964059556524020070120310323930195454952260589778875740130941386109889075203869687321923491643408665507068588775784988078288075734265698139186318796736818313573197531378070122258446846208696332202140441601055183195303569747035132295102566133393090514109468599210157777972423137199252708312341156832737997619441957665736148319038440282486060886586224131974679312528053652031230440066166198113855072834035367567388441662394921517); _sage_const_7060838742565811829053558838657804279560845154018091084158194272242803343929257245220709122923033772911542382343773476464462744720309804214665483545776864536554160598105614284148492704321209780195710704395654076907393829026429576058565918764797151566768444714762765178980092544794628672937881382544636805227077720169176946129920142293086900071813356620614543192022828873063643117868270870962617888384354361974190741650616048081060091900625145189833527870538922263654770794491259583457490475874562534779132633901804342550348074225239826562480855270209799871618945586788242205776542517623475113537574232969491066289349 = Integer(7060838742565811829053558838657804279560845154018091084158194272242803343929257245220709122923033772911542382343773476464462744720309804214665483545776864536554160598105614284148492704321209780195710704395654076907393829026429576058565918764797151566768444714762765178980092544794628672937881382544636805227077720169176946129920142293086900071813356620614543192022828873063643117868270870962617888384354361974190741650616048081060091900625145189833527870538922263654770794491259583457490475874562534779132633901804342550348074225239826562480855270209799871618945586788242205776542517623475113537574232969491066289349); _sage_const_914008410449727213564879221428424249291351166169082040257173225209300987827116859791069006794049057028194309080727806930559540622366140212043574 = Integer(914008410449727213564879221428424249291351166169082040257173225209300987827116859791069006794049057028194309080727806930559540622366140212043574); _sage_const_233711553660002890828408402929574055694919789676036615130193612611783600781851865414087175789069599573385415793271613481055557735270487304894489126945877209821010875514064660591650207399293638328583774864637538897214896592130226433845320032466980448406433179399820207629371214346685408858 = Integer(233711553660002890828408402929574055694919789676036615130193612611783600781851865414087175789069599573385415793271613481055557735270487304894489126945877209821010875514064660591650207399293638328583774864637538897214896592130226433845320032466980448406433179399820207629371214346685408858); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_955 = Integer(955); _sage_const_545 = Integer(545); _sage_const_1024 = Integer(1024); _sage_const_7 = Integer(7); _sage_const_65537 = Integer(65537)
from sage.all import *  
n = _sage_const_13588728652719624755959883276683763133718032506385075564663911572182122683301137849695983901955409352570565954387309667773401321714456342417045969608223003274884588192404087467681912193490842964059556524020070120310323930195454952260589778875740130941386109889075203869687321923491643408665507068588775784988078288075734265698139186318796736818313573197531378070122258446846208696332202140441601055183195303569747035132295102566133393090514109468599210157777972423137199252708312341156832737997619441957665736148319038440282486060886586224131974679312528053652031230440066166198113855072834035367567388441662394921517 
c = _sage_const_7060838742565811829053558838657804279560845154018091084158194272242803343929257245220709122923033772911542382343773476464462744720309804214665483545776864536554160598105614284148492704321209780195710704395654076907393829026429576058565918764797151566768444714762765178980092544794628672937881382544636805227077720169176946129920142293086900071813356620614543192022828873063643117868270870962617888384354361974190741650616048081060091900625145189833527870538922263654770794491259583457490475874562534779132633901804342550348074225239826562480855270209799871618945586788242205776542517623475113537574232969491066289349 
p_msb = _sage_const_914008410449727213564879221428424249291351166169082040257173225209300987827116859791069006794049057028194309080727806930559540622366140212043574 
qp_lsb = _sage_const_233711553660002890828408402929574055694919789676036615130193612611783600781851865414087175789069599573385415793271613481055557735270487304894489126945877209821010875514064660591650207399293638328583774864637538897214896592130226433845320032466980448406433179399820207629371214346685408858 

import itertools

def small_roots(f, bounds, m=_sage_const_1 , d=None):
	if not d:
		d = f.degree()

	if isinstance(f, Polynomial):
		x, = polygens(f.base_ring(), f.variable_name(), _sage_const_1 )
		f = f(x)

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
P = PolynomialRing(Zmod(n**_sage_const_2 ), names=('x', 'y',)); (x, y,) = P._first_ngens(2)
f = n*(_sage_const_2 **_sage_const_955  *x + qp_lsb) - (_sage_const_2 **_sage_const_545  * p_msb + y)
# for m in range(10):
# 	for d in range(10): 
# 		print(f'{m = }')
# 		print(f'{d = }')
# 		r = small_roots(f, (2**(1024-955), 2**545),m=m, d=d)
# 		print(r)

root = small_roots(f, (_sage_const_2 **(_sage_const_1024 -_sage_const_955 ), _sage_const_2 **_sage_const_545 ),m=_sage_const_2 , d=_sage_const_7 )
print(root)

x,y = root[_sage_const_0 ]
p = _sage_const_2 **_sage_const_545 *p_msb + y 
assert is_prime(p) and n%p == _sage_const_0 
q = int(n)//int(p)
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(int(pow(c,pow(_sage_const_65537 ,-_sage_const_1 ,(p-_sage_const_1 )*(q-_sage_const_1 )),n)))) 
