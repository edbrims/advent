import datetime

input = open("day_21_input.txt", "r").read()

# Example
# input = '''
# ...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ...........'''

rows = [l for l in input.split('\n') if l]
height = len(rows)
width = len(rows[0])
start_pos = (height - 1) // 2 # You start right in the middle
if rows[start_pos][start_pos] != 'S':
    print(f'({start_pos},{start_pos}) is {rows[start_pos][start_pos]} instead of S')

def coord_string(r, c):
    return f'{r},{c}'

def can_step(r, c, part_number):
    if part_number == 1:
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
    return rows[r % height][c % width] != '#'

def get_next_steps(r, c, part_number):
    next_steps = []
    # Up
    if can_step(r-1, c, part_number):
        next_steps.append([r-1, c])
    # Left
    if can_step(r, c-1, part_number):
        next_steps.append([r, c-1])
    # Down
    if can_step(r+1, c, part_number):
        next_steps.append([r+1, c])
    # Right
    if can_step(r, c+1, part_number):
        next_steps.append([r, c+1])
    return next_steps

def count_squares(steps_wanted, part_number):
    squares_at_step = []
    new_positions = {coord_string(start_pos, start_pos)}
    for i in range(max(steps_wanted)):
        num_steps = i + 1
        old_positions = new_positions
        new_positions = set()
        for starting_point in old_positions:
            r_str, c_str = starting_point.split(',')
            for [r2, c2] in get_next_steps(int(r_str), int(c_str), part_number):
                new_positions.add(coord_string(r2, c2))
        if num_steps in steps_wanted:
            squares_at_step.append(len(new_positions))
    return squares_at_step


# Part 1
print(f'Part 1: {count_squares([64], 1)[0]}')
# 3637 is right

# Part 2
print(datetime.datetime.now())
# The grid is 131*131, and it takes the first 65 moves to fill the first square.
# We want step 26501365, which is 131*202300 + 65.
# Let's grab the first few 131*n + 65 and extrapolate.
#
# Get the first four points in the cycle. Three is enough to get the differences, but let's
# do one more to make sure it really is quadratic. Doing five takes 7 minutes.
points_wanted = 4
num_positions = count_squares(list(range(start_pos, (points_wanted + 1) * height, height)), 2)
print(datetime.datetime.now())

# Do the differencey thing:
# n	Answer	Diff	2nd diff
# 0	3699	29438	29376
# 1	33137	58814	29376
# 2	91951	88190	29376
# 3	180141	117566	29376
#
# Formula is 3699 + 29438n + 29376*sum(1..n-1)
#          = 3699 + 29438n + 29376*n(n-1)/2
# Plug in n = 202300

first_differences = []
for i in range(len(num_positions) - 1):
    first_differences.append(num_positions[i+1] - num_positions[i])

second_differences = []
for i in range(len(first_differences) - 1):
    second_differences.append(first_differences[i+1] - first_differences[i])

if max(second_differences) != min(second_differences):
    print(f'This differences thing doesn\'t work. Second diffs range from {min(second_differences)} to {max(second_differences)}')

steps_wanted = 26501365
term_wanted = (steps_wanted - start_pos) // height

squares = num_positions[0] + first_differences[0] * term_wanted + second_differences[1] * term_wanted * (term_wanted - 1) // 2

print(f'Part 2: {squares}')
# Answer: 601113643448699
# Right!
