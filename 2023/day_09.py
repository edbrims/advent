input = open("day_09_input.txt", "r").read()

# test
# input = '''0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45'''

def next_number(sequence):
    if len(sequence) <= 1:
        print(f'Not possible: {sequence}')
    if max(sequence) == 0 and min(sequence) == 0:
        return 0
    diff_sequence = []
    for i in range(len(sequence) - 1):
        diff_sequence.append(sequence[i+1] - sequence[i])
    return sequence[-1] + next_number(diff_sequence)

total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    sequence = [int(x) for x in line.split(' ')]
    next_one = next_number(sequence)
    total += next_one
print(f'Part 1: {total}')
# 1930746032 is right.

# Part 2
def prev_number(sequence):
    if len(sequence) <= 1:
        print(f'Not possible: {sequence}')
    if max(sequence) == 0 and min(sequence) == 0:
        return 0
    diff_sequence = []
    for i in range(len(sequence) - 1):
        diff_sequence.append(sequence[i+1] - sequence[i])
    return  sequence[0] - prev_number(diff_sequence)

total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    sequence = [int(x) for x in line.split(' ')]
    prev_one = prev_number(sequence)
    total += prev_one
print(f'Part 2: {total}')
# 1154 is right!
