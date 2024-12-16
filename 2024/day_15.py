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

class Box:
    def __init__(self, r, c1, width, state):
        self.left_square = Coords(r, c1)
        self.state = state
        self.width = width

    def right_square(self):
        return self.left_square.add(Coords(0, self.width - 1))

    def squares(self):
        return [self.left_square.add(Coords(0, i)) for i in range(self.width)]

    def can_move(self, vector, state):
        if vector.r == 0:
            # Moving horizontally.
            if vector.c < 0:
                # Left
                next_squares = [self.left_square.add(vector)]
            elif vector.c > 0:
                # Right
                next_squares = [self.right_square().add(vector)]
        else:
            # Moving vertically
            next_squares = [p.add(vector) for p in self.squares()]

        for next_square in next_squares:
            if next_square in state.walls:
                return False
            if next_square in state.boxes:
                other_can_move = state.boxes[next_square].can_move(vector, state)
                if other_can_move:
                    continue
                return False
        return True

    def move(self, vector, state):
        if vector.r == 0:
            # Moving horizontally.
            if vector.c < 0:
                # Left
                next_squares = [self.left_square.add(vector)]
            elif vector.c > 0:
                # Right
                next_squares = [self.right_square().add(vector)]
        else:
            # Moving vertically
            next_squares = [self.left_square.add(vector), self.right_square().add(vector)]

        for next_square in next_squares:
            if next_square in state.walls:
                raise Exception(f"Can't move {self} to {next_square} because it's a wall")
            # Clear the way
            if next_square in state.boxes:
                state.boxes[next_square].move(vector, state)
        # Move this box.
        for square in self.squares():
            del(self.state.boxes[square])
        self.left_square = self.left_square.add(vector)
        for square in self.squares():
            self.state.boxes[square] = self

    def __repr__(self):
        return f"Block in ({self.left_square.r}, {self.left_square.c}-{self.right_square().c})"

    def __eq__(self, __value: object) -> bool:
        return self.left_square == __value.left_square

    def __hash__(self) -> int:
        return self.left_square.__hash__()

class State:
    def __init__(self, robot_position, boxes, walls, instructions, width):
        self.robot_position = robot_position
        self.boxes = boxes
        self.walls = walls
        self.instructions = instructions
        self.width = width

    def move_robot(self, vector):
        intended_place = self.robot_position.add(vector)
        if intended_place in self.walls:
            return
        if intended_place not in self.boxes:
            self.robot_position = intended_place
            return

        # We're trying to move a box.
        box = self.boxes[intended_place]
        if box.can_move(vector, self):
            box.move(vector, self)
            self.robot_position = intended_place

    def get_gps(self):
        total = 0
        for box in set(self.boxes.values()):
            total += 100 * box.left_square.r + box.left_square.c
        return total

    def run_instructions(self):
        for vector in self.instructions:
            self.move_robot(vector)

    def __repr__(self):
        return f"Robot at {self.robot_position}"

def read_setup(lines, width):
    boxes = {}
    walls = set()
    instructions = []
    robot_position = None
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            symbol = line[c]
            if symbol == "@":
                robot_position = Coords(r, width * c)
            elif symbol == "#":
                for i in range(width):
                    walls.add(Coords(r, width * c + i))
            elif symbol == "O":
                box = Box(r, width * c, width, None)
                for i in range(width):
                    boxes[Coords(r, width * c + i)] = box
            elif symbol == "^":
                instructions.append(Coords(-1, 0))
            elif symbol == "v":
                instructions.append(Coords(1, 0))
            elif symbol == "<":
                instructions.append(Coords(0, -1))
            elif symbol == ">":
                instructions.append(Coords(0, 1))
    state = State(robot_position, boxes, walls, instructions, width)

    for location in state.boxes.keys():
        state.boxes[location].state = state
    return state

lines = get_input(use_real, example_input, __file__)

for width in [1, 2]:
    state = read_setup(lines, width)
    state.run_instructions()
    print(f"Part {width}: {state.get_gps()}") # 1318523, 1337648
