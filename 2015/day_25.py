
# AoC 2015, day 25

# row 2947, column 3029

# 1: r 1 c 1
# 2: r 2 c 1
# 3: r 1 c 2
#
# Triangular numbers in row 1.
# Row 1 Column c: c(c+1)/2

# For row r column c:
# (r+c-1) triangular number, then subtract (r-1)
# = (r+c-1)*(r+c)/2 - (r-1)
# It probably simplifies

def get_sequence_position(r, c):
    return int((r+c-1)*(r+c)/2 - (r-1))

# r = 2
# c = 3
# print(f'At ({r},{c}) you find {term_number}.')


# for (r,c) in [(1,1), (2,1), (1,2),(3,1), (2, 3), (3,2)]:
#     term_number = get_sequence_position(r,c)
#     print(f'At ({r},{c}) you find {term_number}.')

row_wanted = 2947
column_wanted = 3029
term_wanted = get_sequence_position(row_wanted, column_wanted)

print(f'term_wanted: {term_wanted}')

term_number = 1
num = 20151125
for i in range(term_wanted + 1):
    num = ( num * 252533 ) % 33554393
    term_number += 1

    if term_number == term_wanted:
        print(f'Part 1: {num}')

