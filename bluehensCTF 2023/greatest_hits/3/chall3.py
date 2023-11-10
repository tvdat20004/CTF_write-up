flaglink="https://gist.github.com/AndyNovo/aaa4bf206eaaa26dc7ccdbf5254236e0"

def xor(msg, key):
    o = ''
    for i in range(len(msg)):
        o += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return o

clue="https://gist.github.com/AndyNovo"
import os
key = os.urandom(len(clue))
assert(flaglink.count(clue) > 0)

print(xor(flaglink, key).encode('hex'))
#98edbf5c8dd29e9bbc57d0e2990e4e692efb81c2318c69c626d7ea42f2efc70fece4ae5c89c7999fef1e8bac99021d7266bc9cde3cd97b9a2adaeb08dea1ca0582eaac13ced7dfdbad1194b1c60f5d372eeec29832ca20d12a85b545f9f69b1aaeb6ec4cd4
