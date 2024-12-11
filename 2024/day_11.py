from collections import defaultdict
from input_loader import get_input

use_real = True
example_input = '''
0 1 10 99 999
'''
example_input = '''
125 17
'''

lines = get_input(use_real, example_input, __file__)

def blink_once(stone_counts):
    new_counts = defaultdict(lambda: 0)
    for stone in stone_counts.keys():
        number_of_stones = stone_counts[stone]
        if stone == 0:
            new_counts[1] += number_of_stones
        elif len(str(stone)) % 2 == 0:
            one_and_zeros = 10 ** (len(str(stone)) // 2)
            right_stone = stone % one_and_zeros
            left_stone = (stone - right_stone) // one_and_zeros
            new_counts[left_stone] += number_of_stones
            new_counts[right_stone] += number_of_stones
        else:
            new_counts[stone * 2024] += number_of_stones
    return new_counts


def blink_times(line, times):
    stones = [int(n) for n in line.split(" ")]
    stone_counts = defaultdict(lambda: 0)
    for s in stones:
        stone_counts[s] += 1
    for i in range(times):
        stone_counts = blink_once(stone_counts)
    return sum(stone_counts.values())


print(f'Part 1: {blink_times(lines[0], 25)}') # 198075
print(f'Part 2: {blink_times(lines[0], 75)}') # 235571309320764
