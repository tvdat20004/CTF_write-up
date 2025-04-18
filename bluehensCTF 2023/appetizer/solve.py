
choices = [19728964, 30673077, 137289540, 195938621, 207242611, 237735979, 298141799, 302597011, 387047012, 405520686, 424852916, 461998372, 463977415, 528505766, 557896298, 603269308, 613528675, 621228168, 654758801, 670668388, 741571487, 753993381, 763314787, 770263388, 806543382, 864409584, 875042623, 875651556, 918697500, 946831967]
target = 7627676296

def is_subset_sum(set, target):
    n = len(set)
    subset = [False] * n

    def backtrack(index, current_sum):
        if current_sum == target:
            return True
        if current_sum > target or index == n:
            return False

        # Include the current element in the subset
        subset[index] = True
        if backtrack(index + 1, current_sum + set[index]):
            return True

        # Exclude the current element from the subset
        subset[index] = False
        if backtrack(index + 1, current_sum):
            return True

        return False

    if backtrack(0, 0):
        # Subset with the target sum exists, print the subset
        result = [set[i] for i in range(n) if subset[i]]
        return result
    else:
        return None

winner = is_subset_sum(choices, target)

assert sum(winner) == target
print("UDCTF{%s}" % ("_".join(map(str,winner))))