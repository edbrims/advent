input = open("day_01_input.txt", "r").read()
# input = 'R8, R4, R4, R8'
def turn(vector, direction):
    if direction == 'L':
        return [-vector[1], vector[0]]
    else:
        return [vector[1], -vector[0]]

position = [0, 0]
facing_vector = [0, 1]
directions = input.split(', ')
solved_part_2 = False

def position_string(position):
    return f'{position[0],position[1]}'

visited = {position_string(position)}
for direction_str in directions:
    facing_vector = turn(facing_vector, direction_str[0])
    distance_to_walk = int(direction_str[1:])
    for step in range(1, distance_to_walk + 1):
        step_location = [position[i] + step * facing_vector[i] for i in range(2)]
        ps = position_string(step_location)
        if ps in visited:
            if not solved_part_2:
                print(f'Part 2: {sum([abs(p) for p in step_location])}')
                solved_part_2 = True
        else:
            visited.add(ps)

    position = [position[i] + distance_to_walk * facing_vector[i] for i in range(2)]

print(f'Part 1: {sum([abs(p) for p in position])}')
