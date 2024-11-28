import random

input = open("day_25_input.txt", "r").read()

# Example
# input = '''
# jqt: rhn xhk nvd
# rsh: frs pzl lsr
# xhk: hfx
# cmg: qnr nvd lhk bvb
# rhn: xhk bvb hfx
# bvb: xhk hfx
# pzl: lsr hfx nvd
# qnr: nvd
# ntq: jqt hfx bvb xhk
# nvd: lhk
# lsr: lhk
# rzs: qnr cmg lsr rsh
# frs: qnr lhk lsr'''

lines = [l for l in input.split('\n') if l]

# class Wire:
#     def __init__(self, ends):
#         self.start = min(ends)
#         self.end = max(ends)

#     def __repr__(self):
#         return f'({self.start}-{self.end})'


connections = {}

def connect(a, b, connections):
    if a not in connections:
        connections[a] = set()
    if b not in connections:
        connections[b] = set()
    # wire = Wire([a, b])
    # wire = f'{min(a,b)}-{max(a,b)}'
    connections[a].add(b)
    connections[b].add(a)

def disconnect(a, b, connections):
    # ends = wire.split('-')
    # connections[ends[0]].discard(wire)
    # connections[ends[1]].discard(wire)
    connections[a].discard(b)
    connections[b].discard(a)

for line in lines:
    # print(line)
    [source, dests] = line.split(': ')
    for d in dests.split(' '):
        connect(source, d, connections)
# wires = set.union(*connections.values())
# print((connections))
# print((wires))

def find_route(source, target, connections):
    queue = [[source]]
    visited = set()
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        for next_node in connections[node]:
            if next_node in visited:
                continue
            next_path = path + [next_node]
            if next_node == target:
                return next_path
            queue.append(next_path)
    return None

wire_counts = {}
for i in range(1000):
    nodes = list(connections.keys())
    source = random.choice(nodes)
    target = random.choice(nodes)
    path = find_route(source, target, connections)
    if path:
        for i in range(len(path) - 1):
            wire = f'{min(path[i], path[i+1])}-{max(path[i], path[i+1])}'
            if wire in wire_counts:
                wire_counts[wire] += 1
            else:
                wire_counts[wire] = 1

wires = list(wire_counts.keys())
wires.sort(key=lambda w: wire_counts[w], reverse=True)
for wire in wires[:3]:
    print(f'{wire}: {wire_counts[wire]}')
    ends = wire.split('-')
    disconnect(ends[0], ends[1], connections)
# The three "hottest" wires are
# cfn-jkn: 1437
# gst-rph: 1594
# ljm-sfd: 1954
# print(find_route('ntq', 'lsr', connections))

def count_nodes(source, connections):
    queue = [source]
    visited = set()
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for next_node in connections[node]:
            if next_node in visited:
                continue
            queue.append(next_node)
    return len(visited  )


# disconnect('cfn', 'jkn', connections)
# disconnect('gst', 'rph', connections)
# disconnect('ljm', 'sfd', connections)

one_size = count_nodes('cfn', connections)
other_size = count_nodes('jkn', connections)

print(f'Part 1: {one_size * other_size}')
# 596376 is right!

# Part 2
# There is no part 2 for Christmas.
