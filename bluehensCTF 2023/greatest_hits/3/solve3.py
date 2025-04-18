from pwn import xor 

enc = bytes.fromhex("98edbf5c8dd29e9bbc57d0e2990e4e692efb81c2318c69c626d7ea42f2efc70fece4ae5c89c7999fef1e8bac99021d7266bc9cde3cd97b9a2adaeb08dea1ca0582eaac13ced7dfdbad1194b1c60f5d372eeec29832ca20d12a85b545f9f69b1aaeb6ec4cd4")

clue = b"https://gist.github.com/AndyNovo"
for i in range(0,len(enc) - len(clue)):
    key = xor(enc[i:i+len(clue)], clue)
    key = key[-(i%len(clue)):] + key[:-(i%len(clue))]
    print(xor(enc, key))

# b'The last stage of the problem is at https://gist.github.com/AndyNovo/d2415028d31f572ff9ec03bf95fb3605'
