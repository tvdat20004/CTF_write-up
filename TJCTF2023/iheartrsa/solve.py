m = 158074867710147204008831922538780335128399235943762939972254445049226666929140704494407469959477675591361173114618008290111698289078307025270180454503017813091464571988696332043391000128105356238462195601585714151981136533791126254244367388414254637800691497393553587818077944389037864462922610978145839837659167620212298715350220181796591747722791660689297121522985473543020282502562564127780433006101447592255518215938559489539924297015884125911008653036478498672724629349470035832837351838088189176967885284241119026083418780670849777058199916251437033209534092375954239720900448320646483225009137558891307464236
n = 14457187607874869213039015485206702511428688687137630158495121214327879587033651160662996569314331190269107067493499408706135563395879741231592940240342314463102055434056143229630796993773074909968097910845994389135381778364710657016964953421359045950998422474236721996201281420768935828275029669678394947873034636407300556662177458917539188364962833937409232767873848675460330287266153688227981487667468716579167813895143410064508306577847771964601528990387470344716224694682552156534461701485443980767170554113718519526959417943309692897906292794730558811143285435980523010614163610838057069957693937896503591874619

import gmpy2
from Crypto.Util.number import long_to_bytes

e = 8
k = 1
while True:
	h = m + k*n
	hsh = gmpy2.iroot(h,e)[0]
	if hsh**e == h:
		break
	k += 1
# 146913410772757766194482407144214295333114411765260602423197339861209058274813