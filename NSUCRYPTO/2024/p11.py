
def find_bound(num_blocks):
    '''
    find the range of sum (-1^j)*p_{i+6j} in each case of num_blocks
    '''
    min = 0
    max = 0
    for i in range(num_blocks):
        if i % 2:
            min -= 9 
        else:
            max += 9 
    return min, max 

def find_min_num_block(x_i: list[int]):
    '''
    Find the minimum of number of blocks in collision
    '''
    num = 1
    while not all(x in range(*find_bound(num)) for x in x_i):
        num += 1
    return num
def caculate(n):
    '''
    Caculate the sum (-1^i)*n_i
    '''
    return sum((-1)**i * int(x) for i, x in enumerate(n))

def brute(x, num_blocks):
    candidate = 0
    if num_blocks == 1:
        if 0 <= x <= 9:
            return [str(x)]
        else:
            return None
    while True:
        candidate_str = str(candidate).rjust(num_blocks - 1, '0')
        known = caculate(candidate_str)
        if num_blocks % 2:
            unknown = x - known
        else:
            unknown = known - x 
        if 0 <= unknown <= 9:
            return list(candidate_str + str(unknown))
            break
        else:
            candidate += 1
        if candidate > 10**(num_blocks-1):
            return None


def find_collision(data : str):
    # padding
    i = 1
    while len(data) % 6:
        data += str(i)
        i += 1 
    blocks = [data[i:i+6] for i in range(0, len(data), 6)]
    x_i = [caculate([block[i] for block in blocks]) for i in range(6)]
    num_blocks = find_min_num_block(x_i)
    print(x_i)
    if num_blocks == 1:
        return "".join(str(x) for x in x_i)
    # padding case
    for num_pad in [5,4,3,2,1,0]:
        coll = []
        last_block_padding = (6 - num_pad) * [None] + list(range(1,num_pad + 1))
        for i,x in enumerate(x_i):
            if last_block_padding[i]:
                if num_blocks % 2:
                    x -= last_block_padding[i]
                else:
                    x += last_block_padding[i]
                result = brute(x, num_blocks - 1)
                if result == None:
                    break
                else:
                    result += [str(last_block_padding[i])]
            else:
                result = brute(x, num_blocks)
            coll.append(result)
        if len(coll) < 6:
            continue
        ans = ""
        for i in range(num_blocks):
            ans += "".join(c[i] for c in coll)
        print(ans)
        return ans[:-num_pad]

# print(brute(-11, 2))
print(find_collision("134875512293"))
