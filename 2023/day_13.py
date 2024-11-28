input = open("day_13_input.txt", "r").read()

# Test
# input = '''#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#'''

# input = '''.##.###
# .##.###
# .######
# ##...##
# #..#.#.
# .##....
# .##....
# #.#....
# ...###.
# ...###.
# #.#.#..
# .##....
# .##....
# #..#.#.
# ##...##'''

grids = input.split('\n\n')

def count_differences_between_strings(s1, s2):
    num_differences = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            num_differences += 1
    return num_differences

def grid_has_symmetry_with_i_above(grid, i, num_smudges):
    j = 0
    num_differences = 0
    while i + j < len(grid) and i - j - 1 >= 0:
        num_differences += count_differences_between_strings(
            grid[i + j], grid[i - j - 1])
        j += 1

    # print(f'Differences with {i} above: {num_differences}')
    return (num_differences == num_smudges)

def find_horizontal_line(grid, num_smudges):
    for i in range(1, len(grid)):
        if grid_has_symmetry_with_i_above(grid, i, num_smudges):
            return i
    return None

def transpose(grid):
    transposed_grid = []
    for i in range(len(grid[0])):
        transposed_grid.append(''.join([r[i] for r in grid]))
    return transposed_grid

def find_vertical_line(grid, num_smudges):
    transposed_grid = transpose(grid)
    return find_horizontal_line(transposed_grid, num_smudges)

def find_symmetry_with_smudges(num_smudges):
    total = 0
    for grid_str in grids:
        grid = [l for l in grid_str.split('\n') if l]
        horizontal_line = find_horizontal_line(grid, num_smudges)
        if horizontal_line:
            # print(f' Horizontal, {horizontal_line} above out of {len(grid)}')
            total += 100 * horizontal_line
        else:

            vertical_line = find_vertical_line(grid, num_smudges)
            if vertical_line:
                # print(f' Vertical, {vertical_line} to the left out of {len(grid[0])}')
                total += vertical_line
            else:
                print('No symmetry!')
    return total

print(f'Part 1: {find_symmetry_with_smudges(0)}')
# 29907 is too low (wrong while loop condition)
# 31265 is right


print(f'Part 2: {find_symmetry_with_smudges(1)}')
# 39359
