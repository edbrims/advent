import copy
from utils import get_input, XYVector

use_real = True
if use_real:
    width = 101
    height = 103
else:
    width = 11
    height = 7

example_input = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

class Robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def move(self, seconds):
        self.position = self.position.add(self.velocity.times(seconds))
        self.position.x = self.position.x % width
        self.position.y = self.position.y % height

    def __repr__(self):
        return f"[{self.position}->{self.velocity}]"

def make_grid(robots):
    grid = [[0] * width for i in range(height)]
    for robot in robots:
        grid[robot.position.y][robot.position.x] += 1
    return grid

def print_robots(robots):
    for row in make_grid(robots):
        print("".join([str(r) for r in row]))

def load_robots(lines):
    robots = []
    for line in lines:
        parts = line.split(" ")
        position_coords = parts[0][2:].split(",")
        velocity_coords = parts[1][2:].split(",")
        position = XYVector(position_coords[0], position_coords[1])
        velocity = XYVector(velocity_coords[0], velocity_coords[1])
        robots.append(Robot(position, velocity))
    return robots

def move_robots(robots, seconds):
    for robot in robots:
        robot.move(seconds)
    return robots

def quadrants_after_seconds(robots, seconds):
    robots = copy.deepcopy(robots)
    move_robots(robots, seconds)
    middle_row = (height - 1) // 2
    middle_col = (width - 1) // 2
    top_left = top_right = bottom_left = bottom_right = 0
    for robot in robots:
        if robot.position.x < middle_col and robot.position.y < middle_row:
            top_left += 1
        if robot.position.x > middle_col and robot.position.y < middle_row:
            top_right += 1
        if robot.position.x < middle_col and robot.position.y > middle_row:
            bottom_left += 1
        if robot.position.x > middle_col and robot.position.y > middle_row:
            bottom_right += 1
    return (top_left * top_right * bottom_left * bottom_right)

directions = [XYVector(0, 1), XYVector(1,  0), XYVector(0,  -1), XYVector(-1, 0)]

def num_at(position, grid):
    if position.y < 0 or position.y >= height:
        return 0
    if position.x < 0 or position.x >= width:
        return 0
    return grid[position.y][position.x]

def get_region(start_square, grid):
    region = {start_square}
    queue = [start_square]
    while queue:
        square = queue.pop(0)
        for direction in directions:
            neighbour = square.add(direction)
            if neighbour not in region and num_at(neighbour, grid) > 0:
                queue.append(neighbour)
                region.add(neighbour)
    return region


def could_be_christmas_tree(robots):
    grid = make_grid(robots)

    regions = []
    unassigned_squares = {r.position for r in robots}
    while unassigned_squares:
        next_region = get_region(unassigned_squares.pop(), grid)
        regions.append(next_region)
        for square in next_region:
            unassigned_squares.discard(square)
    lengths = [len(r) for r in regions]
    if max(lengths) > 50:
        print([r for r in lengths if r > 50])
        return True
    return False

def seconds_to_christmas_tree(robots):
    robots = copy.deepcopy(robots)
    for t in range(1, 100000):
        for robot in robots:
            robot.move(1)
        if could_be_christmas_tree(robots):
            print(f"At {t} seconds there's a big region")
            print_robots(robots)
            return t
        elif t % 100 == 0:
            print(f"{t}: Nope")
    return None


lines = get_input(use_real, example_input, __file__)
robots = load_robots(lines)

print(f"Part 1: {quadrants_after_seconds(robots, 100)}") # 222062148
print(f"Part 2: {seconds_to_christmas_tree(robots)}") # 7520
# ... and then it repeats every 10,403
