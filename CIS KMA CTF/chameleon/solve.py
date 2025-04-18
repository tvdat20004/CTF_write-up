from pwn import *
import json
from hashlib import sha256
import random 
from tqdm import *
import string 
from Crypto.Util.number import *
class Server:
    def __init__(self, secret) -> None:
        self.N = 2**11
        self.tree = []
        self.users = []
        self.k = long_to_bytes(secret)
        self.p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
        self.q = (self.p - 1) // 2
        self.g = 0x2
        self.x = secret
        self.y = pow(self.g, self.x, self.p)
        self.buile_merkle_tree()
        self.root = self.get_root_hash()

    def keyed_random(self, identifier: bytes, index: int) -> int:
        return int.from_bytes(sha256(identifier + self.k + str(index).encode()).digest(), "big")

    def chameleon_hash(self, m: int, r: int) -> bytes:
        return (pow(self.g, m, self.p) * pow(self.y, r, self.p) % self.p).to_bytes(192, "big")

    def chameleon_extract(self, m1: int, r1: int, m2: int) -> int:
        r2 = (self.x * r1 + m1 - m2) * pow(self.x, -1, self.q) % self.q
        return r2

    def get_leaf(self, index: int) -> bytes:
        return self.chameleon_hash(self.keyed_random(b"m", index), self.keyed_random(b"r", index))

    def buile_merkle_tree(self) -> None:
        curr_layer = [self.get_leaf(i) for i in range(self.N)]
        self.tree.append(curr_layer)
        while len(curr_layer) != 1:
            curr_layer = [sha256(self.tree[-1][i]+self.tree[-1][i+1]).digest()
                          for i in range(0, len(self.tree[-1]), 2)]
            self.tree.append(curr_layer)
        # print(self.tree)

    def get_root_hash(self) -> str:
        return self.tree[-1][0].hex()

    def add_user(self, username: str) -> str:
        if not all(char in string.printable for char in username):
            return "Invalid username."
        if username in self.users:
            return "Username already exists."
        else:
            index = len(self.users) % self.N
            self.users.append(username)
            username_hash = int.from_bytes(sha256(username.encode()).digest(), "big")
            r = self.chameleon_extract(self.keyed_random(b"m", index), self.keyed_random(
                b"r", index), username_hash)
            assert self.chameleon_hash(username_hash, r) == self.get_leaf(index)
            proof = {"username": username, "r": hex(r), "index": index}
            path = []
            for layer in self.tree[:-1]:
                is_right_node = index % 2
                sibling_index = index - 1 if is_right_node else index + 1
                path.append(layer[sibling_index].hex())
                index //= 2
            proof["path"] = path
            return json.dumps(proof)

    def verify_user(self, proof: str) -> str:
        proof = json.loads(proof)
        username = proof["username"]
        index = proof["index"]
        assert 0 <= index < self.N
        tmp = self.chameleon_hash(int.from_bytes(
            sha256(username.encode()).digest(), "big"), int(proof["r"], 16))
        for level in range(num_layers):
            is_right_node = index % 2
            if is_right_node:
                tmp = sha256(bytes.fromhex(
                    proof["path"][level]) + tmp).digest()
            else:
                tmp = sha256(
                    tmp + bytes.fromhex(proof["path"][level])).digest()
            index //= 2
        if tmp.hex() == self.root:
            if username == "Chamomile":
                return FLAG
            return f"Welcome back, {username}."
        else:
            return "Invalid user."

printable_chars = string.printable
io = remote("103.173.227.108",10002)
# io = process(["python3", "chameleon.py"])
# io.recvlne()
print(io.recvlineS())
root = bytes.fromhex(io.recvlineS().strip().split(':')[1])
pkey = int(io.recvlineS().strip().split('0x')[1], 16)
def generate_random_string(length):
    return ''.join(random.choice(printable_chars) for _ in range(length))

def add_user(username):
	payload = json.dumps({"option" : 1, "username" : username})
	io.sendline(payload.encode())
	return json.loads(io.recvlineS().strip())

out1 = add_user('dat')
for i in trange(2**11-1):
	add_user(generate_random_string(10))
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
q = (p-1)//2
out2 = add_user('abc')
r1 = eval(out1["r"])
r2 = eval(out2["r"])
# assert r1 == r2
m1 = int.from_bytes(sha256(b"dat").digest(), "big")
m2 = int.from_bytes(sha256(b"abc").digest(), "big")
secret = (m2 - m1) * pow(r1 - r2, -1, q) % q 
print(secret)
s = Server(secret)
payload = s.add_user("Chamomile")
io.sendline(json.dumps({"option" : 2, "username" : "Chamomile"}).encode())
io.sendline(payload.encode())
io.interactive()


