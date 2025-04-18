from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad

x0 = 2029673067800379268 
y0 = 1814239535542268363 
x1 = 602316613633809952 
y1 = 1566131331572181793 
p = 2525114415681006599 
iv = bytes.fromhex('6959dbf6bf22344d452c3831a3b68897')
enc = bytes.fromhex('a490e177c3838c8f24d36be5ee10e0c9e244ac2e54cd306eddfb0d585d5f27535835fab1cd83d26a669e6c08096b58cc4cc4cb082f4534ce80fab16e21f119adc45a5f59d179ca3683b77a942e4cf4081e01d921a51ec3a3a48c13f850c04b80c997367739bbde0a5415ff921d77a6ef')

F = GF(p)
coeff = Matrix(F,[[x0,1 ],[x1,1 ]])
df = vector(F, [y0**2  - x0**3 , y1**2  - x1**3 ])
[a,b] = coeff \ df
print(a,b)
# assert int(y1**2 - (x1**3 + int(a)*x1 + int(b))) % int(p) == 0
E = EllipticCurve(F, [a,b])
X0 = E(x0,y0)
X1 = E(x1,y1)
G = E.gens()[0 ]
# kp = G.discrete_log(X0)
# kq = G.discrete_log(X1)
kp = 916472720818205535 
kq = 1673271260266693096 
# kp = a + b
# kq = b + a(a+b) = b + a*kp
order = E.order()
coeff = matrix(Zmod(order),[[1 ,1 ], [kp,1 ]])
df = vector([kp,kq])
[a,b] = coeff \ df
v = int((G*int(b) + int(a)*X1).xy()[0 ])
k = pad(l2b(v**2 ), 16 )
cipher = AES.new(k, AES.MODE_CBC, iv=iv)

flag = cipher.decrypt(enc)
print(flag)

