import requests
import sys
from sage.all import * 
from Crypto.Util.number import * 
import hashlib
import json
sys.path.append('/mnt/e/tvdat20004/tools/CTF_tools/shared')
sys.path.append('/mnt/e/tvdat20004/tools/CTF_tools/attacks/hnp')

url = 'http://206.189.88.50:25001'
from partial_integer import PartialInteger
from lattice_attack import * 
def generate_private_key(pokemon_ids):
    pokemon_bytes = bytes(pokemon_ids)
    private_key = hashlib.sha256(pokemon_bytes).digest()
    return private_key

def start_session():
    endpoint = '/api/session/start'
    response = requests.post(url + endpoint,)
    return response.json()
def submit(payload):
    endpoint = '/api/session/verify'
    response = requests.post(url + endpoint,headers=headers, json={'password' : payload})
    return response.json()
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7 
E = EllipticCurve(GF(p), [a,b])
response = start_session()
G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
order = G.order()
data = response['data']
sessionid = data['sessionId']
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {sessionid}",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
pokemon_list = json.loads(open('src/data/pokedex.json', 'r').read())

pk = bytes.fromhex(data['publicKey'])
vaults = data['vaults']
selectedPokemon = data['selectedPokemon']
hs = [bytes_to_long(hashlib.sha256(v['id'].encode()).digest()) for v in vaults]
ids = [pok['id'] for pok in selectedPokemon]
sigs = [bytes.fromhex(v['signature']) for v in vaults]
# print(sigs)
rs = [bytes_to_long(sig[:32]) for sig in sigs]
ses = [bytes_to_long(sig[32:]) for sig in sigs]

nonces = [PartialInteger.from_msb(32*8, bytes_to_long(bytes([0]*9 + [ids[0], 0])), 11*8) for _ in range(6)]
for sk, nonces in dsa_known_msb(order, hs, rs, ses, nonces):
    first = long_to_bytes(abs(nonces[0]))[0]
print(submit('123'))
secret_key = long_to_bytes(sk)
ids.remove(first)
import itertools
import tqdm
cc = list(itertools.permutations(ids))
for perm in tqdm.tqdm(cc):
    pokemonIds = list(perm) + [first]
    if secret_key == generate_private_key(pokemonIds):
        payload = ' '.join(pokemon_list[idx]['name'] for idx in pokemonIds)
        print(submit(payload))