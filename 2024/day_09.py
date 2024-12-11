from input_loader import get_input

use_real = True
example_input = '''
2333133121414131402
'''

lines = get_input(use_real, example_input, __file__)

class File:
    def __init__(self, id, length, start):
        self.id = id
        self.length = length
        self.start = start

    def checksum(self):
        return self.id * self.length * (self.start + self.end()) // 2

    def end(self):
        return self.start + self.length - 1

    def __repr__(self):
        return f'({self.id} in {self.start}-{self.end()})'


def read_files_and_gaps(instructions):
    files = []
    gaps = []
    position = 0
    id = 0
    for i in range(len(instructions) // 2 + 1):
        length = int(instructions[2 * i])
        if length > 0:
            files.append(File(id, length, position))
        position += length

        if (2 * i + 1 >= len(instructions)):
            break
        gap_length = int(instructions[2 * i + 1])
        if gap_length > 0:
            gaps.append(File(None, gap_length, position))
        position += gap_length
        id += 1
    return files, gaps

def defrag_by_block(instructions):
    files, gaps = read_files_and_gaps(instructions)
    while gaps and (gaps[0].start < files[-1].end()):
        first_gap = gaps[0]
        last_file = files[-1]
        if last_file.length == first_gap.length:
            # Perfect fit!
            gaps.pop(0)
            files.pop()
            files.insert(0, File(last_file.id, last_file.length, first_gap.start))
        elif last_file.length < first_gap.length:
            # Small file in a big gap. Shrink the gap.
            files.pop()
            files.insert(0, File(last_file.id, last_file.length, first_gap.start))
            gaps[0].start += last_file.length
            gaps[0].length -= last_file.length
        else:
            # Big file in a small gap. Chop it up to fill the gap.
            files.insert(0, File(last_file.id, first_gap.length, first_gap.start))
            gaps.pop(0)
            files[-1].length -= first_gap.length
    return files

def index_of_first_gap_big_enough(file, gaps):
    for i in range(len(gaps)):
        gap = gaps[i]
        if gap.length >= file.length:
            return i
    return None

def defrag_by_file(instructions):
    files, gaps = read_files_and_gaps(instructions)
    for i in reversed(range(len(files))):
        file = files[i]

        gap_index = index_of_first_gap_big_enough(file, gaps)
        if gap_index is not None and gaps[gap_index].start < file.start:
            gap_to_fill = gaps[gap_index]
            files[i].start = gap_to_fill.start
            if file.length == gap_to_fill.length:
                # Perfect fit - delete the gap.
                gaps.pop(gap_index)
            else:
                # We've only filled part of the gap
                gaps[gap_index].start += file.length
                gaps[gap_index].length -= file.length
        else:
            # Can't be moved
            pass

    return files

def checksum_sum(files):
    return sum([b.checksum() for b in files])

print(f'Part 1: {checksum_sum(defrag_by_block(lines[0]))}') # 6432869891895
print(f'Part 2: {checksum_sum(defrag_by_file(lines[0]))}') # 6467290479134
# First guess 8664287909542 was too high because I didn't insist on moving left.
