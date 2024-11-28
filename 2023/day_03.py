input = open("day_03_input.txt", "r").read()

# Part 1
def is_adjacent(line_number, current_number_start, current_number_end, symbol_positions):
    # print(f'Number is line {line_number}, {current_number_start}-{current_number_end}...')
    for l in range (line_number - 1, line_number + 2):
        for c in range (current_number_start - 1, current_number_end + 2):
            # print(f'Checking ({l},{c})')
            if (l,c) in symbol_positions:
                return True
    return False

lines = [l for l in input.split('\n') if l]
# (line, char)
symbol_positions = set()
for line_number, line in enumerate(lines):
    for char_number, character in enumerate(line):
        if character not in {'.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
            symbol_positions.add((line_number, char_number))

total = 0
current_number = current_number_start = current_number_end = -1
for line_number, line in enumerate(lines):
    line = line + '$' # Cheat so you never end in a number
    for char_number, character in enumerate(line):
        if character in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
            if (current_number < 0):
                current_number_start = char_number
                current_number = 0
            current_number = current_number * 10 + int(character)
        elif current_number > 0:
            # Just finished a number
            current_number_end = char_number - 1
            ## Do stuff with the number
            if is_adjacent(line_number, current_number_start, current_number_end, symbol_positions):
                total += current_number
            # Reset
            current_number = current_number_start = current_number_end = -1

print(f'Part 1: {total}')

# 308699 is too low. I was silly params in wrong order.
# 550934 is right!

# Part 2
def find_adjacent_stars(line_number, current_number_start, current_number_end, stars):
    adjacent_stars = []
    for l in range (line_number - 1, line_number + 2):
        for c in range (current_number_start - 1, current_number_end + 2):
            # print(f'Checking ({l},{c})')
            if (l,c) in stars.keys():
                adjacent_stars.append((l,c))
    return adjacent_stars

# Stars. Map (l,c) to a list of adjacent numbers.
stars = {}
lines = [l for l in input.split('\n') if l]
for line_number, line in enumerate(lines):
    for char_number, character in enumerate(line):
        if character in {'*'}:
            stars[(line_number, char_number)] = []
current_number = current_number_start = current_number_end = -1
for line_number, line in enumerate(lines):
    line = line + '$' # Cheat so you never end in a number
    for char_number, character in enumerate(line):
        if character in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
            if (current_number < 0):
                current_number_start = char_number
                current_number = 0
            current_number = current_number * 10 + int(character)
        elif current_number > 0:
            # Just finished a number
            current_number_end = char_number - 1
            ## Do stuff with the number
            adjacent_stars = find_adjacent_stars(line_number, current_number_start, current_number_end, stars)
            for (l,c) in adjacent_stars:
                stars[(l,c)].append(current_number)
            # Reset
            current_number = current_number_start = current_number_end = -1

total = 0
for (l,c), adj_list in stars.items():
    if len(adj_list) == 2:
        total += adj_list[0] * adj_list[1]

print(f'Part 2: {total}')
# 81997870 is right!
