import random
import time
# from pwn import * 

# r = remote("209.97.140.29", 32271)
seed = int(time.time())
print(seed)
# r.recvuntil(b'EXTRACTION: ')
# check_seed = list(map(int, r.recvuntilS(b'\n').strip().split(' ')))
check_seed = list(map(int, input("enter:").strip().split(' ')))
print(check_seed)
while True:
    random.seed(int(seed))
    print(seed) 
    continuer = 0
    for _ in range(5):
        if random.randint(1,90) != check_seed[_]:
            continuer = 1
            break
    time.sleep(1)
    if continuer:
        seed += 1
        continue
    for _ in range(5):
        print(random.randint(1,90), end = " ")
    break