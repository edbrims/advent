input = open("day_16_input.txt", "r").read()

# input = open("day_16_example.txt", "r").read()

lines = [l for l in input.split('\n') if l]

def print_grid(visited):
    grid = []
    for r in range(len(lines)):
        row = []
        for c in range(len(lines[0])):
            if f'({r}, {c})' in visited:
                row.append(lines[r][c])
            else:
                row.append(' ')
        grid.append(''.join(row))
    print('\n'.join(grid))



def count_visited_cells(starting_ray):

    # Row, col, down, right
    # rays = [[0,-1,0,1]]
    rays = [starting_ray]
    visited = set()
    vectors_seen = set()

    steps = 0
    while rays: # and steps < 1000:
        steps += 1
        dead_rays = []
        for i in range(len(rays)):
            # move mark turn
            rays[i][0] += rays[i][2]
            rays[i][1] += rays[i][3]

            vector_str = f'({rays[i][0]}, {rays[i][1]}, {rays[i][2]}, {rays[i][3]})'
            if vector_str in vectors_seen or rays[i][0] < 0 or rays[i][0] >= len(lines) or rays[i][1] < 0 or rays[i][1] >= len(lines[0]):
                dead_rays.append(i)
                continue
            visited.add(f'({rays[i][0]}, {rays[i][1]})')
            vectors_seen.add(vector_str)

            content = lines[rays[i][0]][rays[i][1]]
            if content == '/':
                down = -rays[i][3]
                rays[i][3] = -rays[i][2]
                rays[i][2] = down
            elif content == '\\':
                down = rays[i][3]
                rays[i][3] = rays[i][2]
                rays[i][2] = down
            elif content == '-' and rays[i][2] != 0:
                rays[i][2] = 0
                rays[i][3] = 1
                rays.append([rays[i][0], rays[i][1], 0, -1])
            elif content == '|' and rays[i][3] != 0:
                rays[i][2] = 1
                rays[i][3] = 0
                rays.append([rays[i][0], rays[i][1], -1, 0])


        for i in dead_rays[::-1]:
            del(rays[i])
    # print_grid(visited)

    return len(visited)

def get_maximum():
    best = 0
    for row in range(len(lines)):
        visited = count_visited_cells([row,-1,0,1])
        if visited > best:
            best = visited
        visited = count_visited_cells([row,len(lines[0]),0,-1])
        if visited > best:
            best = visited

    for col in range(len(lines[0])):
        visited = count_visited_cells([-1,col,1,0])
        if visited > best:
            best = visited
        visited = count_visited_cells([len(lines[0]),col,-1,0])
        if visited > best:
            best = visited
    return best

# print(f'visited {visited}')
print(f'Part 1: {count_visited_cells([0,-1,0,1])}')
# 195 too low
# 162 in 100 turns
print(f'Part 2: {get_maximum()}')
