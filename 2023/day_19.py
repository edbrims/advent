import copy

workflows_input = open("day_19_workflows.txt", "r").read()
properties_input = open("day_19_properties.txt", "r").read()

# Example
# workflows_input = '''px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}
# '''
# properties_input = '''
# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}
# '''

workflows = [l for l in workflows_input.split('\n') if l]
properties = [l for l in properties_input.split('\n') if l]

workflows_map = {}
for workflow_str in workflows:
    parts = workflow_str.split('{')
    label = parts[0]
    workflow = parts[1][:-1]
    # print(workflow)
    workflows_map[label] = workflow

def is_condition_satisfied(condition, part_properties):
    if condition[1] == '<':
        return part_properties[condition[0]] < int(condition[2:])
    elif condition[1] == '>':
        return part_properties[condition[0]] > int(condition[2:])

    print('Cannot deal with ' + condition)


def is_accepted(workflow, part_properties):
    # print(f'Doing workflow {workflow}')
    # s<537:gd,x>2440:R,A
    if workflow == 'R':
        return False
    if workflow == 'A':
        return True

    first_colon_pos = workflow.find(':')
    # print(first_colon_pos)
    if first_colon_pos < 0:
        # It's a label. Look up the label.
        return is_accepted(workflows_map[workflow], part_properties)

    condition = workflow[:first_colon_pos]
    first_comma_position = workflow.find(',')
    action_if_true = workflow[first_colon_pos + 1:first_comma_position]
    action_if_false = workflow[first_comma_position + 1:]
    if is_condition_satisfied(condition, part_properties):
        # print(f'Condition {condition} is true, so doing {action_if_true}')
        return is_accepted(action_if_true, part_properties)
    # print(f'Condition {condition} is false, so doing {action_if_false}')
    return is_accepted(action_if_false, part_properties)

def get_part_sum_if_accepted(part_properties):
    if is_accepted('in', part_properties):
        return sum(part_properties.values())
    return 0


total = 0
for part_str in properties:
    # {x=787,m=2655,a=1222,s=2876}
    part_properties = {}
    pairs = part_str[1:-1].split(',')
    for pair in pairs:
        bits = pair.split('=')
        part_properties[bits[0]] = int(bits[1])

    # print(part_properties)
    # if is_accepted('in', part_properties):
    total += get_part_sum_if_accepted(part_properties)
print(f'Part 1: {total}')
# 397643 is right

# Part 2 brute force is silly. I get bored before m=2, let alone x.
# total = 0
# for x in range (1, 4001):
#     print(f'x = {x}, total = {total}')
#     for m in range(1, 4001):
#         print(f'  m = {m}, total = {total}')
#         for a in range(1, 4001):
#             print(f'    a = {a}, total = {total}')
#             for s in range(1, 4001):
#                 if (is_accepted('in', {'x': x, 'm': m, 'a': a, 's': s})):
#                     total += 1
# print(total)

class Condition:
    def __init__(self, variable, sign, value):
        self.variable = variable
        self.sign = sign
        self.value = value
    def __repr__(self):
        return f'{self.variable}{self.sign}{self.value}'

class Tree:
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
    def __repr__(self):
        return f'{self.condition} ? [{self.if_true} : {self.if_false}]'

# Make a tree?
#        condition
#     True?      False?
#  action          action
# Where action is another condition, or True/False to accept or reject.
# Bottom leaves are all A/R, top root is the "in"
# {'x<3': [{'m>2': [True, {}]}, {}]}
def make_tree(action):
    # s<537:gd,x>2440:R,A
    if action == 'R':
        return False
    if action == 'A':
        return True

    first_colon_pos = action.find(':')
    # print(first_colon_pos)
    if first_colon_pos < 0:
        # It's a label. Look up the label.
        return make_tree(workflows_map[action])

    condition_str = action[:first_colon_pos]
    # condition = [condition_str[0], condition_str[1], int(condition_str[2:])]

    # condition = type('condition', (object,), dict(variable=condition_str[0],
    #                                               sign=condition_str[1],
    #                                               value = int(condition_str[2:])))

    condition = Condition(condition_str[0], condition_str[1], int(condition_str[2:]))

    first_comma_position = action.find(',')
    action_if_true = action[first_colon_pos + 1:first_comma_position]
    action_if_false = action[first_comma_position + 1:]

    # return [condition, make_tree(action_if_true), make_tree(action_if_false)]
    return Tree(condition, make_tree(action_if_true), make_tree(action_if_false))

def simplify_tree(tree):
    if tree in [True, False]:
        return tree

    tree_if_true : Tree = simplify_tree(tree.if_true)
    tree_if_false : Tree = simplify_tree(tree.if_false)

    if tree_if_true == tree_if_false:
        return tree_if_true

    # if tree_if_true in [True, False] or tree_if_false in [True, False]:
    #     # Can't simplify them any further if they are not both trees.
    #     return tree

    condition : Condition = tree.condition

    # Might as well always be <
    if condition.sign == '>':
        [tree_if_true, tree_if_false] = [tree_if_false, tree_if_true]
        condition.sign = '<'
        condition.value += 1

    # if (tree_if_true not in [True, False] and
    #     condition.variable == tree_if_true.condition.variable and
    #     condition.value < tree_if_true.condition.value):
    #     # eg. This is x<30, and if true it's checking x<50
    #     tree_if_true = tree_if_true.if_true
    #     print('This happens')
    #     # pass

    return Tree(condition, tree_if_true, tree_if_false)


def size_range(property_ranges):
    number = 1
    for range in property_ranges.values():
        number *= (range[1] - range[0] + 1)
    return number

def how_many_accepted(tree, property_ranges):
    if tree == True:
        return size_range(property_ranges)
    if tree == False:
        return 0

    condition = tree.condition
    if condition.sign != '<':
        print(f'Not simplified right: {condition}')

    if_true_range = copy.deepcopy(property_ranges)
    if_false_range = copy.deepcopy(property_ranges)

    accepted_if_true = 0
    if_true_range[condition.variable][1] = condition.value - 1
    if if_true_range[condition.variable][0] <= if_true_range[condition.variable][1]:
        # print(f'For {condition}, split {property_ranges[condition.variable]} into {if_true_range[condition.variable]} if true')
        accepted_if_true += how_many_accepted(tree.if_true, if_true_range)

    accepted_if_false = 0
    if_false_range[condition.variable][0] = condition.value
    if if_false_range[condition.variable][0] <= if_false_range[condition.variable][1]:
        # print(f'For {condition}, split {property_ranges[condition.variable]} into {if_false_range[condition.variable]} if false')
        accepted_if_false += how_many_accepted(tree.if_false, if_false_range)


    return accepted_if_true + accepted_if_false

decision_tree = make_tree('in')
# print(decision_tree)
simplified_tree = simplify_tree(decision_tree)
# print(simplified_tree)

property_ranges = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}

num_accepted = how_many_accepted(simplified_tree, property_ranges)
print(f'Part 2: {num_accepted}')
# For the example I get 15320205000000
# Actual answer is     167409079868000
# With copy.deepcopy,  167409079868000
