from pwn import xor
flag_enc = bytes.fromhex("fb7fdbf9e714a08ce9cdf109bb527acba27accfeff16fcdcb1cdf358bb557898aa2d9da9af5c")
msg = b'1'*len(flag_enc)
msg_enc = bytes.fromhex("ab2d9eaead10a88eb9cbf00cb9002acfab2d9eaead10a88eb9cbf00cb9002acfab2d9eaead10")
print(xor(xor(msg_enc, flag_enc),msg))