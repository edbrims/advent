from input_loader import get_input

use_real = True
example_input = '''
2333133121414131402
'''

lines = get_input(use_real, example_input, __file__)

class Block:
    def __init__(self, id, length, start):
        self.id = id
        self.length = length
        self.start = start

    def checksum(self):
        return self.id * self.length * (2 * self.start + self.length - 1) // 2

    def end(self):
        return self.start + self.length - 1

    def __repr__(self):
        return f'({self.id} in {self.start}-{self.end()})'


def read_blocks(line):
    blocks = []
    gaps = []
    position = 0
    id = 0
    for i in range(len(line) // 2 + 1):
        length = int(line[2 * i])
        if length > 0:
            blocks.append(Block(id, length, position))
        position += length

        if (2 * i + 1 >= len(line)):
            break
        gap_length = int(line[2 * i + 1])
        if gap_length > 0:
            gaps.append(Block(None, gap_length, position))
        position += gap_length
        id += 1
    return blocks, gaps

def defrag_by_block(blocks, gaps):
    while gaps and (gaps[0].start < blocks[-1].end()):
        first_gap = gaps[0]
        last_block = blocks[-1]
        if last_block.length == first_gap.length:
            # Perfect fit!
            gaps.pop(0)
            blocks.pop()
            blocks.insert(0, Block(last_block.id, last_block.length, first_gap.start))
        elif last_block.length < first_gap.length:
            # Small block in a big gap. Shrink the gap.
            blocks.pop()
            blocks.insert(0, Block(last_block.id, last_block.length, first_gap.start))
            gaps[0].start += last_block.length
            gaps[0].length -= last_block.length
        else:
            # Big block in a small gap. Chop it up to fill the gap.
            blocks.insert(0, Block(last_block.id, first_gap.length, first_gap.start))
            gaps.pop(0)
            blocks[-1].length -= first_gap.length
    return blocks

def index_of_first_gap_big_enough(block, gaps):
    for i in range(len(gaps)):
        gap = gaps[i]
        if gap.length >= block.length:
            return i
    return None

def defrag_by_file(blocks, gaps):
    for i in reversed(range(len(blocks))):
        block = blocks[i]

        gap_index = index_of_first_gap_big_enough(block, gaps)
        if gap_index is not None and gaps[gap_index].start < block.start:
            gap_to_fill = gaps[gap_index]
            blocks[i].start = gap_to_fill.start
            if block.length == gap_to_fill.length:
                # Perfect fit - delete the gap.
                gaps.pop(gap_index)
            else:
                # We've only filled part of the gap
                gaps[gap_index].start += block.length
                gaps[gap_index].length -= block.length
        else:
            # Can't be moved
            pass

    return blocks

def checksum_sum(blocks):
    return sum([b.checksum() for b in blocks])

blocks, gaps = read_blocks(lines[0])
print(f'Part 1: {checksum_sum(defrag_by_block(blocks, gaps))}') # 6432869891895

blocks, gaps = read_blocks(lines[0])
print(f'Part 2: {checksum_sum(defrag_by_file(blocks, gaps))}') # 6467290479134
# First guess 8664287909542 was too high because I didn't insist on moving left.
