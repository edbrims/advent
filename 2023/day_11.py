input = open("day_11_input.txt", "r").read()
lines = [l for l in input.split('\n') if l]

empty_rows = set(range(len(lines)))
empty_cols = set(range(len(lines[0])))
for r in range(len(lines)):
    for c in range(len(lines[r])):
        if lines[r][c] == '#':
            empty_rows.discard(r)
            empty_cols.discard(c)

# print(empty_rows)
# print(empty_cols)

def dist_between(r1, c1, r2, c2, empty_size):
    min_row = r2 # min(r1, r2)
    max_row = r1 # max(r1, r2)
    min_col = min(c1, c2)
    max_col = max(c1, c2)

    distance = (max_row - min_row) + (max_col - min_col)
    for empty_row in empty_rows:
        if min_row < empty_row and empty_row < max_row:
            distance += (empty_size - 1)
    for empty_col in empty_cols:
        if min_col < empty_col and empty_col < max_col:
            distance += (empty_size - 1)
    return distance

def measure_distances(empty_size):
    galaxy_locations = []
    total_distance = 0
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            if lines[r][c] == '#':
                for galaxy in galaxy_locations:
                    total_distance += dist_between(r, c, galaxy[0], galaxy[1], empty_size)
                galaxy_locations.append([r, c])

    return total_distance

print(f'Part 1: {measure_distances(2)}')
# 10422930
print(f'Part 2: {measure_distances(1000000)}')
# 699909023130
