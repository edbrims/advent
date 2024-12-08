from input_loader import get_input

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

def can_make_rtl(target, ingredients):
    targets = {target}
    for number in ingredients[::-1]:
        by_subtracting = {t - number for t in targets}
        by_dividing = {t // number for t in targets if t % number == 0}
        targets = by_subtracting.union(by_dividing)
    return (0 in by_subtracting or 1 in by_dividing)

def can_make_with_concat(target, ingredients):
    results = {ingredients[0]}
    for number in ingredients[1:]:
        by_adding = {t + number for t in results}
        by_multiplying = {t * number for t in results}
        by_concat = {int(f"{t}{number}") for t in results}
        results = {r for r in by_adding.union(by_multiplying).union(by_concat) if r <= target}

    return (target in results)


def add_up_targets(lines, can_concatenate):
    count = 0
    for line in lines:
        [target_str, ingredients_str] = line.split(': ')
        target = int(target_str)
        ingredients = [int(i) for i in ingredients_str.split(' ')]
        if can_concatenate:
            if can_make_rtl(target, ingredients):
                count += target
        else:
            if can_make_with_concat(target, ingredients):
                count += target

    return count

lines = get_input(use_real, example_input, __file__)

print(f'Part 1: {add_up_targets(lines, True)}') # 66343330034722
print(f'Part 2: {add_up_targets(lines, False)}') # 637696070419031
