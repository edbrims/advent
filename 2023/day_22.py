import copy
import datetime

input = open("day_22_input.txt", "r").read()

# Example
# input = '''
# 1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9'''

class Coords:
    def __init__(self, coords):
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.z = int(coords[2])

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

class Block:
    def __init__(self, one_end, other_end, name):
        self.one_end = one_end
        self.other_end = other_end
        self.name = name
        self.blocks_above = set()
        self.blocks_below = set()
        self.is_vertical = one_end.z != other_end.z
        self.direction = 'x' if one_end.x != other_end.x else 'y' if one_end.y != other_end.y else 'z' if one_end.z != other_end.z else '.'
        self.num_blocks = abs(one_end.x - other_end.x) + abs(one_end.y - other_end.y) + abs(one_end.z - other_end.z) + 1
    def lowest_point(self):
        return min(self.one_end.z, self.other_end.z)
    def highest_point(self):
        return max(self.one_end.z, self.other_end.z)
    def move_down(self, how_far):
        self.one_end.z -= how_far
        self.other_end.z -= how_far
    def footprint(self):
        footprint = []
        if self.direction == 'x':
            for x in range(min(self.one_end.x, self.other_end.x), max(self.one_end.x, self.other_end.x) + 1):
                footprint.append(Coords([x, self.one_end.y, 0]))
        elif self.direction == 'y':
            for y in range(min(self.one_end.y, self.other_end.y), max(self.one_end.y, self.other_end.y) + 1):
                footprint.append(Coords([self.one_end.x, y, 0]))
        else:
            footprint.append(Coords([self.one_end.x, self.one_end.y, 0]))
        return footprint
    def blocks(self):
        blocks = []
        if self.direction == 'x':
            for x in range(min(self.one_end.x, self.other_end.x), max(self.one_end.x, self.other_end.x) + 1):
                blocks.append(Coords([x, self.one_end.y, self.one_end.z]))
        elif self.direction == 'y':
            for y in range(min(self.one_end.y, self.other_end.y), max(self.one_end.y, self.other_end.y) + 1):
                blocks.append(Coords([self.one_end.x, y, self.one_end.z]))
        else:
            for z in range(min(self.one_end.z, self.other_end.z), max(self.one_end.z, self.other_end.z) + 1):
                blocks.append(Coords([self.one_end.x, self.one_end.y, z]))
        return blocks

    def __repr__(self):
        # vertical_string = 'Vertical' if self.is_vertical else 'Horizontal'
        return f'{self.name}: {self.direction} {self.num_blocks}, {self.one_end}-{self.other_end}'


lines = [l for l in input.split('\n') if l]

max_x = 0
max_y = 0
max_z = 0

blocks = []
ascii = 65
for line in lines:
    ends = line.split('~')
    name = str(ascii)
    ascii += 1
    block = Block(Coords(ends[0].split(',')), Coords(ends[1].split(',')), name)
    blocks.append(block)
    max_x = max(max_x, block.one_end.x, block.other_end.x)
    max_y = max(max_y, block.one_end.y, block.other_end.y)
    max_z = max(max_z, block.one_end.z, block.other_end.z)
    # print(block)

# print(f'{max_x}, {max_y}')

# Let them fall
tops = [ [0] * (max_x + 1) for i in range((max_y + 1))]
content = [ [ [' '] * (max_z + 1) for i in range((max_y + 1))] for i in range((max_x + 1))]

block_dict = {}
for block in blocks:
    block_dict[block.name] = block

# print(tops)
blocks.sort(key=lambda x: x.lowest_point(), reverse=False)
for block in blocks:
    how_far_can_it_move_down = 1000000
    for coords in block.footprint():
        # if block.name == 'B':
        #     print(f'Based on {coords} where the top is {tops[coords.x][coords.y]}, B can move down {block.lowest_point() - tops[coords.x][coords.y] - 1}')
        how_far_can_it_move_down = min(how_far_can_it_move_down, block.lowest_point() - tops[coords.x][coords.y] - 1)

    block.move_down(how_far_can_it_move_down)
    for coords in block.footprint():
        # if block.name == 'A':
        #     print(f'A is setting the top at {coords} to {block.highest_point()}')
        tops[coords.x][coords.y] = block.highest_point()
    for coords in block.blocks():
        content[coords.x][coords.y][coords.z] = block.name

    # print(block)
blocks.sort(key=lambda x: x.lowest_point(), reverse=False)

# print(tops)
# print(content)

# Link supporting and supported bricks.
for block in blocks:
    for coords in block.footprint():
        block_below = content[coords.x][coords.y][block.lowest_point() - 1]
        block_above = content[coords.x][coords.y][block.highest_point() + 1]

        if block_above != ' ':
            block.blocks_above.add(block_above)
        if block_below != ' ':
            block.blocks_below.add(block_below)

# Can disintegrate one if all its blocks above are supported by something else.
blocks_to_disintegrate = set(blocks)
for block in blocks:
    for above_name in block.blocks_above:
        block_above = block_dict[above_name]
        if len(block_above.blocks_below) <= 1:
            # print(f'We cannot disintegrate {block} because it is needed to support {block_above}')
            blocks_to_disintegrate.discard(block)
print(f'Part 1: {len(blocks_to_disintegrate)}')

# Part 2: chain reactions
# def how_many_fall(block):
#     num_falling = 0
#     for above_name in block.blocks_above:
#         block_above = block_dict[above_name]
#         if len(block_above.blocks_below) <= 1:
#             # It will fall
#             num_falling += 1
#             num_falling += how_many_fall(block_above)
#     return num_falling

# def disintegrate(block, content_copy):
#     for coords in block.blocks():
#         content_copy[coords.x][coords.y][coords.z] = ' '

# num_disintegrated = 0
# for block in blocks:
#     content_copy = copy.deepcopy(content)
#     disintegrated_for_block = 0
#     disintegrate(block, content_copy)
#     for other_block in blocks:
#         if other_block.lowest_point() <= block.highest_point():
#             continue
#         can_fall = True
#         for coords in other_block.footprint():
#             block_below = content_copy[coords.x][coords.y][block.lowest_point() - 1]
#             if block_below != ' ' and block.lowest_point() > 1:
#                 can_fall = False
#                 break
#         if can_fall:
#             disintegrate(other_block, content_copy)
#             disintegrated_for_block += 1
#             # print(f'For {block}, {other_block} can fall ({disintegrated_for_block})')
#     print(f'For {block}, {disintegrated_for_block} fell')

# total = 0
# for i in range(len(blocks)):
#     block = blocks[i]
#     vanishing_blocks = {block.name}
#     for j in range(i + 1, len(blocks)):
#         block_above = blocks[j]
#         if len(block_above.blocks_below.difference(vanishing_blocks)) == 0:
#             vanishing_blocks.add(block_above.name)
#     # print(f'For {block}, {len(vanishing_blocks) - 1} fell')
#     print(f'For {block}, {vanishing_blocks} fell')
#     total += (len(vanishing_blocks) - 1)
# print(f'Part 2: {total}')
# 1388 is too low (came from adding 1 each time, oops.)
# 88028 is too high.

total = 0
print(datetime.datetime.now())
for block_to_lose in blocks:
    vanishing_blocks = set() # {block_to_lose.name}
    queue = [block_to_lose]

    while queue:
        block_to_check = queue.pop(0)
        if block_to_check == block_to_lose or len(block_to_check.blocks_below.difference(vanishing_blocks)) == 0:
            # This block is unsupported. Disintegrate it and check everything above it.
            vanishing_blocks.add(block_to_check.name)
            for block_above_name in block_to_check.blocks_above:
                block_above = block_dict[block_above_name]
                queue.append(block_above)

    # print(f'For {block_to_lose}, {len(vanishing_blocks) - 1} fell')
    # print(f'For {block_to_lose}, {vanishing_blocks} fell')
    total += (len(vanishing_blocks) - 1)
print(datetime.datetime.now())
print(f'Part 2: {total}')
# 1352 is too low
# 75784 is right!
