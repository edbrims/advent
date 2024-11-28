import copy
import datetime

input = open("day_23_input.txt", "r").read()
global_longest = 0

# Example
# input = '''
# #.#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>.>.###.#.###
# ###v#####.#v#.###.#.###
# ###.>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>.#
# #.#.#v#######v###.###v#
# #...#.>.#...>.>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>.>.#.>.###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################.#'''

grid = [l for l in input.split('\n') if l]

def make_key(r, c):
    return r * 1000 + c

def parse_key(key):
    return [key // 1000, key % 1000]

def can_move(r, c, visited):
    if r < 0 or c < 0 or r > len(grid) - 1 or c > len(grid[r]) - 1:
        return False
    if make_key(r, c) in visited:
        return False
    if grid[r][c] != '#':
        return True

    return False

def find_longest_path(initial_r, initial_c, initial_visited):
    longest = 0
    queue = [[initial_r, initial_c, initial_visited]]

    while queue:
        [r, c, visited] = queue.pop(0)
        # print(f'{r},{c} in {len(visited) - 1}. Queue is {len(queue)} long')

        visited.add(make_key(r, c))
        if r == len(grid) - 1:
            # Made it!
            distance = len(visited) - 1
            print(f'{datetime.datetime.now()}: We are at {r},{c} in {distance}. Checking {len(queue)} paths')
            longest = max(longest, distance)

        # lengths = []
        # Up
        if grid[r][c] in {'^', '.'} and can_move(r-1, c, visited):
        # if can_move(r-1, c, visited):
            queue.append([r-1, c, copy.deepcopy(visited)])
        # Down
        if grid[r][c] in {'v', '.'} and can_move(r+1, c, visited):
        # if can_move(r+1, c, visited):
            queue.append([r+1, c, copy.deepcopy(visited)])
        # Left
        if grid[r][c] in {'<', '.'} and can_move(r, c-1, visited):
        # if can_move(r, c-1, visited):
            queue.append([r, c-1, copy.deepcopy(visited)])
        # Right
        if grid[r][c] in {'>', '.'} and can_move(r, c+1, visited):
        # if can_move(r, c+1, visited):
            queue.append([r, c+1, copy.deepcopy(visited)])
    return longest

r = 0
c = grid[r].find('.')
visited = {make_key(r, c)}
# print(datetime.datetime.now())
# print(f'Part 1: {find_longest_path(r, c, visited)}')
# print(datetime.datetime.now())
# 2278 is right.


# def map_junctions(initial_r, initial_c):
#     # [3,4]
#     junctions = {make_key(initial_r, initial_c)}
#     # '3,4-9,10': 6
#     # edges = {}
#     queue = [[initial_r, initial_c, make_key(initial_r, initial_c), [0,0], 0, {make_key(initial_r, initial_c)}]]
#     while queue:
#         [r, c, previous_junction, previous_square, distance, visited] = queue.pop(0)
#         visited.add(make_key(r, c))

#         next_squares = []
#         # Up
#         if can_move(r-1, c, visited) or (make_key(r-1, c) in junctions and make_key(r-1, c) != previous_junction):
#             next_squares.append([r-1, c])
#         # Down
#         if can_move(r+1, c, visited) or (make_key(r+1, c) in junctions and make_key(r+1, c) != previous_junction):
#             next_squares.append([r+1, c])
#         # Left
#         if can_move(r, c-1, visited) or (make_key(r, c-1) in junctions and make_key(r, c-1) != previous_junction):
#             next_squares.append([r, c-1])
#         # Right
#         if can_move(r, c+1, visited) or (make_key(r, c+1) in junctions and make_key(r, c+1) != previous_junction):
#             next_squares.append([r, c+1])

#         this_key = make_key(r, c)

#         if this_key == 10021:
#             print(f'At 10,21, coming from {previous_square}. Next squares: {next_squares}')
#         if this_key == 11021:
#             print(f'At 11,21, coming from {previous_square}. Next squares: {next_squares}')

#         if r == len(grid) - 1 or len(next_squares) > 1 or this_key in junctions:
#             # We're at a junction.
#             junctions.add(this_key)

#             # if this_key != previous_junction:
#             #     edges[f'{previous_junction}-{this_key}'] = distance
#             # print(f'{len(next_squares)} ways out of {this_key}')
#             for next_square in next_squares:
#                 # print(f'{this_key} --> {next_square}')
#                 queue.append([next_square[0], next_square[1], this_key, this_key, 0, (visited)])
#         else:
#             for next_square in next_squares:
#                 queue.append([next_square[0], next_square[1], previous_junction, this_key, distance + 1, (visited)])

#     return junctions

        # if r == len(grid) - 1:
        #     # Made it!
        #     distance = len(visited) - 1
        #     print(f'{datetime.datetime.now()}: We are at {r},{c} in {distance}. Checking {len(queue)} paths')
        #     longest = max(longest, distance)

def find_junctions():
    junctions = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if can_move(r, c, {}):
                num_exits = 0
                # Up
                if can_move(r-1, c, {}):
                    num_exits += 1
                # Down
                if can_move(r+1, c, {}):
                    num_exits += 1
                # Left
                if can_move(r, c-1, {}):
                    num_exits += 1
                # Right
                if can_move(r, c+1, {}):
                    num_exits += 1
                if num_exits != 2:
                    junctions.add(make_key(r, c))
    return junctions

def measure_to_next_junction(r, c, prev_square, junctions):
    dist = 1
    while make_key(r, c) not in junctions:
        # Up
        if can_move(r-1, c, {}) and not [r-1, c] == prev_square:
            prev_square = [r, c]
            r = r-1
        # Down
        elif can_move(r+1, c, {}) and not [r+1, c] == prev_square:
            prev_square = [r, c]
            r = r+1
        # Left
        elif can_move(r, c-1, {}) and not [r, c-1] == prev_square:
            prev_square = [r, c]
            c = c-1
        # Right
        elif can_move(r, c+1, {}) and not [r, c+1] == prev_square:
            prev_square = [r, c]
            c = c+1
        dist += 1
    return [dist, make_key(r, c)]



def size_junctions(junctions):
    edges = {}
    for junction_str in junctions:
        [r, c] = parse_key(junction_str)
        edges[junction_str] = {}
        # Up
        if can_move(r-1, c, {}):
            [distance, next_junction_key] = measure_to_next_junction(r-1, c, [r, c], junctions)
            edges[junction_str][next_junction_key] = distance
        # Down
        if can_move(r+1, c, {}):
            [distance, next_junction_key] = measure_to_next_junction(r+1, c, [r, c], junctions)
            edges[junction_str][next_junction_key] = distance
        # Left
        if can_move(r, c-1, {}):
            [distance, next_junction_key] = measure_to_next_junction(r, c-1, [r, c], junctions)
            edges[junction_str][next_junction_key] = distance
        # Right
        if can_move(r, c+1, {}):
            [distance, next_junction_key] = measure_to_next_junction(r, c+1, [r, c], junctions)
            edges[junction_str][next_junction_key] = distance

    return edges


def find_longest_path_by_graph(start, target_row, edges, visited, distance_so_far, path):
    global global_longest
    [r, c] = start
    this_key = make_key(r, c)
    visited.add(this_key)
    path.append(this_key)
    if r == target_row:
        if distance_so_far > global_longest:
            global_longest = distance_so_far
            print(f'Got there in {distance_so_far} with {path}')
        return 0

    longest_onward_path = 0
    for next_junction_key in edges[this_key].keys():
        distance = edges[this_key][next_junction_key]
        if next_junction_key not in visited:
            next_junction = parse_key(next_junction_key)
            onward_path = distance + find_longest_path_by_graph(next_junction, target_row, edges, copy.deepcopy(visited), distance_so_far + distance, copy.deepcopy(path))
            if onward_path and onward_path > longest_onward_path:
                longest_onward_path = onward_path

    return longest_onward_path



junctions = find_junctions()
# print(junctions)
edges = size_junctions(junctions)
print(edges)
longest = find_longest_path_by_graph([0, 1], len(grid) - 1, edges, set(), 0, [])

print(longest)
# Longest is 6548 for a while, but that's too low.
# Then 6700 for a while. Completed on 6700 - also too low.
# [1, 15009, 33015, 37037, 5031, 7061, 43067, 55053, 67035, 57011, 77017, 101015, 133041, 125057, 123077, 133107, 107111, 101079, 109055, 103029, 77041, 89059, 81083, 85105, 61109, 33107, 39077, 7077, 19103, 31135, 59123, 81125, 107123, 127123, 140139]
# Upper bound is 9476, every path tile in the grid.

# Fixes: I was missing junctions if I hit them twice from two angles.
# Distances all off by 1 somehow.

# 6582 for ages... Then 6734:
# [1, 15009, 33015, 37037, 5031, 7061, 43067, 55053, 67035, 57011, 77017, 101015, 133041, 125057, 123077, 133107, 107111, 101079, 109055, 103029, 77041, 89059, 81083, 85105, 61109, 33107, 39077, 7077, 19103, 31135, 59123, 81125, 107123, 127123, 140139]
# 6734 is right!!!
