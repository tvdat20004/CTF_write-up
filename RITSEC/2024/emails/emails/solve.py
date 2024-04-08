from pwn import xor 
enc = open("email5.enc", "rb").read()
block = [enc[i:i+32] for i in range(0,len(enc), 32)]
known = b"hanks,\r\n- Your Secret Conspirato"
key = xor(block[-2], known)

# key = key + (32 - len(key))*b'\0'
print(xor(enc, key))