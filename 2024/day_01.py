from utils import get_input

use_real = True
example_input = '''
3   4
4   3
2   5
1   3
3   9
3   3
'''

input = get_input(use_real, example_input, __file__)

list_1 = []
list_2 = []
for line in input:
    parts = line.split('   ')
    list_1.append(int(parts[0]))
    list_2.append(int(parts[1]))

list_1.sort()
list_2.sort()
diffs = [abs(a-b) for a, b in zip(list_1, list_2)]
print(f'Part 1: {sum(diffs)}') # 3574690

total = 0
for location_id in list_1:
    count = list_2.count(location_id)
    total += location_id * count
print(f'Part 2: {total}') # 22565391
