input = open("day_02_input.txt", "r").read()

# input = '''2x3x4
# 1x1x10'''

# Part 1
total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    measurements = list(map(int, line.split('x')))
    face_areas = [measurements[0]*measurements[1], measurements[1]*measurements[2], measurements[2]*measurements[0]]
    area_needed = 2 * sum(face_areas) + min(face_areas)
    # print(f'{line} requires {area_needed}')
    total += area_needed

print(f'Part 1: {total}')
# 1588178

# Part 2
total = 0
lines = [l for l in input.split('\n') if l]
for line in lines:
    measurements = list(map(int, line.split('x')))
    face_perimeters = [measurements[0]+measurements[1], measurements[1]+measurements[2], measurements[2]+measurements[0]]
    smallest_face = 2 * min(face_perimeters)
    bow = measurements[0]*measurements[1]*measurements[2]
    ribbon_needed = smallest_face + bow
    # print(f'{line} requires {ribbon_needed}')
    total += ribbon_needed
print(f'Part 2: {total}')
# 3783758
