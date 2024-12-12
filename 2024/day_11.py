from collections import defaultdict
from input_loader import get_input
import time

use_real = True
example_input = '''
0 1 10 99 999
'''
example_input = '''
125 17
'''

lines = get_input(use_real, example_input, __file__)

replacement_cache = {}

def replace_one_stone(stone):
    if stone == 0:
        return [1]

    if len(str(stone)) % 2 == 0:
        one_and_zeros = 10 ** (len(str(stone)) // 2)
        right_stone = stone % one_and_zeros
        left_stone = (stone - right_stone) // one_and_zeros
        return [left_stone, right_stone]

    return [stone * 2024]

def replace_one_stone_with_cache(stone):
    if stone not in replacement_cache:
        replacement_cache[stone] = replace_one_stone(stone)
    return replacement_cache[stone]

def blink_once(stone_counts):
    new_counts = defaultdict(lambda: 0)
    for stone in stone_counts.keys():
        for new_stone in replace_one_stone_with_cache(stone):
            new_counts[new_stone] += stone_counts[stone]
    return new_counts

def blink_times(line, times):
    stones = [int(n) for n in line.split(" ")]
    stone_counts = defaultdict(lambda: 0)
    for s in stones:
        stone_counts[s] += 1
    for i in range(times):
        stone_counts = blink_once(stone_counts)
    return sum(stone_counts.values())

start = time.time()

print(f'Part 1: {blink_times(lines[0], 25)}') # 198075
print(f'Part 2: {blink_times(lines[0], 75)}') # 235571309320764

end = time.time()
print(f"Time taken: {end-start} seconds")
# 0.053 with caching, 0.077 without caching
