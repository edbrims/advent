input = open("day_02_input.txt", "r").read()

# Part 1
total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    bits = line.split(': ')
    game_number = int(bits[0][5:])
    in_bag = {'red': 0, 'green': 0, 'blue': 0}
    draws = bits[1].split('; ')
    for draw in draws:
        balls = draw.split(', ')
        for ball in balls:
            (number, colour) = ball.split(' ')

            if (int(number) > in_bag[colour]):
                in_bag[colour] = int(number)
    if (in_bag['red'] <= 12 and in_bag['green'] <= 13 and in_bag['blue'] <= 14):
        total += game_number

print(f'Part 1: {total}')

# 249 too low, oops, I did >=
# 2771 is right!

# Part 2
total = 0
lines = [l for l in input.split('\n') if l]
# print(lines[0])
for line in lines:
    bits = line.split(': ')
    game_number = int(bits[0][5:])
    in_bag = {'red': 0, 'green': 0, 'blue': 0}
    draws = bits[1].split('; ')
    for draw in draws:
        balls = draw.split(', ')
        for ball in balls:
            (number, colour) = ball.split(' ')

            if (int(number) > in_bag[colour]):
                in_bag[colour] = int(number)
    power = in_bag['red'] * in_bag['green']* in_bag['blue']
    total += power

print(f'Part 2: {total}')
# 70924 is right
