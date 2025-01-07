from utils import get_input

use_real = True
example_input = '''
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

grids = get_input(use_real, example_input, __file__, True)

keys = []
locks = []
for grid in grids:
    thing = [-1] * 5
    for row in grid:
        for i, c in enumerate(row):
            if c == "#":
                thing[i] += 1
    if grid[0][0] == "#":
        locks.append(thing)
    else:
        keys.append(thing)

def fits(key, lock):
    for i in range(5):
        if key[i] + lock[i] > 5:
            return False
    return True

matching_pairs = 0
for key in keys:
    for lock in locks:
        if fits(key, lock):
            matching_pairs += 1

print(f"Part 1: {matching_pairs}") # 3317
