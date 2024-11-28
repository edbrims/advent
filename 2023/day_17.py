import datetime

input = open("day_17_input.txt", "r").read()

#Test
# input = '''
# 2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533'''

# input = '''
# 111111111111
# 999999999991
# 999999999991
# 999999999991
# 999999999991'''

lines = [l for l in input.split('\n') if l]

# Create a graph. Nodes of the graph are
# [row, column, last direction, straight run]
queue = []
graph = {}

def make_key(r, c, dir, straight_run):
    return f'({r},{c},{dir},{straight_run})'

def get_next_straight_run(dir_now, prev_dir, prev_straight_run):
    if dir_now != prev_dir:
        return 1
    return prev_straight_run + 1

def is_opposite(dir1, dir2):
    return ((dir1 == 'U' and dir2 == 'D') or
            (dir1 == 'D' and dir2 == 'U') or
            (dir1 == 'L' and dir2 == 'R') or
            (dir1 == 'R' and dir2 == 'L'))

def attempt_move(new_r, new_c, new_dir, prev_dir, straight_run, heat_loss_to_here, min_straight, max_straight):
    if new_r < 0 or new_r >= len(lines) or new_c < 0 or new_c >= len(lines[0]):
        return

    if is_opposite(new_dir, prev_dir):
        return

    if new_dir == prev_dir and straight_run >= max_straight:
        return

    if prev_dir != '-' and new_dir != prev_dir and straight_run < min_straight:
        # print(f'Do not change {prev_dir} to {new_dir} after {straight_run} straight')
        return

    next_straight_run = get_next_straight_run(new_dir, prev_dir, straight_run)
    next_key = make_key(new_r, new_c, new_dir, next_straight_run)
    next_heat_loss = heat_loss_to_here + int(lines[new_r][new_c])
    if next_key not in graph or graph[next_key] > next_heat_loss:
        queue.append([new_r, new_c, new_dir, next_straight_run])
        graph[next_key] = next_heat_loss

def find_best_heat_loss(min_straight, max_straight):
    best_heat_loss = None
    r = 0
    c = 0
    dir = '-'
    straight_run = 0
    queue.clear()
    queue.append([r, c, dir, straight_run])
    graph.clear()
    graph[make_key(r, c, dir, straight_run)] = 0

    while queue:
        queue_entry = queue.pop(0)
        r = queue_entry[0]
        c = queue_entry[1]
        dir = queue_entry[2]
        straight_run = queue_entry[3]

        key = make_key(r, c, dir, straight_run)
        heat_loss_to_here = graph[key]

        if best_heat_loss and heat_loss_to_here > best_heat_loss:
            # No point exploring this path beyond the best finished heat loss.
            # I bet I could do more here to speed things up.
            continue

        if r == len(lines) - 1 and c == len(lines[r]) - 1 and straight_run >= min_straight:
            if not best_heat_loss or heat_loss_to_here < best_heat_loss:
                best_heat_loss = heat_loss_to_here
                # print(f'Reached bottom-right in {best_heat_loss}')

        # print(f'At {queue_entry} in {heat_loss_to_here}')

        attempt_move(r-1, c, 'U', dir, straight_run, heat_loss_to_here, min_straight, max_straight)
        attempt_move(r+1, c, 'D', dir, straight_run, heat_loss_to_here, min_straight, max_straight)
        attempt_move(r, c-1, 'L', dir, straight_run, heat_loss_to_here, min_straight, max_straight)
        attempt_move(r, c+1, 'R', dir, straight_run, heat_loss_to_here, min_straight, max_straight)
    return best_heat_loss

print(datetime.datetime.now())
print(f'Part 1: {find_best_heat_loss(-1, 3)}')
# 1008 is right!
print(datetime.datetime.now())
print(f'Part 2: {find_best_heat_loss(4, 10)}')
# 1210
print(datetime.datetime.now())

# Phew. Takes a minute or two, but it works!
# 2023-12-18 11:55:50.605443
# Part 1: 1008
# 2023-12-18 11:57:13.057725
# Part 2: 1210
# 2023-12-18 11:58:53.129686
