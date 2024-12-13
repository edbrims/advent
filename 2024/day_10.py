from utils import get_input, Coords
import random
import string

use_real = True
example_input = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

directions = [Coords(0, 1), Coords(1, 0), Coords(0, -1), Coords(-1, 0)]

def height_at(position, grid):
    if position.r < 0 or position.r >= len(grid):
        return None
    if position.c < 0 or position.c >= len(grid[position.r]):
        return None
    character = grid[position.r][position.c]
    if character == ".":
        return None
    return int(character)

def rate_peaks_from(current_ratings, grid):
    if len(current_ratings) == 0:
        return current_ratings
    current_height = height_at(list(current_ratings.keys())[0], grid)
    if current_height == 9:
        return current_ratings
    next_steps = {}
    for position in current_ratings.keys():
        for direction in directions:
            next_step = position.add(direction)
            if height_at(next_step, grid) == current_height + 1:
                if next_step not in next_steps:
                    next_steps[next_step] = 0
                next_steps[next_step] += current_ratings[position]
    return rate_peaks_from(next_steps, grid)

def rate_trailheads(grid):
    total_score = 0
    total_rating = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            position = Coords(r, c)
            if height_at(position, grid) == 0:
                ratings = rate_peaks_from({position: 1}, grid)
                rating = sum(ratings.values())
                total_rating += rating
                total_score += len(ratings)
    return total_score, total_rating

grid = get_input(use_real, example_input, __file__)
total_score, total_rating = rate_trailheads(grid)

print(f'Part 1: {total_score}') # 517
print(f'Part 2: {total_rating}') # 1116


# Let's make a 3D stereogram of the landscape!
def random_char():
    return random.choice(string.ascii_letters)

def get_separation(elevation, background):
    return background - elevation

def print_stereogram(grid, square_size, background):
    grid_with_background = ["0" * (len(grid)+2)] + [f"0{row}0" for row in grid] + ["0" * (len(grid)+2)]
    for r in range(len(grid_with_background)):
        for x in range(square_size // 2):
            buffer = get_separation(0, background)
            output_row = [random_char() for i in range(buffer)]
            prev_separation = buffer
            for c in range(len(grid_with_background[r])):
                for y in range(square_size):
                    elevation = int(grid_with_background[r][c])
                    separation = get_separation(elevation, background)
                    if separation > prev_separation:
                        for i in range(separation - prev_separation):
                            output_row.append(random_char())
                    elif separation < prev_separation:
                        for i in range(prev_separation - separation):
                            output_row.pop()
                    char_to_copy = output_row[-separation]
                    output_row.append(char_to_copy)
                    prev_separation = separation
            print(''.join(output_row))

# print_stereogram(grid, 15, 50)
