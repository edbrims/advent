import copy

input = '''
AABBBCCCCC
AAABBBCCCC
AABBBEDDDD
AEEEEEFFFD
EEEEGGFDFD
EHHGGGGDDD
HHGGGGGDII
HGGGJJGGII
HGGGJGGGGI
HHHGJGGGGI
'''

num_per_row_col_region = 2

grid = [l for l in input.split('\n') if l]

def clear_around(positions, row, col):
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if r >= 0 and r < len(positions) and c >= 0 and c < len(positions[r]) and positions[r][c] == 'W':
                return False
    return True

def print_positions(positions):
    for row in positions:
        print(''.join(row))

def solve_recursive(grid, positions, next_r, next_c, row_counts, col_counts, num_per_region):
    num_placed = sum(row_counts)
    if num_placed == num_per_row_col_region * len(grid):
        print('Finished!')
        print_positions(positions)
        return
    for r in range(next_r, len(grid)):
        if r > 0 and row_counts[r-1] != num_per_row_col_region:
            # We didn't place two in the previous row. Nothing can work from here.
            return
        for c in range(len(grid[r])):
            if r == next_r and c < next_c:
                continue
            if row_counts[r] >= num_per_row_col_region or col_counts[c] >= num_per_row_col_region:
                continue
            if num_per_region[grid[r][c]] >= num_per_row_col_region:
                continue
            if not clear_around(positions, r, c):
                continue
            # Try it here.
            new_positions = copy.deepcopy(positions)
            new_positions[r][c] = 'W'
            new_row_counts = row_counts.copy()
            new_row_counts[r] += 1
            new_col_counts = col_counts.copy()
            new_col_counts[c] += 1
            new_num_per_region = copy.deepcopy(num_per_region)
            new_num_per_region[grid[r][c]] += 1
            solve_recursive(grid, new_positions, r, c + 2, new_row_counts, new_col_counts, new_num_per_region)

def solve(grid):
    num_per_region = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0}
    positions = [['.'] * len(grid[i]) for i in range(len(grid))]

    solve_recursive(grid, positions, 0, 0, [0] * len(grid), [0] * len(grid[0]), num_per_region)

solve(grid)
