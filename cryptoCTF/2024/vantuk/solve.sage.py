

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_6080057478320734754578252336954411086329731226445881868123716230995225973869803901199434606333357820515656618869146654158788168766842914410452961599054518002813068771365518772891986864276289860125347726759503163130747954047189098354503529975642910040243893426023284760560550058749486622149336255123273699589 = Integer(6080057478320734754578252336954411086329731226445881868123716230995225973869803901199434606333357820515656618869146654158788168766842914410452961599054518002813068771365518772891986864276289860125347726759503163130747954047189098354503529975642910040243893426023284760560550058749486622149336255123273699589); _sage_const_10166660077500992696786674322778747305573988490459101951030888617339232488971703619809763229396514541455656973227690713112602531083990085142454453827397614 = Integer(10166660077500992696786674322778747305573988490459101951030888617339232488971703619809763229396514541455656973227690713112602531083990085142454453827397614); _sage_const_3225614773582213369706292127090052479554140270383744354251548034114969532022146352828696162628127070196943244336606099417210627640399143341122777407316956319347428454301338989662689983156270502206905873768685192940264891098471650041034871787036353839986435 = Integer(3225614773582213369706292127090052479554140270383744354251548034114969532022146352828696162628127070196943244336606099417210627640399143341122777407316956319347428454301338989662689983156270502206905873768685192940264891098471650041034871787036353839986435); _sage_const_9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609 = Integer(9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609); _sage_const_1971582892158351181843851788527088806814104010680626247728311504906886858748378948163011806974145871263749452213375101951129675358232283650086419295655854343862361076089682606804214329522917382524296561295274823374483828323983651110722084223144007926678084087 = Integer(1971582892158351181843851788527088806814104010680626247728311504906886858748378948163011806974145871263749452213375101951129675358232283650086419295655854343862361076089682606804214329522917382524296561295274823374483828323983651110722084223144007926678084087); _sage_const_1 = Integer(1); _sage_const_17 = Integer(17); _sage_const_3 = Integer(3); _sage_const_2 = Integer(2)
A = Rational(_sage_const_6080057478320734754578252336954411086329731226445881868123716230995225973869803901199434606333357820515656618869146654158788168766842914410452961599054518002813068771365518772891986864276289860125347726759503163130747954047189098354503529975642910040243893426023284760560550058749486622149336255123273699589 /_sage_const_10166660077500992696786674322778747305573988490459101951030888617339232488971703619809763229396514541455656973227690713112602531083990085142454453827397614 )
U = Rational(_sage_const_3225614773582213369706292127090052479554140270383744354251548034114969532022146352828696162628127070196943244336606099417210627640399143341122777407316956319347428454301338989662689983156270502206905873768685192940264891098471650041034871787036353839986435 /_sage_const_9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609 )
V = Rational(_sage_const_1971582892158351181843851788527088806814104010680626247728311504906886858748378948163011806974145871263749452213375101951129675358232283650086419295655854343862361076089682606804214329522917382524296561295274823374483828323983651110722084223144007926678084087 /_sage_const_9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609 )

P = PolynomialRing(QQ, 'a')
a = P.gen() 
f = a + (_sage_const_1 /(_sage_const_17 *a)) - A
f = f.numerator()
root = f.roots()

for r, _ in root:
	if r.is_integer():
		a = r 

D1 = _sage_const_10166660077500992696786674322778747305573988490459101951030888617339232488971703619809763229396514541455656973227690713112602531083990085142454453827397614 
N1 = _sage_const_6080057478320734754578252336954411086329731226445881868123716230995225973869803901199434606333357820515656618869146654158788168766842914410452961599054518002813068771365518772891986864276289860125347726759503163130747954047189098354503529975642910040243893426023284760560550058749486622149336255123273699589 

N2 = _sage_const_3225614773582213369706292127090052479554140270383744354251548034114969532022146352828696162628127070196943244336606099417210627640399143341122777407316956319347428454301338989662689983156270502206905873768685192940264891098471650041034871787036353839986435 
D2 = _sage_const_9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609 

N3 = _sage_const_1971582892158351181843851788527088806814104010680626247728311504906886858748378948163011806974145871263749452213375101951129675358232283650086419295655854343862361076089682606804214329522917382524296561295274823374483828323983651110722084223144007926678084087 
D3 = _sage_const_9195042623204647899565271327907071916397082689301388805795886223781949921278129819112624089473306486581983153439866384171645444456400131619437018878598534536108398238424609 

Q, (x, y) = QQ['x', 'y'].objgens()

Q2 = a * D2 
Q3 = a * D3

I1 = Q.ideal([
    D2 * x ** _sage_const_3  + D2 * x * y * y + Q2 * x - D2 * y - N2 * x * x - N2 * y * y, 
    D3 * y ** _sage_const_3  + D3 * x * x * y - Q3 * y - D3 * x - N3 * x * x - N3 * y * y
])

for root in I1.variety():
	x, y = int(root['x']), int(root['y'])
	try:
		print(bytes.fromhex(hex(x)[_sage_const_2 :]), end='')
		print(bytes.fromhex(hex(y)[_sage_const_2 :]))
	except:
		pass
# from Crypto.Util.number import *

# print(long_to_bytes(350799328046836724707876331502758499088281144928479088116262376685681093677946249551), end="")
# print(long_to_bytes(214418026424679791626535920403147011577793961208832046224896849702981130286017264892462), end="")
