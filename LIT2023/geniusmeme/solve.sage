df = [1825147270203874538950085, 1755355241290944436019489,  150220311113190713333212, 1826562141290875830948785]
coef = matrix([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1]
])
ans = coef \ vector(df)
X = [i+1 for i in range(4)]
P.<x> = PolynomialRing(QQ)
fx = P.lagrange_polynomial([
    (x, y) for x,y in zip(X,ans)
])
flag = "".join([str(i) for i in ans]) + str(fx(5))
print(flag)
