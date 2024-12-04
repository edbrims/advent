import re
from input_loader import get_input

use_real = True
example_input = '''
xmul(2,4)&mul[3,7]!^
don't()_mul(5,5)+mul(32,64](mul(11,8)un
do()?mul(8,5))
'''

input = get_input(use_real, example_input, __file__)

def count(input, skip_donts: bool):
    total = 0
    for line in input:
        if skip_donts and line.startswith('don'):
            continue
        matches = re.findall( r'mul\(\d+,\d+\)', line)
        for match in matches:
            # mul(11,8)
            number_bit = match[4:-1]
            numbers = number_bit.split(',')
            total += int(numbers[0]) * int(numbers[1])
    return total

print(f'Part 1: {count(input, False)}') # 153469856
print(f'Part 2: {count(input, True)}') # 77055967
