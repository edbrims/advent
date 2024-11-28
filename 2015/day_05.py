input = open("day_05_input.txt", "r").read()

vowels = {'a', 'e', 'i', 'o', 'u'}
def has_three_vowels(str):
    num_vowels = 0
    for c in str:
        if c in vowels:
            num_vowels += 1
            if num_vowels >= 3:
                return True
    return False

def has_double(str):
    for i in range(len(str) - 1):
        if str[i] == str[i+1]:
            return True
    return False

def contains_bad_pairs(str):
    if 'ab' in str:
        return True
    if 'cd' in str:
        return True
    if 'pq' in str:
        return True
    if 'xy' in str:
        return True
    return False

def is_nice_part_1(str):
    return has_three_vowels(str) and has_double(str) and not contains_bad_pairs(str)

def has_xyx(str):
    for i in range(len(str) - 2):
        if str[i] == str[i+2]: # and str[i] != str[i+1]:
            return True
    return False

def has_abab(str):
    for i in range(len(str) - 3):
        pair = str[i:i+2]
        if pair in str[i+2:]:
            # print(f'Pair {pair} twice in {str}')
            return True
    return False


def is_nice_part_2(str):
    return has_xyx(str) and has_abab(str)

strings = [l for l in input.split('\n') if l]

num_nice_part_1 = 0
num_nice_part_2 = 0
for str in strings:
    if is_nice_part_1(str):
        num_nice_part_1 += 1
    if is_nice_part_2(str):
        num_nice_part_2 += 1

print(f'Part 1: {num_nice_part_1}')
# 255
print(f'Part 2: {num_nice_part_2}')
# 55
