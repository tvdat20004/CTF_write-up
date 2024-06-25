def gen_pubkey(p, n, k, r):
    F = GF(p)
    assert p > n, "Number of elements in field should be greater than n"
    C = codes.GeneralizedReedSolomonCode(sample(F.list(), n), k)
    S = matrix(F, k, k)
    S.randomize()
    while S.rank() != k:
        S.randomize()
    G = C.generator_matrix()
    R = matrix(k, r, lambda i, j: F.random_element())
    Q = list(identity_matrix(n + r))
    shuffle(Q)
    Q = matrix(F, Q)
    G_pub = S.inverse() * G.augment(R) * Q.inverse()
    pubkey = G_pub
    privkey = (C, S, Q)
    return (pubkey, privkey)


def encode_message(message: bytes, F, k):
    p = F.cardinality()
    message_int = int.from_bytes(message, 'big')
    message_vector = []
    while message_int:
        message_vector.append(message_int % p)
        message_int //= p
    print(len(message_vector))
    padding = k - len(message_vector) % k
    message_vector += [padding] * padding
    return [vector(F, message_vector[i:i + k])
            for i in range(0, len(message_vector), k)]


def encrypt(message: bytes, pubkey):
    k, n = pubkey.dimensions()
    F = pubkey[0, 0].parent()
    num_errors = (n - k) // 4 # 21
    encryptions = []
    for m in encode_message(message, F, k):
        print(m)
        error = [F.random_element() for _ in range(num_errors)] + \
            [0] * (n - num_errors)
        shuffle(error)
        error = vector(F, error)
        encryptions.append(m * pubkey + error)
    return encryptions


def main(p, n, k, r):
    pubkey, privkey = gen_pubkey(p, n, k, r)
    FLAG = b"CTF{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}"
    FLAG = b"CTF{pr1v4t3_s3t_m3mb3rsh1p_qu3r135_m3d4_m0r3_p0w3rfu1}"

    encrypted_flag = encrypt(FLAG, pubkey)
    pubkey.dump("pubkey1.sobj")
    matrix(encrypted_flag).dump("flag_enc1.sobj")

if __name__ == "__main__" and "__file__" in globals():
    p, n, k, r = 521, 256, 169, 39
    main(p, n, k, r)
