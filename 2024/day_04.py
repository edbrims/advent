from utils import get_input

use_real = True
example_input = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''

lines = get_input(use_real, example_input, __file__)

def get_vectors():
    vectors = []
    for u in range(-1, 2):
        for v in range(-1, 2):
            if u != 0 or v != 0:
                vectors.append([u, v])
    return vectors

def letter_is_at(letter, lines, row, col):
    if row < 0 or row >= len(lines):
        return False
    if col < 0 or col >= len(lines[row]):
        return False
    return (lines[row][col] == letter)

def letter_is_at_by_vector(letter, lines, x_row, x_col, unit_vector, multiplier):
    vector = [i * multiplier for i in unit_vector]
    row = x_row + vector[0]
    col = x_col + vector[1]
    return letter_is_at(letter, lines, row, col)

def count_from_x(lines, x_row, x_col):
    count = 0
    unit_vectors = get_vectors()
    for unit_vector in unit_vectors:
        if (letter_is_at_by_vector('M', lines, x_row, x_col, unit_vector, 1) and
            letter_is_at_by_vector('A', lines, x_row, x_col, unit_vector, 2) and
            letter_is_at_by_vector('S', lines, x_row, x_col, unit_vector, 3)):
            count += 1
    return count

def count_xmas(lines):
    count = 0
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == 'X':
                count += count_from_x(lines, r, c)
    return count

print(f'Part 1: {count_xmas(lines)}') # 2571


def crossing_around_a(lines, r, c):
    # Both opposite pairs of corners have to be M and S, either way round.
    return ({lines[r-1][c-1], lines[r+1][c+1]} == {'M', 'S'} and
            {lines[r+1][c-1], lines[r-1][c+1]} == {'M', 'S'})

def count_mas_crossings(lines):
    count = 0
    for r in range(1, len(lines) - 1):
        for c in range(1, len(lines[r]) - 1):
            if lines[r][c] == 'A' and crossing_around_a(lines, r, c):
                count += 1
    return count

print(f'Part 2: {count_mas_crossings(lines)}') # 1992
