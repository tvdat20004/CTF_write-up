
from Crypto.Util.number import *
from Crypto.Cipher import AES
n = 0x6fe4dba45f9d40226fef01f4fa4039eea9a9001266c4730f14df7faac4a086046a9246425dd0b0328cf51540d2cfbc31e0b73fdea75ee49e178cc4a555d83b9e99c28980ff420b7ff9b8a02e7f26b38eb3dd40e519d4cea7804d6b9172198778d3fc8da2d2d225fd3ed7aafb2f5262b70f3c313e2df7944ca678d10e5659c43f

def isqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def fermat(n):
    a = isqrt(n)
    b2 = a*a - n
    b = isqrt(n)
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2)
        count += 1
    p = a+b
    q = a-b
    assert n == p * q
    return p, q


from Crypto.Cipher import AES
import hashlib

def decrypt_seipd_aes256(enc: bytes, key32: bytes):
    """
    Giải mã SEIPD (Tag 18) với AES-256 session key.
    Trả về (data_without_mdc, info).
    """
    if len(key32) != 32:
        raise ValueError("AES-256 session key phải 32 byte")
    bs = 16
    if len(enc) < bs + 2 + 22:
        raise ValueError("Ciphertext quá ngắn cho OpenPGP CFB + MDC")

    eiv = enc[:bs]      # encrypted IV (OpenPGP variant)
    body = enc[bs:]     # phần còn lại

    cipher = AES.new(key32, AES.MODE_OPENPGP, iv=eiv)
    plain = cipher.decrypt(body)
    print(plain)
    prefix = plain[:bs+2]           
    rest   = plain[bs+2:]          
    if len(rest) < 22:
        raise ValueError("Thiếu MDC")

    trailer = rest[-22:-20]    
    mdc     = rest[-20:]
    data    = rest[:-22]

    prefix_ok = (prefix[-2:] == prefix[bs-2:bs])
    mdc_ok = (
        trailer == b"\xD3\x14" and
        hashlib.sha1(prefix + data + b"\xD3\x14").digest() == mdc
    )
    return data, {"prefix_ok": prefix_ok, "mdc_ok": mdc_ok}
p, q = fermat(n)

c1 = bytes.fromhex("042ff6b422fdfa142ce7802699f895120bc9ad8c4925d603bde4d9920c5400962792f0ccd48de0a4249ec16357a66f16a5585ecdd72ed690ffab1ab362231520a2d6f683703e1948f6fbcf0a9ab8afdef076eae4490e55dc45b41af6741340a597d68725fd1a473eaa5ef81e47f4d2c72029736a24311dac75c02320024f2237")
c1 = bytes_to_long(c1)
# print(pow(65537, -1, (p-1) * (q-1)))
m1 = pow(c1, pow(65537, -1, (p-1) * (q-1)), n)
m1 = long_to_bytes(m1)
# print(len(m1))
enc = bytes.fromhex("e9eff9ef904f16f5f427a9603f04da469b6ae0b4ab2ca339542299457e310555f19a87ad8d4db659b86460426ac2d4c58dc10e0e03a6add792ce252b1eacdfeaa37b6d93cb7db68d7b9ad41fcfa5e1b37c84cb2ff33f9f42d615456a6f85ac986f780b295334a4")
sep_index = m1.index(b'\x00')
session_key = payload[1:-2]  # khóa phiên thực tế
print(decrypt_seipd_aes256(enc, session_key))