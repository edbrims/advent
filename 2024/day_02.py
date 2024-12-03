from input_loader import get_input

use_real = True
example_input = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

input = get_input(use_real, example_input, __file__)

def is_safe(levels):
    diffs = [a-b for a, b in zip(levels[1:], levels[:-1])]
    if max(diffs) > 0 and min(diffs) < 0:
        return False
    if 0 in diffs:
        return False
    if max(diffs) > 3 or min(diffs) < -3:
        return False
    return True

def is_safe_dampened(levels):
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        dampened_list = levels[:i] + levels[i+1:]
        if (is_safe(dampened_list)):
            return True
    return False

count_safe = 0
count_safe_dampened = 0
for line in input:
    levels = list(map(int, line.split(' ')))
    if is_safe(levels):
        count_safe += 1
    if is_safe_dampened(levels):
        count_safe_dampened += 1
print(f'Part 1: {count_safe}')
print(f'Part 2: {count_safe_dampened}')
