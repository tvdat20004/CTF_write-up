

# This file was *autogenerated* from the file solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_5 = Integer(5); _sage_const_100 = Integer(100); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0)
from pwn import * 

r = process(["sage", "server.sage"])
r.recvline()
exec(r.recvlineS().strip()) #m0
exec(r.recvlineS().strip()) #m1
exec(r.recvlineS().strip()) #m2
r.recvline()
exec(r.recvlineS().strip()) #seed 
exec(r.recvlineS().strip()) #v 
com = m0
resp = m1
verif = m2
F = []
seed = bytes(seed)	
from hashlib import sha256

FF = GF(_sage_const_5 )
for i in range(_sage_const_100 ):
    cur = []
    for j in range(_sage_const_100 ):
        cur.append([])
        for k in range(_sage_const_100 ):
            cur[-_sage_const_1 ].append(list(FF)[sha256(seed).digest()[_sage_const_0 ] % _sage_const_5 ])
            seed = sha256(seed).digest()
    F.append(matrix(FF, _sage_const_100 , _sage_const_100 , cur))
variables = ",".join([f't{i}' for i in range(_sage_const_100 )])
t = var(variables)
t = matrix(n, _sage_const_1 , t)
# for i in range(100):

# equation = []
# for k in range(100)
# 	left = 0
# 	for j in range(100):
# 		for i in range(100):



