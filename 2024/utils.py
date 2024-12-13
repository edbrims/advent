def get_input(use_real: bool, example_input: str, code_path: str):
    if (use_real):
        input_path = code_path[:-3] + '_input.txt'
        raw_input = open(input_path, "r").read()
    else:
        raw_input = example_input

    return [l for l in raw_input.split('\n') if l]

class Coords:
    def __init__(self, r, c):
        self.r = r
        self.c = c

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
