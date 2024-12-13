from utils import get_input

use_real = True
example_input = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

def can_make_rtl(target, ingredients, can_concatenate):
    targets = {target}
    for number in ingredients[1:][::-1]:
        by_subtracting = {t - number for t in targets}
        by_dividing = {t // number for t in targets if t % number == 0}

        if can_concatenate:
            one_and_zeros = (10 ** len(str(number)))
            by_shortening = {(t - number) // one_and_zeros for t in targets if t % one_and_zeros == number}

        targets = by_subtracting.union(by_dividing)
        if can_concatenate:
            targets = targets.union(by_shortening)
        targets = {t for t in targets if t >= 0}

    return (ingredients[0] in targets)


def add_up_targets(lines, can_concatenate):
    count = 0
    for line in lines:
        [target_str, ingredients_str] = line.split(': ')
        target = int(target_str)
        ingredients = [int(i) for i in ingredients_str.split(' ')]
        if can_make_rtl(target, ingredients, can_concatenate):
            count += target

    return count

lines = get_input(use_real, example_input, __file__)

print(f'Part 1: {add_up_targets(lines, False)}') # 66343330034722
print(f'Part 2: {add_up_targets(lines, True)}') # 637696070419031
