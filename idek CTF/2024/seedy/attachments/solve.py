# from https://github.com/StackeredSAS/python-random-playground/blob/main/recover_DefaultSeed.py
from functions import *
import random

state = (3, (0, 4105789988, 2067591534, 2432402800, 1433881788, 3003124887, 1495199749, 984335047, 547862992, 1620362539, 2319963362, 2503999060, 2577833387, 3085279240, 114339416, 3472849231, 716465497, 3100925111, 1531881806, 4238598057, 3618195854, 3591989825, 105677198, 298928123, 3751036512, 119244537, 1518968726, 722465279, 3596941776, 3774769659, 3898511397, 1285558913, 751089842, 3985096120, 2058640983, 2559207619, 1554664638, 750231873, 4090305221, 771516336, 1277265304, 3751627889, 3150013619, 1277974136, 1415705662, 189770590, 3818215044, 1304440841, 1660286548, 2907635430, 115261396, 3150259341, 3687104454, 1061386245, 1671413543, 2466543233, 122897383, 2396113571, 3617161978, 3259867688, 2327605124, 1244702447, 2818625743, 243997131, 1247921812, 4147580939, 1986345085, 590332311, 200465741, 1270944412, 1781408327, 2841115703, 2306950959, 1326820268, 660861642, 1151247748, 1791733079, 2502162905, 3289173354, 1930247131, 1624168709, 2677468227, 2589679657, 2279565241, 691317876, 3581952291, 2509322642, 1938528549, 427890173, 510397650, 2094950364, 2253545286, 2281838199, 2186846142, 2897623700, 1206442494, 1403545543, 3264778457, 4096137485, 1368542590, 468546664, 3175649264, 1049532107, 3566583184, 532824081, 3441120247, 337384806, 305171162, 3699566574, 2898010962, 1694051187, 363125370, 3975878675, 1761302102, 2149867823, 1104451694, 2877469118, 829795533, 1308089070, 3334437478, 1455040021, 3350934173, 1829959861, 2336557134, 777225410, 2575283344, 2702312652, 4079519746, 2814810987, 3702757010, 2504370789, 3013078342, 4189733797, 2824469765, 4112719081, 651508064, 3153045939, 2315731645, 3492347661, 1305273427, 1132462562, 3477273211, 1676060314, 835566660, 3096295714, 2200990729, 529514343, 1250415862, 63190046, 805938067, 811806385, 3169574177, 2473549477, 2425859370, 2790453957, 416844822, 871641356, 2573881572, 3394910391, 3856451555, 2809845697, 3032030011, 3187684230, 3042877608, 1316011489, 120605308, 1998471367, 2817367133, 4078110888, 3090054487, 2550725984, 1904000358, 4214813430, 352707580, 2603572685, 2663525362, 3378477703, 3802618596, 2417611433, 1067844862, 1470942005, 2039730967, 1645188080, 2278603158, 1707648031, 70476484, 2733429161, 268892346, 3923623743, 1869467816, 3070247121, 2491792332, 1478861924, 2394425102, 1422418463, 912632610, 2555712405, 949365163, 138218426, 1535691606, 3442388084, 3827556973, 2340377546, 2724480239, 910248640, 573359166, 1425073581, 4066331030, 1502758826, 3651675665, 527117737, 1760895042, 1550146593, 273414177, 3593695378, 4180461967, 1780687992, 4261992670, 3991908742, 1053857060, 3242178769, 369046495, 3142419764, 1363772701, 4048081969, 3774323319, 341842977, 945032421, 1993882967, 2858074001, 96810303, 989691594, 2456992510, 1379446363, 965915142, 2124080283, 4253529648, 1321992587, 4292998495, 3147842259, 2086503724, 2575778271, 1552786361, 3718049205, 3849936855, 967056442, 4285969027, 2566603199, 2214441425, 801009799, 991252266, 1861282828, 2199494470, 757272870, 756737134, 465581557, 4151629387, 3567855099, 3601890657, 1196011973, 1379778467, 2143897127, 1190655114, 2321008015, 110514200, 3958404014, 239702121, 854677999, 1070441860, 2331008741, 570283571, 170884152, 557975185, 3147767611, 2911488364, 3723067959, 3451109703, 1905599538, 4178071621, 3786037856, 526857901, 3929191976, 1261797932, 3623652736, 3393661082, 2568172821, 1426397998, 864812920, 4103243150, 525326124, 3617621711, 287117497, 1908468563, 3052604065, 862736164, 255630558, 3809349974, 2545627768, 4115508706, 865695813, 1535096004, 2534516883, 1186921415, 2384229689, 1253486662, 2021320229, 1389964746, 4190248527, 880280112, 1850826025, 1647088500, 2905883009, 425324314, 1259422001, 3353738620, 3184156186, 2268193758, 536127506, 1916525021, 1684741010, 1749501578, 202259276, 160225615, 2505815205, 3851056852, 4166350006, 1415203975, 1657116296, 3651000651, 3645030349, 1391094999, 3246228032, 848268091, 3789072779, 645605620, 3006203579, 263418293, 1078749835, 663411076, 388752538, 4090042559, 878932466, 1579716270, 848079794, 3805987987, 2480287254, 2293386910, 964418862, 174373917, 547559185, 3502313357, 3371223352, 2874281982, 1065068462, 3048631420, 104728535, 2902352142, 2511967253, 2426716438, 1793335076, 3409129847, 3243625393, 3161467187, 2987902173, 2056189239, 1537669591, 2791492834, 4010169773, 2085046148, 611826913, 2329043999, 3444297466, 3942306059, 3196111214, 2186667688, 119978682, 1441499139, 561972125, 881937966, 2002715140, 2451752101, 2374941825, 289851086, 249698079, 1545065499, 1745809095, 753263612, 204465415, 4198094834, 2868666650, 1204698671, 772683217, 1385871115, 1235160716, 303023112, 1760781780, 4147267522, 3408412739, 2934791156, 1110703618, 3472654945, 1729628227, 3267967648, 461026103, 1896448384, 588245927, 625638852, 421090606, 2614767084, 1042937102, 3482212990, 3369091170, 289045130, 1895348359, 4121154101, 248445160, 4157368174, 1989081397, 2365220591, 2665937082, 3933525465, 2585736521, 3989430748, 1435181224, 762291554, 1625259426, 1302846132, 737037456, 2035268883, 1923225678, 21674646, 3746177995, 922991566, 3628381727, 3697068048, 1035900410, 2598210815, 2075507559, 653301610, 437045042, 3901725058, 3886013162, 3594954986, 1179738091, 4042857752, 3981514714, 1870349719, 4064998966, 3555637952, 1472070909, 1906059173, 4218676849, 3901004608, 2456246273, 4260965906, 1697558184, 1491222780, 2369756485, 2483766583, 63931416, 3456825531, 1731646699, 2360265228, 4019753736, 3454617757, 641531034, 1038246617, 3378956260, 748450241, 1376727208, 3561771840, 3681085834, 2296018536, 1349909281, 2229885807, 801923397, 1956747583, 4099816471, 362760569, 1546725325, 1084426707, 1130162054, 2020364847, 1771089913, 274473022, 1804034190, 404449570, 1600214965, 300094536, 3710651896, 1061893042, 2727724276, 937491582, 1436478667, 4250178879, 3315532740, 1676215165, 2239482349, 168995494, 4108672866, 3669720109, 12839398, 2121166717, 928262555, 4130529543, 2313301983, 3292913087, 3341444638, 761292692, 3839444310, 897192773, 865082327, 1764997964, 1008935761, 642526567, 1185122336, 3312068013, 3143524457, 795628675, 1907433167, 1459722402, 1187491358, 2399797873, 3000182761, 3986901562, 3713135144, 350995268, 4022259078, 187419681, 1989548312, 1378866138, 1698454578, 3136172403, 2788422833, 373093553, 3727047934, 2984705754, 4200790360, 672115284, 2320992050, 306906876, 2556407580, 1372241020, 1515521357, 1466347022, 1228529466, 426380086, 715695443, 4062226718, 1048421952, 2857598327, 1423542059, 1300814240, 3141909693, 3677223531, 2241803262, 1132254070, 3938493189, 3648369175, 2317784221, 2130383931, 242438180, 4155101118, 1913287060, 368528257, 289757747, 3137643972, 2646856874, 871087832, 541933880, 3334074036, 1947050477, 2681527534, 2539368124, 1543855068, 3233481252, 2105281155, 3831270343, 2380685531, 2271041690, 962639125, 1361345162, 4185966738, 562401006, 3700402638, 2823766012, 2058110897, 2941494311, 3061119005, 1940483462, 2310018383, 3412465755, 322329080, 63307277, 299877164, 3500635689, 2026828896, 1223287729, 3718051052, 158066441, 1629183052, 1129169396, 13953419, 630499087, 3883544247, 2567923959, 1903470044, 3964705285, 4292398747, 1064567123, 3786641399, 1734227856, 4181466708, 1372149418, 1815842159, 3985667302, 3006098018, 2364798451, 2969338269, 3297142513, 4077061429, 1390862857, 1837035173, 3636607464, 0), None)
random.setstate(state)
S = [untemper(random.getrandbits(32)) for _ in range(624)]
I = rewindState(S)

seed_array = seedArrayFromState(I)
seed = seedArrayToInt(seed_array)

from Crypto.Util.number import *
assert b'idek' in long_to_bytes(seed)
print(long_to_bytes(seed))