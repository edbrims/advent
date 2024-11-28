input = open("day_04_input.txt", "r").read()

total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    bits = line.split(': ')
    card_number = int(bits[0][5:])
    (win_str, entries_str) = bits[1].split(' | ')
    winner_strings = [s for s in win_str.split(' ') if s]
    winners = set(map(int, winner_strings))
    entry_strings = [s for s in entries_str.split(' ') if s]
    entries = set(map(int, entry_strings))

    winning_entries = winners.intersection(entries)

    if len(winning_entries) == 0:
        score = 0
    else:
        score = 2 ** (len(winning_entries) - 1)
    # print(f'Card {card_number + 10000} has winning_entries {winning_entries}. Score is {score}')
    total += score

print(f'Part 1: {total}')
# 2484 typo!
# 24848 is right!

# Part 2.
lines = [l for l in input.split('\n') if l]
copies = [1] * (len(lines) + 1)
copies[0] = 0
for line in lines:
    bits = line.split(': ')
    card_number = int(bits[0][5:])
    (win_str, entries_str) = bits[1].split(' | ')
    winner_strings = [s for s in win_str.split(' ') if s]
    winners = set(map(int, winner_strings))
    entry_strings = [s for s in entries_str.split(' ') if s]
    entries = set(map(int, entry_strings))

    winning_entries = winners.intersection(entries)
    num_winners = len(winning_entries)

    for i in range(card_number + 1, card_number + num_winners + 1):
        copies[i] += copies[card_number]

    total += score

print(f'Part 2: {sum(copies)}')
# 7258152 is right!

