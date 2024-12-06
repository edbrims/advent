from input_loader import get_input

use_real = True
example_input = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

grid = get_input(use_real, example_input, __file__)

class Coords:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def add(self, vector):
        return Coords(self.r + vector.r, self.c + vector.c)

    def __repr__(self):
        return f'({self.r}, {self.c})'

    def __eq__(self, __value: object) -> bool:
        return self.r == __value.r and self.c == __value.c

    def __hash__(self) -> int:
        return self.r + self.c * 1000

class State:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector

    def __repr__(self):
        return f'({self.position} -> {self.vector})'

    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position and self.vector == __value.vector

    def __hash__(self) -> int:
        return self.position.__hash__() + self.vector.__hash__() * 1000000

def find_start():
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '^':
                return Coords(r, c)
    return None

def is_block(coords, grid):
    if coords.r < 0 or coords.c < 0 or coords.r >= len(grid) or coords.c >= len(grid[coords.r]):
        return False
    return (grid[coords.r][coords.c] == '#')

def turn_right(vector):
    return Coords(vector.c, -vector.r)

def print_grid(grid, visited):
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[r])):
            if Coords(r, c) in visited:
                row.append('X')
            else:
                row.append(grid[r][c])
        print(''.join(row))

def get_visited_positions(grid):
    position = find_start()

    visited = set()
    vector = Coords(-1, 0) # Row move, column move
    while position.r >= 0 and position.c >= 0 and position.r < len(grid) and position.c < len(grid[position.r]):
        visited.add(position)
        square_ahead = position.add(vector)
        if is_block(square_ahead, grid):
            vector = turn_right(vector)
        else:
            position = square_ahead

    # print_grid(grid, visited)
    return visited

def gives_loop(grid, extra_block):
    position = find_start()

    visited = set()
    states = set()
    vector = Coords(-1, 0) # Row move, column move
    while position.r >= 0 and position.c >= 0 and position.r < len(grid) and position.c < len(grid[position.r]):
        visited.add(position)
        state = State(position, vector)
        if state in states:
            return True
        states.add(state)
        square_ahead = position.add(vector)
        if is_block(square_ahead, grid) or square_ahead == extra_block:
            vector = turn_right(vector)
        else:
            position = square_ahead
    return False

def count_loops(grid):
    count = 0
    positions_to_check = get_visited_positions(grid)
    for block_position in positions_to_check:
        if grid[block_position.r][block_position.c] == '.' and gives_loop(grid, block_position):
            print(f'You get a loop with a block at {block_position}')
            count += 1
    return count

print(f'Part 1: {len(get_visited_positions(grid))}')
print(f'Part 2: {count_loops(grid)}')
