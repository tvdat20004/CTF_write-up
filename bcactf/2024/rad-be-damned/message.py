import random
# = .bit_length()
def find_leftmost_set_bit(plaintext):
    pos = 0
    while plaintext > 0:
        plaintext = plaintext >> 1
        pos += 1
    return pos
        
def encrypt(plaintext: str):
    enc_plaintext = ""

    for letter in plaintext:
        cp = 19
        cp_length = 5
        bin_letter, rem = ord(letter), ord(letter) * 2**(cp_length - 1)
        while (rem.bit_length() >= cp_length):
            first_pos = find_leftmost_set_bit(rem)
            rem = rem ^ (cp << (first_pos - cp_length))
        enc_plaintext += format(bin_letter, "08b") + format(rem, "04b")

    return enc_plaintext

def rad(text: str):
    corrupted_str = ""
    for ind in range(0, len(text), 12):
        bit_mask = 2 ** (random.randint(0, 11))
        snippet = int(text[ind : ind + 12], base = 2)
        rad_str = snippet ^ bit_mask
        corrupted_str += format(rad_str, "012b")
    return corrupted_str

def main():
    with open('flag.txt') as f:
        plaintext = f.read().strip()
    enc_plaintext = encrypt(plaintext)
    cor_text = rad(enc_plaintext)
    print(cor_text)

if __name__ == '__main__':
    main()