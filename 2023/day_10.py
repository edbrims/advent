input = open("day_10_input.txt", "r").read()
# Start
r = 98
c = 90

# input = '''-L|F7
# 7S-7|
# L|7||
# -L-J|
# L|-JF'''
# r = 1
# c = 1

lines = [l for l in input.split('\n') if l]

def mark_interior(colouring_grid, r, c):
    # print(r)
    if r >= len(colouring_grid) or r < 0:
        return
    if c >= len(colouring_grid[r]) or c < 0:
        return
    if colouring_grid[r][c] == '·':
        colouring_grid[r][c] = '█'

def fill_interior(colouring_grid):
    for r in range(1, len(colouring_grid) - 1):
        for c in range(1, len(colouring_grid[r]) - 1):
            if colouring_grid[r][c] == '·':
                if colouring_grid[r-1][c] == '█' or colouring_grid[r+1][c] == '█' or colouring_grid[r][c-1] == '█' or colouring_grid[r][c+1] == '█':
                    colouring_grid[r][c] = '█'

# colouring_grid = [['E'] * len(lines[0])] * len(lines)
colouring_grid = [ ['·'] * len(lines[0]) for i in range(len(lines))]
colouring_grid[r][c] = 'S' # 'S'

# Start by moving down
right_turns = 0
left_turns = 0
prev_r = r
prev_c = c
r += 1
steps = 1
while lines[r][c] != 'S':
    colouring_grid[r][c] = '.' # lines[r][c]
    symbol = lines[r][c]
    # print(f'Moved to {symbol}')
    if symbol == '-':
        colouring_grid[r][c] = '─'
        if prev_c > c:
            # colouring_grid[r][c] = '←'
            mark_interior(colouring_grid, r+1, c)
            prev_c = c
            c -= 1
        else:
            # colouring_grid[r][c] = '→'
            mark_interior(colouring_grid, r-1, c)
            prev_c = c
            c += 1
    elif symbol == '|':
        colouring_grid[r][c] = '│'
        if prev_r > r:
            # colouring_grid[r][c] = '↑'
            mark_interior(colouring_grid, r, c-1)
            prev_r = r
            r -= 1
        else:
            # colouring_grid[r][c] = '↓'
            mark_interior(colouring_grid, r, c+1)
            prev_r = r
            r += 1
    elif symbol == 'F':
        colouring_grid[r][c] = '┌'
        if prev_c > c:
            mark_interior(colouring_grid, r+1, c+1)
            prev_r = r
            prev_c = c
            r += 1
            left_turns += 1
        else:
            mark_interior(colouring_grid, r, c-1)
            mark_interior(colouring_grid, r-1, c-1)
            mark_interior(colouring_grid, r-1, c)
            prev_r = r
            prev_c = c
            c += 1
            right_turns += 1
    elif symbol == '7':
        colouring_grid[r][c] = '┐'
        if prev_c < c:
            mark_interior(colouring_grid, r-1, c)
            mark_interior(colouring_grid, r-1, c+1)
            mark_interior(colouring_grid, r, c+1)
            prev_r = r
            prev_c = c
            r += 1
            right_turns += 1
        else:
            mark_interior(colouring_grid, r+1, c-1)
            prev_r = r
            prev_c = c
            c -= 1
            left_turns += 1
    elif symbol == 'J':
        colouring_grid[r][c] = '┘'
        if prev_c < c:
            mark_interior(colouring_grid, r-1, c-1)
            prev_r = r
            prev_c = c
            r -= 1
            left_turns += 1
        else:
            mark_interior(colouring_grid, r+1, c)
            mark_interior(colouring_grid, r+1, c+1)
            mark_interior(colouring_grid, r, c+1)
            prev_r = r
            prev_c = c
            c -= 1
            right_turns += 1
    elif symbol == 'L':
        colouring_grid[r][c] = '└'
        if prev_c > c:
            mark_interior(colouring_grid, r+1, c)
            mark_interior(colouring_grid, r+1, c-1)
            mark_interior(colouring_grid, r, c-1)
            prev_r = r
            prev_c = c
            r -= 1
            right_turns += 1
        else:
            mark_interior(colouring_grid, r-1, c+1)
            prev_r = r
            prev_c = c
            c += 1
            left_turns += 1
    steps += 1
    # print(f'{steps}: {r},{c}: {lines[r][c]}')
# print(f'{steps} steps in the loop')
# print(f'Turned left {left_turns}, right {right_turns}')

# Turned left 4356, right 4352
# So it's anticlockwise, interior on your left.

fill_interior(colouring_grid)
interior = 0
for row in colouring_grid:
    # print(''.join(row))
    for ch in row:
        if ch == '█':
            interior += 1

print(f'Part 1: {steps//2}')
print(f'Part 2: {interior}')

