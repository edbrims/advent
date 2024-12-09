from input_loader import get_input

use_real = True
example_input = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''

class Coords:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def add(self, vector):
        return Coords(self.r + vector.r, self.c + vector.c)

    def __repr__(self):
        return f'({self.r}, {self.c})'

    def __eq__(self, __value: object) -> bool:
        return self.r == __value.r and self.c == __value.c

    def __hash__(self) -> int:
        return self.r + self.c * 1000

lines = get_input(use_real, example_input, __file__)

def get_antennae(lines):
    antennae = {}
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            character = lines[r][c]
            if character != '.':
                if character not in antennae:
                    antennae[character] = []
                antennae[character].append(Coords(r, c))
    return antennae

def find_antinodes_for_character(positions, height, width, repeating):
    antinodes = set()
    for p1 in positions:
        for p2 in positions:
            if p1 == p2:
                continue
            offset = Coords(p2.r-p1.r, p2.c-p1.c)

            if repeating:
                antinode = p2
                while antinode.r >= 0 and antinode.r < height and antinode.c >= 0 and antinode.c < width:
                    antinodes.add(antinode)
                    antinode = antinode.add(offset)
            else:
                antinode = p2.add(offset)
                if antinode.r >= 0 and antinode.r < height and antinode.c >= 0 and antinode.c < width:
                    antinodes.add(antinode)

    return antinodes

def find_all_antinodes(antennae, height, width, repeating):
    antinodes = set()
    for character in antennae.keys():
        positions = antennae[character]
        antinodes = antinodes.union(find_antinodes_for_character(positions, height, width, repeating))
    return antinodes

def count_antinodes(lines, repeating):
    antennae = get_antennae(lines)
    antinodes = find_all_antinodes(antennae, len(lines), len(lines[0]), repeating)
    return len(antinodes)

print(f'Part 1: {count_antinodes(lines, False)}') # 295
print(f'Part 2: {count_antinodes(lines, True)}') # 1034
