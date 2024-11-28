import math
input = open("day_14_input.txt", "r").read()

# Test
# input = '''O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....'''

grid = [[*l] for l in input.split('\n') if l]

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def rotate_clockwise(grid):
    rotated_grid = []
    for i in range(len(grid[0])):
        # Columns from left to right, reversed
        column = [line[i] for line in grid][::-1]
        rotated_grid.append(column)
    return rotated_grid

def rotate_anticlockwise(grid):
    rotated_grid = []
    for i in range(len(grid[0])):
        # Columns from right to left, not reversed
        column = [line[len(line) - i - 1] for line in grid]
        rotated_grid.append(column)
    return rotated_grid

def rotate_180(grid):
    return [l[::-1] for l in grid[::-1]]

def roll_to_start(column):
    last_solid = -1
    pointer = 0
    for pointer in range(len(column)):
        if column[pointer] == '#':
            last_solid = pointer
        elif column[pointer] == 'O':
            column[pointer] = '.'
            column[last_solid + 1] = 'O'
            last_solid += 1
    return column

def roll_west(grid):
    rolled_grid = []
    for row in grid:
        rolled_grid.append(roll_to_start(row))
    return rolled_grid

def score_grid(grid):
    score = 0
    length = len(grid)
    for i in range(length):
        for c in grid[i]:
            if c == 'O':
                score += length - i
    return score

def do_cycle(grid, which):
    # Roll north
    grid = rotate_anticlockwise(grid)
    grid = roll_west(grid)
    grid = rotate_clockwise(grid)

    # Roll west
    grid = roll_west(grid)

    # Roll south and leave clockwise
    grid = rotate_clockwise(grid)
    grid = roll_west(grid)

    # Roll east and leave upside down
    grid = rotate_clockwise(grid)
    grid = roll_west(grid)

    # Straighten up
    grid = rotate_180(grid)

    return grid

def get_easy_equivalent(target, first_time, second_time):
    cycle_length = (second_time - first_time)
    modded = target % cycle_length
    # Make it at least first_time
    return modded + cycle_length * math.floor(first_time * 1.0/cycle_length)

def do_n_cycles(grid, n):
    grid_to_index = {}
    grids_seen = []

    for i in range(n):
        grids_seen.append(grid)
        cache_key = ':'.join([''.join(r) for r in grid])
        if cache_key in grid_to_index:
            # We're repeating ourselves!
            # print(f'{ grid_to_index[cache_key]} == {i}')
            easy_n = get_easy_equivalent(n, grid_to_index[cache_key], i)
            return grids_seen[easy_n]

        else:
            grid_to_index[cache_key] = i

        grid = do_cycle(grid, i)
    return grid

print(f'Part 1: {score_grid(rotate_clockwise(roll_west(rotate_anticlockwise(grid))))}')
print(f'Part 2: {score_grid(do_n_cycles(grid, 1000000000))}')
