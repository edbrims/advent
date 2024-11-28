input = open("day_18_input.txt", "r").read()

# Example
# input = '''
# R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)'''

lines = [l for l in input.split('\n') if l]

def is_interior(r, c, grid, top, bottom, left, right):
    if (read_at(r-1, c, grid, top, left) == 'I' or
        read_at(r+1, c, grid, top, left) == 'I' or
        read_at(r, c-1, grid, top, left) == 'I' or
        read_at(r, c+1, grid, top, left) == 'I'):
        return True
    return False

def fill_interior(grid, top, bottom, left, right):
    for r in range(top, bottom):
        for c in range(left, right):
            if read_at(r, c, grid, top, left) == '.':
                if read_at(r, c, grid, top, left) and is_interior(r, c, grid, top, bottom, left, right):
                    place_at('I', r, c, grid, top, left)

def count_grid(grid):
    count = 0
    for row in grid:
        for c in row:
            if c == '#' or c == 'I':
                count += 1
    return count

def get_instructions(lines, part_number):
    directions = []
    for line in lines:
        parts = line.split(' ')
        if part_number == 1:
            direction = parts[0]
            # Vector: Row, column
            if direction == 'U':
                vector = [-1, 0]
            elif direction == 'D':
                vector = [1, 0]
            elif direction == 'L':
                vector = [0, -1]
            elif direction == 'R':
                vector = [0, 1]
            distance = int(parts[1])
        elif part_number == 2:
            # parts[2] is of the form (#1c0d23)
            distance = int(parts[2][2:7], 16)
            direction_code = int(parts[2][7])

            # Vector: Row, column
            if direction_code == 3:
                direction = 'U'
                vector = [-1, 0]
            elif direction_code == 1:
                direction = 'D'
                vector = [1, 0]
            elif direction_code == 2:
                direction = 'L'
                vector = [0, -1]
            elif direction_code == 0:
                direction = 'R'
                vector = [0, 1]
        directions.append({'direction': direction, 'vector': vector, 'distance': distance})
    return directions

def get_bounds(instructions):
    top = 0
    bottom = 0
    left = 0
    right = 0
    position = [0,0]
    for instruction in instructions:
        # direction = instruction['direction']
        vector = instruction['vector']
        distance = instruction['distance']
        position = [position[c] + vector[c] * distance for c in range(2)]

        if position[0] < top:
            top = position[0]
        elif position[0] > bottom:
            bottom = position[0]
        elif position[1] < left:
            left = position[1]
        elif position[1] > right:
            right = position[1]
    # print(f'Top {top}, bottom {bottom}, left {left}, right {right}')
    return [top, bottom, left, right]

def place_at(char, r, c, grid, top, left):
    grid[r - top][c - left] = char
def read_at(r, c, grid, top, left):
    return grid[r - top][c - left]
def place_if_clear(char, r, c, grid, top, left):
    if read_at(r, c, grid, top, left) == '.':
        place_at(char, r, c, grid, top, left)

def populate_grid_part_1():
    instructions = get_instructions(lines, 1)
    [top, bottom, left, right] = get_bounds(instructions)
    grid = [['.'] * (right - left + 1) for i in range(top, bottom + 1)]
    place_at('#', 0, 0, grid, top, left)
    position = [0,0]

    for instruction in instructions:
        direction = instruction['direction']
        vector = instruction['vector']
        distance = instruction['distance']

        for i in range(distance):
            position = [position[c] + vector[c] for c in range(2)]
            place_at('#', position[0], position[1], grid, top, left)
            place_if_clear('I', position[0] + vector[1], position[1] - vector[0], grid, top, left)

    fill_interior(grid, top, bottom, left, right)
    return grid

grid = populate_grid_part_1()
print(f'Part 1: {count_grid(grid)}')
# 56939 is too high.
# 52231 is right.

# Part 2
def measure_area(part_number):
    instructions = get_instructions(lines, part_number)
    [top, bottom, left, right] = get_bounds(instructions)
    position = [0,0]

    instruction_number = 0

    nodes = [position]
    sum_edge_lengths = 0

    for instruction in instructions:
        instruction_number += 1
        direction = instruction['direction']
        vector = instruction['vector']
        distance = instruction['distance']

        sum_edge_lengths += distance

        position = [position[c] + vector[c] * distance for c in range(2)]
        nodes.append(position)

    # Ummm.
    # The shoelace formula seems to be the answer, but I bet there are fencepost oddities.
    double_area = 0
    for i in range(len(nodes)):
        next_i = (i+1) % len(nodes)
        # Negative determinant - I guess that tells you if we're going clockwise or anticlockwise?
        double_area += nodes[i][1]*nodes[next_i][0] - nodes[i][0]*nodes[next_i][1]

    # Area of the outside half of the boundary is the sum of half the edge lengths
    # plus 1 (four double-counted quarter-squares; otherwise all the right turns
    # and left turns cancel each other out).
    area_of_outside_half_of_boundary = sum_edge_lengths // 2 + 1

    # The area from the shoelace formula is bordered by the middle line
    # of the boundary, so we need to add the outside half of the boundary.
    return double_area // 2 + area_of_outside_half_of_boundary

print(f'Part 1: {measure_area(1)}')
print(f'Part 2: {measure_area(2)}')
# 57196493937398 is right!
