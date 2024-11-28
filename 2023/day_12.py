input = open("day_12_input.txt", "r").read()

# Test
# input = '''???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1'''


# ????.#...#... [4, 1, 1]
# while():
#    Place the first one:
#    XXXX.#...#...
#    Recursively place the rest:
#        .#...#... [1, 1]

# Slow one, runtime exceeded:
# input = '???..????.????#?? 1,1,1,1,5'
# Fixed by DP.

lines = [l for l in input.split('\n') if l]
cache = {}

def count_solutions(pattern, block_lengths):
    # [Boundary conditions I don't actually use.]
    # if len(block_lengths) == 0:
    #     # Nothing to place - we've got them all in.
    #     return 1
    # if len(pattern) < sum(block_lengths) + len(block_lengths) - 1:
    #     # No room to fit them all in.
    #     return 0

    cache_key = pattern + ':' + ','.join([str(k) for k in block_lengths])
    if cache_key in cache:
        return cache[cache_key]

    # Try all locations for the first block, then recursively get the rest.
    num_options = 0
    first_block_length = block_lengths[0]
    last_possible_position = len(pattern) - first_block_length
    for first_block_pos in range(last_possible_position + 1):
        if first_block_pos > 0 and pattern[first_block_pos - 1] == '#':
            # We can't place the first block after a hash. Don't check any more.
            break
        for i in range(first_block_pos, first_block_pos + first_block_length):
            if (pattern[i] == '.'):
                # Doesn't fit here.
                break
        else:
            # We found somewhere it fits
            if pattern[first_block_pos + first_block_length] == '#':
                # Actually it doesn't fit, because this would be part of a longer run.
                pass
            else:
                remaining_block_lengths = block_lengths[1:]
                remaining_pattern = pattern[first_block_pos + first_block_length + 1:]
                if len(remaining_block_lengths) == 0:
                    for c in remaining_pattern:
                        if c == '#':
                            # Actually it doesn't fit, because we need a later one.
                            break
                    else:
                        # We have placed the last block for the row, so that's one solution!
                        num_options += 1
                else:
                    # There are more blocks to place. Do them recursively
                    num_options += count_solutions(remaining_pattern, remaining_block_lengths)

    cache[cache_key] = num_options
    return num_options

def count_all(copies_of_input):
    total = 0
    for line in lines:
        [pattern, block_length_str] = line.split(' ')
        block_lengths = [int(k) for k in block_length_str.split(',')]

        pattern = '?'.join([pattern] * copies_of_input)
        block_lengths = block_lengths * copies_of_input

        options = count_solutions(pattern + '.', block_lengths)
        # print(f'{pattern} {block_lengths}: {options} arrangements')
        total += options
    return total

print(f'Part 1: {count_all(1)}')
print(f'Part 2: {count_all(5)}')
