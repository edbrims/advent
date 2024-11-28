# Day 6
import math

races = [
    { 'time': 62, 'record': 644},
    { 'time': 73, 'record': 1023},
    { 'time': 75, 'record': 1240},
    { 'time': 65, 'record': 1023},
]

# It's just solving this inequality:
# h * (t-h) > record
# h^2 -ht + record < 0
def num_ways_to_win(time, record):
    square_rooty_bit = math.sqrt(time*time/4 - record)
    minimum = time/2 - square_rooty_bit
    maximum = time/2 + square_rooty_bit
    return math.floor(maximum) - math.ceil(minimum) + 1

# Part 1
product = 1
for race in races:
    number = num_ways_to_win(race['time'], race['record'])
    product = product * number
print(f'Part 1: {product}')
# 393120

# print(num_ways_to_win(62, 644))
# print(num_ways_to_win(71530, 940200))

# Part 2
# print(num_ways_to_win(62737565, 644102312401023))
print(f'Part 2: {num_ways_to_win(62737565, 644102312401023)}')
# 36872656
