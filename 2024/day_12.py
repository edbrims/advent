from utils import get_input, Coords

use_real = True
example_input = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

directions = [Coords(0, 1), Coords(1,  0), Coords(0,  -1), Coords(-1, 0)]
diagonals  = [Coords(1, 1), Coords(1, -1), Coords(-1, -1), Coords(-1, 1)]

def plant_at(position, grid):
    if position.r < 0 or position.r >= len(grid):
        return None
    if position.c < 0 or position.c >= len(grid[position.r]):
        return None
    return grid[position.r][position.c]

def get_region(start_square, grid):
    plants = plant_at(start_square, grid)
    region = {start_square}
    queue = [start_square]
    while queue:
        square = queue.pop(0)
        for direction in directions:
            neighbour = square.add(direction)
            if neighbour not in region and plant_at(neighbour, grid) == plants:
                queue.append(neighbour)
                region.add(neighbour)
    return region

def find_regions(grid):
    unassigned_squares = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            unassigned_squares.add(Coords(r, c))

    regions = []
    while unassigned_squares:
        next_region = get_region(unassigned_squares.pop(), grid)
        regions.append(next_region)
        for square in next_region:
            unassigned_squares.discard(square)
    return regions

def measure_perimeter(region):
    perimeter = 0
    for square in region:
        for direction in directions:
            if square.add(direction) not in region:
                perimeter += 1
    return perimeter

def count_corners(region):
    num_corners = 0
    for square in region:
        # Check if the square's four corners are corners of the region.
        for diagonal in diagonals:
            # It's a convex corner if the two adjacent squares are outside the region.
            if (square.add(Coords(diagonal.r, 0)) not in region and
                square.add(Coords(0, diagonal.c)) not in region):
                num_corners += 1

            # It's a concave corner if the two adjacent squares are inside with the diagonal square outside.
            elif (square.add(diagonal) not in region and
                  square.add(Coords(diagonal.r, 0)) in region and
                  square.add(Coords(0, diagonal.c)) in region):
                num_corners += 1

    return num_corners

# This way is fun but doesn't work, because it misses the internal boundaries.
def count_sides_by_crawling(region):
    # Crawl around the border from a top edge
    starting_square = Coords(1000, 0)
    for square in region:
        if square.r < starting_square.r:
            starting_square = square
    # Face east, keeping your right foot inside the region.
    direction = Coords(0, 1)

    num_turns = 0
    first = True
    right_foot_square = starting_square
    while right_foot_square != starting_square or direction != Coords(0, 1) or first:
        first  = False
        ahead_right = right_foot_square.add(direction)
        ahead_left = ahead_right.add(direction.turn_left())
        if ahead_right not in region:
            # Turn right, right foot stays in the same square
            direction = direction.turn_right()
            num_turns += 1
        elif ahead_left in region:
            # Turn left, right foot is now ahead left.
            direction = direction.turn_left()
            right_foot_square = ahead_left
            num_turns += 1
        else:
            # Go straight
            right_foot_square = ahead_right
    return num_turns

def price_region_by_perimeter(region):
    area = len(region)
    perimeter = measure_perimeter(region)
    return area * perimeter

def price_region_by_sides(region):
    area = len(region)
    sides = count_corners(region)
    return area * sides

def price_regions_by_perimeter(regions):
    return sum([price_region_by_perimeter(r) for r in regions])

def price_regions_by_sides(regions):
    return sum([price_region_by_sides(r) for r in regions])

grid = get_input(use_real, example_input, __file__)
regions = find_regions(grid)

print(f"Part 1: {price_regions_by_perimeter(regions)}") # 1473276
print(f"Part 2: {price_regions_by_sides(regions)}") # 901100
