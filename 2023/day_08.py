import math

moves = 'LRLRLRLRRLRRRLRLRLRRRLLRRLRRLRRLLRRLRRLRLRRRLRRLLRRLRRRLRRLRRRLRRRLLLRRLLRLLRRRLLRRLRLLRLLRRRLLRRLRRLRRRLRRLRLRRLRRLRLLRLRRRLRLRRLRLLRRLRRRLRRLRLRRLLLRRLRRRLRRRLRRLRRRLRLRRLRRLRRRLRRLRRLRRLRRLRRRLLRRRLLLRRRLRRLRRRLLRRRLRRLRRLLLLLRRRLRLRRLRRLLRRLRRLRLRLRRRLRRRLRRLLLRRRR'
input = open("day_08_input.txt", "r").read()

# test input
# moves = 'LLR'
# input = '''AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)'''


# test for part 2
# moves = 'LR'
# input = '''11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)'''

lines = [l for l in input.split('\n') if l]
map = {}
for line in lines:
    [source, pair] = line.split(' = (')
    [left, right] = pair.split(', ')
    right = right[0:3]
    # print(left, right)
    map[source] = {'L': left, 'R': right}

node = 'AAA'
num_moves = 0
while node != 'ZZZ':
    options = map[node]
    direction = moves[num_moves % len(moves)]
    node = options[direction]
    num_moves += 1
print(f'Part 1: {num_moves}')
# 12643


# Part 2
# ghost_nodes = [n for n in map.keys() if n[-1] == 'A']
# num_ghosts = len(ghost_nodes)
# print(ghost_nodes)
# num_moves = 0
# while [n[-1] for n in ghost_nodes] != ['Z'] * num_ghosts:
#     for i in range(num_ghosts):
#         options = map[ghost_nodes[i]]
#         direction = moves[num_moves % len(moves)]
#         ghost_nodes[i] = options[direction]
#     num_moves += 1
#     if num_moves % 100 == 0:
#         print(f'{num_moves}: {ghost_nodes}')
# Runtime exceeded! After 2,038,800 moves
# print(f'Part 2: {num_moves}')


# Part 2 one at a time:
ghost_nodes = [n for n in map.keys() if n[-1] == 'A']
num_ghosts = len(ghost_nodes)
print(ghost_nodes)
zs_found = []
for i in range(num_ghosts):
    num_moves = 0
    node = ghost_nodes[i]
    zs_found.append([])
    while len(zs_found[i]) < 2:
        options = map[node]
        direction = moves[num_moves % len(moves)]
        node = options[direction]
        num_moves += 1
        if node[-1] == 'Z':
            # zs_found[i].append(f'{node}\t{num_moves}')
            zs_found[i].append(num_moves)

    # print(f'{ghost_nodes[i]} --> {node} in {num_moves} moves')
    # print(f'{ghost_nodes[i]} --> {zs_found}')
    # print(f'{ghost_nodes[i]}\t{zs_found[0]}\t{zs_found[1]}')

for i in range(num_ghosts):
    if zs_found[i][1] != zs_found[i][0] * 2:
        print(f'The cycle thing won\'t work: {zs_found[i]}')

print('Doing the cycle thing')
answer = math.lcm(*[z[0] for z in zs_found])

print(f'Part 2: {answer}')
# 13133452426987

# I actually did it in a spreadsheet, LCM of them all is...
# 13133452426987
# 13,133,452,426,987 is millions of times bigger than the 2 million I could check.

