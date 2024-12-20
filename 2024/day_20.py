from collections import defaultdict
from utils import get_input, Coords

use_real = True
example_input = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

directions = [Coords(0, 1), Coords(1, 0), Coords(0, -1), Coords(-1, 0)]
diagonals  = [Coords(1, 1), Coords(1, -1), Coords(-1, -1), Coords(-1, 1)]

def find_start(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                return Coords(r, c)
    return None

def char_at(square, grid):
    if square.r < 0 or square.r >= len(grid):
        return None
    if square.c < 0 or square.c >= len(grid[square.r]):
        return None
    return grid[square.r][square.c]

def print_course(grid, numbered):
    for r in range(len(grid)):
        output_row = []
        for c in range(len(grid[r])):
            if numbered[r][c] is not None:
                output_row.append(str(numbered[r][c] % 10))
            else:
                output_row.append(grid[r][c])
        print("".join(output_row))


def number_path(grid):
    start_square = find_start(grid)

    numbered = [[None]*len(grid[r]) for r in range(len(grid))]
    square = start_square
    step_number = 0
    path = [start_square]
    while char_at(square, grid) != "E":
        numbered[square.r][square.c] = step_number
        possible_steps = []
        for direction in directions:
            next_square = square.add(direction)
            if char_at(next_square, grid) == "#":
                continue
            if numbered[next_square.r][next_square.c] == step_number - 1:
                continue
            possible_steps.append(next_square)
        if len(possible_steps) != 1:
            raise Exception(f"Wrong number of steps: {possible_steps}")
        square = possible_steps[0]
        step_number += 1
        numbered[square.r][square.c] = step_number
        path.append(square)
    return path, numbered

def find_cheats_from_square(start_cheat_square, max_cheat_length, grid, numbered):
    savings_from_square = defaultdict(lambda: set())
    starting_number = char_at(start_cheat_square, numbered)

    # Just do Mahattan diamonds.
    for size in range(1, max_cheat_length + 1):
        diamond = set()
        for diagonal in diagonals:
            for i in range(size + 1):
                diamond.add(start_cheat_square.add(Coords(diagonal.r * (size - i), 0)).add(Coords(0, diagonal.c * i)))
        for cheat_square in diamond:
            if (char_at(cheat_square, numbered) is not None and
                char_at(cheat_square, numbered) > starting_number + size):
                saving = char_at(cheat_square, numbered) - starting_number - size
                savings_from_square[saving].add(cheat_square)

    # if savings_from_square[74]:
    #     print(f"Ways to save 74: {start_cheat_square}-{savings_from_square[74]}")
    num_savings_from_square = {}
    for saving in savings_from_square.keys():
        num_savings_from_square[saving] = len(savings_from_square[saving])
    return num_savings_from_square

def count_cheats(grid, max_cheat_length):
    path, numbered = number_path(grid)
    savings = defaultdict(lambda: 0)
    # print_course(grid, numbered)
    for square in path:
        cheats = find_cheats_from_square(square, max_cheat_length, grid, numbered)
        for cheat_saving in cheats.keys():
            savings[cheat_saving] += cheats[cheat_saving]
    return savings

grid = get_input(use_real, example_input, __file__)

def num_cheats_saving_100(grid, max_cheat_length):
    savings = count_cheats(grid, max_cheat_length)
    num_cheats = 0
    for saving in sorted(savings.keys()):
        if saving >= 100:
            num_cheats += savings[saving]
        print(f"There are {savings[saving]} cheats that save {saving} picoseconds.")
    return num_cheats

print(f"Part 1: {num_cheats_saving_100(grid, 2)}") # 1402
print(f"Part 2: {num_cheats_saving_100(grid, 20)}")# 1020244
