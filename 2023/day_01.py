# Day one
# import regex as re
import re

input = open("day_01_input.txt", "r").read()
lines = [l for l in input.split('\n') if l]

# First star
total = 0
for line in lines:
    matches = re.findall(r"\d", line)
    first_digit = matches[0]
    last_digit = matches[-1]
    number = int(first_digit + last_digit)
    total += number

print(f'Part 1: {total}')
# 55971

# Second star
digit_map = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}
def make_digit(string):
    if string in digit_map:
        return digit_map[string]
    return int(string)

total = 0
for line in lines:
    # This fails on overlaps: hthphptmmtwo7sixsevenoneightls: 21
    # matches = re.findall(r"\d|one|two|three|four|five|six|seven|eight|nine", line)

    matches = []
    temp_line = line
    while len(temp_line):
        m = re.search(r"\d|one|two|three|four|five|six|seven|eight|nine", temp_line)
        if m:
            matches.append(m.group())
            # print(f'matches: {m.group()}')
            temp_line = temp_line[m.start() + 1:]
        else:
            break

    first_digit = make_digit(matches[0])
    last_digit = make_digit(matches[-1])
    number = 10 * first_digit + last_digit

    # print(f'{line}: {number}')

    total += number

print(f'Part 2: {total}')

# 54699 too low?
# Total: 54719 - right!


# Doomed attempt in a spreadsheet:
# https://docs.google.com/spreadsheets/d/1RGplq-EsAyEBx4MZPcBjBRr4_8YRF4OwahLB1m8JSMk/edit#gid=0
