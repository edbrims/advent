def get_input(use_real: bool, example_input: str, code_path: str):
    if (use_real):
        input_path = code_path[:-3] + '_input.txt'
        raw_input = open(input_path, "r").read()
    else:
        raw_input = example_input

    return [l for l in raw_input.split('\n') if l]

class Coords:
    def __init__(self, r, c):
        self.r = int(r)
        self.c = int(c)

    def add(self, vector):
        return Coords(self.r + vector.r, self.c + vector.c)

    def turn_right(self):
        return Coords(self.c, -self.r)

    def turn_left(self):
        return Coords(-self.c, self.r)

    def __repr__(self):
        return f'({self.r}, {self.c})'

    def __eq__(self, __value: object) -> bool:
        return self.r == __value.r and self.c == __value.c

    def __hash__(self) -> int:
        return self.r + self.c * 1000

class XYVector:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def add(self, vector):
        return XYVector(self.x + vector.x, self.y + vector.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def __hash__(self) -> int:
        return self.x + self.y * 1000

class XYZVector:
    def __init__(self, x, y, z):
        self.x = int(coords[0])
        self.y = int(coords[1])
        self.z = int(coords[2])

    def add(self, vector):
        return XYZVector(self.x + vector.x,
                         self.y + vector.y,
                         self.z + vector.z)

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y and self.z == __value.z

    def __hash__(self) -> int:
        return self.x + self.y * 1000
