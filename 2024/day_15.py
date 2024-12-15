from utils import get_input, Coords

use_real = True
example_input = '''
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''

example_input = '''
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

# example_input = '''
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^
# '''

class WideBox:
    def __init__(self, r, c1, state):
        self.pos1 = Coords(r, c1)
        self.state = state

    def pos2(self):
        return self.pos1.add(Coords(0, 1))
    
    def can_move(self, vector, state):
        if vector.r == 0:
            # Moving horizontally.
            if vector.c < 0:
                # Left
                next_squares = [self.pos1.add(vector)]
            elif vector.c > 0:
                # Right
                next_squares = [self.pos2().add(vector)]
        else:
            # Moving vertically
            next_squares = [self.pos1.add(vector), self.pos2().add(vector)]

        # print(f"next squares beyond {self}: {next_squares}")
        for next_square in next_squares:
            # print(f"next square beyond {self}: {next_square}")
            if next_square in state.walls:
                # print("It's a wall")
                return False
            if next_square in state.boxes:
                other_can_move = state.boxes[next_square].can_move(vector, state)
                if other_can_move:
                    continue
                # print("It's a block that can't move")
                return False
        # print("Clear to move")
        return True


    def __repr__(self):
        return f"Block in ({self.pos1.r}, {self.pos1.c}-{self.pos2().c})"

    def move(self, vector, state):
        if vector.r == 0:
            # Moving horizontally.
            if vector.c < 0:
                # Left
                next_squares = [self.pos1.add(vector)]
            elif vector.c > 0:
                # Right
                next_squares = [self.pos2().add(vector)]
        else:
            # Moving vertically
            next_squares = [self.pos1.add(vector), self.pos2().add(vector)]

        for next_square in next_squares:
            if next_square in state.walls:
                raise Exception(f"Can't move {self} to {next_square} because it's a wall")
            # Clear the way
            if next_square in state.boxes:
                state.boxes[next_square].move(vector, state)
        # Move this box.
        del(self.state.boxes[self.pos1])
        del(self.state.boxes[self.pos2()])
        self.pos1 = self.pos1.add(vector)
        self.state.boxes[self.pos1] = self
        self.state.boxes[self.pos2()] = self

class State:
    def __init__(self, robot_position, boxes, walls, instructions, wide_boxes):
        self.robot_position = robot_position
        self.boxes = boxes
        self.walls = walls
        self.instructions = instructions
        self.wide_boxes = wide_boxes

    def get_gps(self):
        total = 0
        if self.wide_boxes:
            for box in set(self.boxes.values()):
                total += 100 * box.pos1.r + box.pos1.c
        else:
            for box_coords in self.boxes.keys():
                total += 100 * box_coords.r + box_coords.c
        return total


    def __repr__(self):
        return f"Robot at {self.robot_position}"

def read_setup(lines):
    boxes = {}
    walls = set()
    instructions = []
    robot_position = None
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            symbol = line[c]
            if symbol == "@":
                robot_position = Coords(r, c)
            elif symbol == "#":
                walls.add(Coords(r, c))
            elif symbol == "O":
                boxes[Coords(r, c)] = "O"
            elif symbol == "^":
                instructions.append(Coords(-1, 0))
            elif symbol == "v":
                instructions.append(Coords(1, 0))
            elif symbol == "<":
                instructions.append(Coords(0, -1))
            elif symbol == ">":
                instructions.append(Coords(0, 1))
    return State(robot_position, boxes, walls, instructions, False)

def read_setup_double(lines):
    boxes = {}
    walls = set()
    instructions = []
    robot_position = None
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            symbol = line[c]
            if symbol == "@":
                robot_position = Coords(r, 2 * c)
            elif symbol == "#":
                walls.add(Coords(r, 2 * c))
                walls.add(Coords(r, 2 * c + 1))
            elif symbol == "O":
                box = WideBox(r, 2 * c, None)
                boxes[Coords(r, 2 * c)] = box
                boxes[Coords(r, 2 * c + 1)] = box
            elif symbol == "^":
                instructions.append(Coords(-1, 0))
            elif symbol == "v":
                instructions.append(Coords(1, 0))
            elif symbol == "<":
                instructions.append(Coords(0, -1))
            elif symbol == ">":
                instructions.append(Coords(0, 1))
    state = State(robot_position, boxes, walls, instructions, True)
    
    for location in state.boxes.keys():
        state.boxes[location].state = state
    return state

def move(state, step):
    vector = state.instructions[step]
    intended_place = state.robot_position.add(vector)
    if intended_place in state.walls:
        return
    if intended_place not in state.boxes:
        state.robot_position = intended_place
        return
    
    # We're trying to move a box.
    if state.wide_boxes:
        box = state.boxes[intended_place]
        if box.can_move(vector, state):
            box.move(vector, state)
            state.robot_position = intended_place
    else:
        next_square = intended_place
        while next_square in state.walls or next_square in state.boxes:
            next_square = next_square.add(vector)
            if next_square in state.walls:
                # Can't move anything.
                return
        
        state.boxes[next_square] = "O"
        del(state.boxes[intended_place])
        state.robot_position = intended_place
        return



lines = get_input(use_real, example_input, __file__)

state = read_setup(lines)
for i in range(len(state.instructions)):
    move(state, i)
print(f"Part 1: {state.get_gps()}") # 1318523

double_state = read_setup_double(lines)
for i in range(len(double_state.instructions)):
    move(double_state, i)
print(f"Part 2: {double_state.get_gps()}") # 1337648
