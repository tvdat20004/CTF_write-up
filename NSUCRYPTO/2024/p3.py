from itertools import product

shift = [[], [0], [1], [0, 1], [2], [3], [0, 3], [1, 3], [4], [5], [6], [0, 6], [1, 6], [6, 3], [7], [8]]

perms = product([0, 1], repeat=9)


for perm in list(perms):
    for i in shift:
        tmp = list(perm)
        for j in i:
            tmp[j] = 1 - tmp[j]

        print(tmp)