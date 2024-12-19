from utils import get_input

use_real = True
example_input = '''
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

lines = get_input(use_real, example_input, __file__)
available_patterns = set(lines[0].split(", "))
designs = lines[1:]

cache = {}

def count_combinations(design, available_patterns):
    if design == "":
        return 1
    if design in cache:
        return cache[design]

    combinations = 0
    for pattern in available_patterns:
        if design.startswith(pattern):
            remainder = design[len(pattern):]
            combinations += count_combinations(remainder, available_patterns)

    cache[design] = combinations
    return combinations

count = 0
total_combinations = 0
for design in designs:
    num_combinations = count_combinations(design, available_patterns)
    if num_combinations > 0:
        count += 1
        total_combinations +=num_combinations

print(f"Part 1: {count}") # 360
print(f"Part 2: {total_combinations}") # 577474410989846
