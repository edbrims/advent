# import sympy as sym

input = open("day_24_input.txt", "r").read()
region_start = 200000000000000
region_end = 400000000000000

# Example
# input = '''19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3'''
# region_start = 7
# region_end = 27


class Vector:
    def __init__(self, coords):
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.z = int(coords[2])

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

class Hailstone:
    def __init__(self, start, velocity):
        self.start = start
        self.velocity = velocity

    def __repr__(self):
        return f'{self.start} @ {self.velocity}'

lines = [l for l in input.split('\n') if l]

hailstones = []
for line in lines:
    vectors = line.split(' @ ')
    start = Vector(vectors[0].split(', '))
    velocity = Vector(vectors[1].split(', '))
    hailstone = Hailstone(start, velocity)
    hailstones.append(hailstone)

def meeting_place(hailstone_1, hailstone_2):
    if hailstone_2.velocity.x * hailstone_1.velocity.y == hailstone_1.velocity.x * hailstone_2.velocity.y:
        return None


    time_2 = ((hailstone_1.velocity.y * (hailstone_1.start.x - hailstone_2.start.x)
               - hailstone_1.velocity.x * (hailstone_1.start.y - hailstone_2.start.y)) * 1.0 /
               (hailstone_2.velocity.x * hailstone_1.velocity.y - hailstone_1.velocity.x * hailstone_2.velocity.y))
    if time_2 < 0:
        return None

    time_1 = ((hailstone_2.velocity.y * (hailstone_2.start.x - hailstone_1.start.x)
               - hailstone_2.velocity.x * (hailstone_2.start.y - hailstone_1.start.y)) * 1.0 /
               (hailstone_1.velocity.x * hailstone_2.velocity.y - hailstone_2.velocity.x * hailstone_1.velocity.y))
    if time_1 < 0:
        return None

    return Vector([(hailstone_2.start.x + time_2 * hailstone_2.velocity.x),
                   (hailstone_2.start.y + time_2 * hailstone_2.velocity.y),
                      0])


count = 0
for i in range(len(hailstones)):
    for j in range(i+1, len(hailstones)):
        meeting = meeting_place(hailstones[i], hailstones[j])
        if meeting:
            if meeting.x >= region_start and meeting.x <= region_end and meeting.y >= region_start and meeting.y <= region_end:
                count += 1


print(f'Part 1: {count}')
# 14672

# Trying a lot of pencil and paper.
# And spreadsheet formulae.
# And the Excel Solver add-in.
# The first three hailstones give 9 equations for 9 unknowns:
# x+at=197869613734967+150t,
# y+bt=292946034245705+5t,
# z+ct=309220804687650-8t,
# x+au=344503265587754-69u,
# y+bu=394181872935272+11u,
# z+cu=376338710786779-46u,
# x+av=293577250654200-17v,
# y+bv=176398758803665+101v,
# z+cv=272206447651388+26v

#  x+a*t=197869613734967+150*t, y+b*t=292946034245705+5*t, z+c*t=309220804687650-8*t, x+a*u=344503265587754-69*u, y+b*u=394181872935272+11*u, z+c*u=376338710786779-46*u, x+a*v=293577250654200-17*v, y+b*v=176398758803665+101*v, z+c*v=272206447651388+26*v
# https://solvemymath.com/online_math_calculator/algebra_combinatorics/system_of_equations/index.php

x = 291669802654110
y = 103597826800230
z = 251542427650413
a = -11
b = 330
c = 91
t = 582609869063
u = 910921774718
# v = whatever
print(f'Part 2: {x+y+z}')
# 646810057104753 is right!!
