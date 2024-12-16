from collections import defaultdict
from utils import get_input, Coords
import copy

use_real = True
example_input = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''

directions = [Coords(0, 1), Coords(1,  0), Coords(0,  -1), Coords(-1, 0)]

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

def print_paths(tiles, grid):
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[r])):
            if Coords(r, c) in tiles:
                row.append("O")
            else:
                row.append(grid[r][c])
        print("".join(row))


def find_square(grid, symbol):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == symbol:
                return Coords(r, c)

def find_best_score(grid):
    start_square = find_square(grid, "S")
    end_square = find_square(grid, "E")
    direction = Coords(0, 1)
    state = State(start_square, direction)
    best_score = 1e9

    # For each state, the lowest score to get there.
    lowest_scores = defaultdict(lambda: [1e9, set()])
    queue = [[state, 0, [start_square]]]
    while queue:
        [state, score_so_far, path_to_here] = queue.pop(0)

        if score_so_far < lowest_scores[state][0]:
            lowest_scores[state] = [score_so_far, set(path_to_here)]
        elif score_so_far == lowest_scores[state][0]:
            lowest_scores[state][1] = lowest_scores[state][1].union(path_to_here)
        else:
            continue

        if grid[state.position.r][state.position.c] == "E":
            tiles_on_best_path = len(lowest_scores[state][1])
            print(f"Reached the end in {score_so_far}")
            if score_so_far < best_score:
                best_score = score_so_far
                continue

        # Straight ahead
        square_ahead = state.position.add(state.vector)
        if grid[square_ahead.r][square_ahead.c] in [".", "E"]:
            next_state = State(square_ahead, state.vector)
            if score_so_far + 1 <= lowest_scores[next_state][0] and score_so_far + 1 <= best_score:
                queue.append([next_state, score_so_far + 1, path_to_here + [square_ahead]])
        
        # Turning
        score_after_turning = score_so_far + 1000
        state_to_left = State(state.position, state.vector.turn_left())
        if score_after_turning <= lowest_scores[state_to_left][0] and score_after_turning <= best_score:
            queue.append([state_to_left, score_after_turning, path_to_here])
        state_to_right = State(state.position, state.vector.turn_right())
        if score_after_turning <= lowest_scores[state_to_right][0] and score_after_turning <= best_score:
            queue.append([state_to_right, score_after_turning, path_to_here])

    tiles_on_best_paths = set()
    for direction in directions:
        state = State(end_square, direction)
        low_score_for_state = lowest_scores[state]
        if low_score_for_state[0] == best_score:
            tiles_on_best_paths = tiles_on_best_paths.union(low_score_for_state[1])
    
    print_paths(tiles_on_best_paths, grid)

    return best_score, len(tiles_on_best_paths)

grid = get_input(use_real, example_input, __file__)
[best_score, tiles_on_best_paths] = find_best_score(grid)

print(f"Part 1: {best_score}") # 85432
print(f"Part 2: {tiles_on_best_paths}") # 465
