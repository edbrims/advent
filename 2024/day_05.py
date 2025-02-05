from utils import get_input

use_real = True
example_input = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

lines = get_input(use_real, example_input, __file__)

def parse_rules_and_updates(lines):
    start_of_updates = 0
    rules = []
    for i in range(len(lines)):
        line = lines[i]
        if "," in line:
            start_of_updates = i
            break
        rules.append([int(p) for p in line.split('|')])

    updates = []
    for i in range(start_of_updates, len(lines)):
        line = lines[i]
        updates.append([int(p) for p in line.split(',')])
    return rules, updates

def is_correct(update, rules):
    page_locations = {}
    for i in range(len(update)):
        page_locations[update[i]] = i

    for rule in rules:
        if (rule[0] in page_locations and
            rule[1] in page_locations and
            page_locations[rule[1]] < page_locations[rule[0]]):
            return False
    return True

def middle(update):
    num_updates = len(update)
    if num_updates % 2 == 0:
        raise Exception(f'Even number of updates! {num_updates}')
    return update[(num_updates - 1) // 2]

def filter(rules, page_set):
    return [r for r in rules if r[0] in page_set and r[1] in page_set]

def get_next_page(pages_remaining, filtered_rules):
    candidates = set(pages_remaining)
    for rule in filtered_rules:
        candidates.discard(rule[1])
    (only_candidate,) = candidates
    return only_candidate

def fix(update, rules):
    filtered_rules = rules
    pages_remaining = set(update)
    fixed_update = []
    while pages_remaining:
        filtered_rules = filter(filtered_rules, pages_remaining)
        next_page = get_next_page(pages_remaining, filtered_rules)
        fixed_update.append(next_page)
        pages_remaining.remove(next_page)
    return fixed_update


def count_middles_of_good_updates(updates, rules):
    return sum([middle(u) for u in updates if is_correct(u, rules)])

def count_middles_of_bad_updates(updates, rules):
    return sum([middle(fix(u, rules)) for u in updates if not is_correct(u, rules)])

rules, updates = parse_rules_and_updates(lines)
print(f'Part 1: {count_middles_of_good_updates(updates, rules)}') # 4774
print(f'Part 2: {count_middles_of_bad_updates(updates, rules)}') # 6004
