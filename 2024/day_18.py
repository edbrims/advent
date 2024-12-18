from utils import get_input, XYVector

use_real = True
if use_real:
    grid_max = 70
    range_to_use = 1024
else:
    grid_max = 6
    range_to_use = 12

example_input = '''
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''

lines = get_input(use_real, example_input, __file__)
corrupted_bytes = []
for line in lines:
    parts = line.split(",")
    corrupted_bytes.append(XYVector(parts[0], parts[1]))

directions = [XYVector(0, 1), XYVector(1,  0), XYVector(0,  -1), XYVector(-1, 0)]

def print_path(path, corrupted_bytes):
    path_tiles = set(path)
    for y in range(grid_max + 1):
        row = []
        for x in range(grid_max + 1):
            square = XYVector(x, y)
            if square in path_tiles:
                row.append("O")
            elif square in corrupted_bytes:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))
    print(len(path_tiles) - 1)

def can_move(square, corrupted_bytes):
    if square.x < 0 or square.x > grid_max:
        return False
    if square.y < 0 or square.y > grid_max:
        return False
    if square in corrupted_bytes:
        return False
    return True

def find_shortest_path(corrupted_bytes, cutoff):
    first_square = XYVector(0, 0)
    queue = [[first_square, 0]]
    visited = {first_square}
    while queue:
        [square, steps_so_far] = queue.pop(0)
        if square == XYVector(grid_max, grid_max):
            # Made it!
            return steps_so_far
        for direction in directions:
            next_square = square.add(direction)
            if can_move(next_square, corrupted_bytes[:cutoff]) and next_square not in visited:
                queue.append([next_square, steps_so_far + 1])
                visited.add(next_square)
    return None

def find_first_blocker(corrupted_bytes):
    lower_bound = 0
    upper_bound = len(corrupted_bytes) - 1
    while lower_bound < upper_bound - 1:
        midpoint = (lower_bound + upper_bound) // 2
        steps = find_shortest_path(corrupted_bytes, midpoint)
        if steps:
            print(f"{midpoint} can be done in {steps}")
            lower_bound = midpoint
        else:
            print(f"{midpoint} cannot be done")
            upper_bound = midpoint
    
    first_blocker = corrupted_bytes[lower_bound]
    return f"{first_blocker.x},{first_blocker.y}"

print(f"Part 1: {find_shortest_path(corrupted_bytes, range_to_use)}") # 262
print(f"Part 2: {find_first_blocker(corrupted_bytes)}") # 22,20
