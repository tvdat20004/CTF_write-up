from secp256k1 import *
import secrets
from hashlib import sha256
import json
from pwn import *
def gen_publickey(a, gen_proof=False):  # generate public key with a Schnorr proof
    A = multiply(G, a)
    if gen_proof:
        k = secrets.randbelow(N)
        R = multiply(G, k)
        e = int(sha256((str(P) + str(Gx) + str(Gy) +
                str(A[0]) + str(A[1]) + str(R[0]) + str(R[1])).encode()).hexdigest(), 16)
        z = (e*a + k) % N
        assert multiply(G, z) == add(multiply(A, e), R)
        return A, (R, z, e)
    return A
def check(B):
	return B[1]**2 % P == (B[0]**3 + 7)%P

def verify_publickey(A, proof):
    R, z = proof
    e = int(sha256((str(P) + str(Gx) + str(Gy) +
            str(A[0]) + str(A[1]) + str(R[0]) + str(R[1])).encode()).hexdigest(), 16)
    return multiply(G, z) == add(multiply(A, e), R)

def arbitrary_proof():
    while True:
        A = [0, randint(10, 2**256)]
        R = [0,   0]
        e = int(sha256((str(P) + str(Gx) + str(Gy) +
                str(A[0]) + str(A[1]) + str(R[0]) + str(R[1])).encode()).hexdigest(), 16)
        z = 0
        proof = (R, z)
        if verify_publickey(A, proof):
            return A, proof

# io = process(["python3", "guessme.py"])
io = remote("103.173.227.108", 10001)
pub = arbitrary_proof()
A, proof = pub
R,z = proof
payload = json.dumps({
	"publickey" : A, 
	"proof" : (R,z)
})
for i in range(128):
	io.sendlineafter(b'Give me your public key and its Schnorr proof.\n', payload.encode())
	exec(io.recvlineS().strip())
	res = int(not check(B))
	send = json.dumps({"bit" : res})
	io.sendlineafter(b'Guess my bit.\n', send.encode())
io.interactive()


