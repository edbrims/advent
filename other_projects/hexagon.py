from collections import defaultdict

# Solving a wooden hexagonal puzzle with pieces on a triangular grid.

# The a-axis points down
# The b-axis points up and right
# The c-axis points up and left

# Vector from a point to a triangle.
class Vector:
    def __init__(self, a, b, c):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        assert a + b + c == 1 or a + b + c == 2, f"{a} + {b} + {c} = {a + b + c}"

    def turn_right(self):
        return Vector(1-self.c, 1-self.a, 1-self.b)

    def turn_left(self):
        return Vector(1-self.b, 1-self.c, 1-self.a)

    def flip(self):
        return Vector(self.a, self.c, self.b)

    def points_up(self):
        return (self.a + self.b + self.c == 1)

    def __repr__(self):
        return f'{"^" if self.points_up() else "V"}({self.a}, {self.b}, {self.c})'

    def __eq__(self, __value: object) -> bool:
        return self.a == __value.a and self.b == __value.b and self.c == __value.c

    def __hash__(self) -> int:
        return self.a + self.b * 10 + self.c * 100

class Triangle:
    def __init__(self, a, b, c):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        assert a + b + c == 10 or a + b + c == 11, f"{a} + {b} + {c} = {a + b + c}"

    def points_up(self):
        return (self.a + self.b + self.c == 10)

    def neighbours(self):
        if self.points_up():
            return [Triangle(self.a + 1, self.b, self.c), Triangle(self.a, self.b + 1, self.c), Triangle(self.a, self.b, self.c + 1)]
        else:
            return [Triangle(self.a - 1, self.b, self.c), Triangle(self.a, self.b - 1, self.c), Triangle(self.a, self.b, self.c - 1)]

    def left_neighbour(self):
        if self.points_up():
            return Triangle(self.a, self.b, self.c + 1)
        else:
            return Triangle(self.a, self.b - 1, self.c)

    def right_neighbour(self):
        if self.points_up():
            return Triangle(self.a, self.b + 1, self.c)
        else:
            return Triangle(self.a, self.b, self.c - 1)

    def __repr__(self):
        return f'{"^" if self.points_up() else "V"}{self.a}{self.b}{self.c}'

    def __eq__(self, __value: object) -> bool:
        return self.a == __value.a and self.b == __value.b and self.c == __value.c

    def __hash__(self) -> int:
        return self.a + self.b * 10 + self.c * 100

class Point:
    def __init__(self, a, b, c):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        assert a + b + c == 9, f"{a} + {b} + {c} = {a + b + c}"

    def add(self, vector):
        return Triangle(self.a + vector.a, self.b + vector.b, self.c + vector.c)

    def __repr__(self):
        return f'.{self.a}{self.b}{self.c}'

    def __eq__(self, __value: object) -> bool:
        return self.a == __value.a and self.b == __value.b and self.c == __value.c

    def __hash__(self) -> int:
        return self.a + self.b * 10 + self.c * 100

class Piece:
    def __init__(self, label, vectors):
        self.label = label

        # Shift it up and right so that translated versions of the same piece are treated as equal.
        max_a = max([v.a for v in vectors if v.points_up()])
        bottom_pieces = [v for v in vectors if v.a == max_a and v.points_up()]
        min_b = min([v.b for v in bottom_pieces])
        bottom_left_pieces = [v for v in bottom_pieces if v.b == min_b]
        min_c = min([v.c for v in bottom_left_pieces])
        (new_base,) = [v for v in bottom_left_pieces if v.c == min_c]

        self.vectors = {Vector(v.a - new_base.a + 1, v.b - new_base.b, v.c - new_base.c) for v in vectors}

    def turn_right(self):
        return Piece(self.label, [v.turn_right() for v in self.vectors])

    def turn_left(self):
        return Piece(self.label, [v.turn_left() for v in self.vectors])

    def flip(self):
        return Piece(self.label, [v.flip() for v in self.vectors])

    def rotations(self):
        rotations = {self}
        p = self
        for i in range(5):
            p = p.turn_left()
            rotations.add(p)
        p = self.flip()
        rotations.add(p)
        for i in range(5):
            p = p.turn_left()
            rotations.add(p)
        return rotations

    def __repr__(self):
        return f'{self.label}{self.vectors}'

    def __eq__(self, __value: object) -> bool:
        return self.vectors == __value.vectors

    def __hash__(self) -> int:
        vector_list = list(self.vectors)
        return sum(i * vector_list[i].__hash__() for i in range(len(vector_list)))

class Board:
    def __init__(self, triangles):
        self.triangles = set(triangles)
        self.contents = defaultdict(lambda: " ")
        self.points = set()
        for triangle in triangles:
            if triangle.points_up():
                self.points.add(Point(triangle.a-1, triangle.b, triangle.c))
                self.points.add(Point(triangle.a, triangle.b-1, triangle.c))
                self.points.add(Point(triangle.a, triangle.b, triangle.c-1))
            else:
                self.points.add(Point(triangle.a-1, triangle.b-1, triangle.c))
                self.points.add(Point(triangle.a-1, triangle.b, triangle.c-1))
                self.points.add(Point(triangle.a, triangle.b-1, triangle.c-1))

    def can_place(self, piece, point):
        for vector in piece.vectors:
            triangle = point.add(vector)
            if triangle not in self.triangles:
                return False
            if self.contents[triangle] != " ":
                return False
        return True

    def place(self, piece, point):
        assert self.can_place(piece, point), f"Can't place {piece} at {point}"
        for vector in piece.vectors:
            self.contents[point.add(vector)] = piece.label

    def remove(self, piece, point):
        for vector in piece.vectors:
            triangle = point.add(vector)
            assert self.contents[triangle] == piece.label, f"{triangle} contains {self.contents[triangle]} instead of {piece.label}"
            self.contents[triangle] = " "

    def regions(self):
        regions = []
        remaining_triangles = {t for t in self.triangles if self.contents[t] == " "}

        while remaining_triangles:
            triangle = remaining_triangles.pop()
            region = {triangle}
            queue = [triangle]
            while queue:
                triangle = queue.pop(0)

                for neighbour in triangle.neighbours():
                    if neighbour in remaining_triangles:
                        queue.append(neighbour)
                        remaining_triangles.discard(neighbour)
                        region.add(neighbour)
            regions.append(region)
        return regions

    def solve(self, pieces):
        regions = self.regions()
        for region in regions:
            if (len(region) % 3) != 0:
                # Can't solve a region that isn't a multiple of 3.
                return 0

        if not pieces:
            # Solved it!
            print(self)
            # exit()
            return 1

        count = 0
        piece = pieces.pop()
        for point in self.points:
            for rotation in piece.rotations():
                if self.can_place(rotation, point):
                    self.place(rotation, point)
                    count += self.solve(pieces)
                    self.remove(rotation, point)
        pieces.append(piece)

        return count

    def get_triangle(self, a, x, max_c):
        if a % 2 == 1:
            b = (x + 1) // 2 - (a-1)//2 + 2
            c = max_c - x//2 - (a-1)//2 + 1
        else:
            b = x // 2 - a//2 + 3
            c = max_c - (x + 1) // 2 - a//2 + 2
        return Triangle(a, b, c)

    def border_between(self, t1, t2):
        if t1 not in self.triangles and t2 in self.triangles:
            return True
        if t2 not in self.triangles and t1 in self.triangles:
            return True
        return (self.contents[t1] != self.contents[t2])

    def __repr__(self):
        min_a = min([t.a for t in self.triangles])
        max_a = max([t.a for t in self.triangles])
        min_b = min([t.b for t in self.triangles])
        max_b = max([t.b for t in self.triangles])
        min_c = min([t.c for t in self.triangles])
        max_c = max([t.c for t in self.triangles])
        repr = ""
        for a in range(min_a, max_a + 1):
            # Lines above
            for x in range((max_b - min_b) + (max_c - min_c) + 2):
                triangle_above = self.get_triangle(a - 1, x, max_c)
                if not triangle_above.points_up():
                    if x == 0:
                        repr += "   "
                    continue
                triangle_below = self.get_triangle(a, x, max_c)
                point = Point(triangle_above.a, triangle_above.b - 1, triangle_above.c)

                # A corner between triangles
                if (self.border_between(point.add(Vector(1, 0, 1)), point.add(Vector(0, 0, 1))) and
                    self.border_between(point.add(Vector(1, 1, 0)), point.add(Vector(0, 1, 0)))):
                    repr += "-"
                elif (self.border_between(point.add(Vector(1, 0, 0)), point.add(Vector(1, 0, 1))) and
                    self.border_between(point.add(Vector(0, 1, 1)), point.add(Vector(0, 1, 0)))):
                    repr += "/"
                elif (self.border_between(point.add(Vector(1, 0, 0)), point.add(Vector(1, 1, 0))) and
                    self.border_between(point.add(Vector(0, 0, 1)), point.add(Vector(0, 1, 1)))):
                    repr += "\\"
                else:
                    repr += " "

                if self.border_between(triangle_above, triangle_below):
                    repr += "-----"
                else:
                    repr += "     "

            repr += "\n "

            # Top half of triangle
            for x in range((max_b - min_b) + (max_c - min_c) + 1):
                triangle = self.get_triangle(a, x, max_c)

                if triangle in self.triangles:
                    content = self.contents[triangle][0]
                    if triangle.points_up():
                        if triangle.left_neighbour() not in self.triangles:
                            repr += " "
                        if self.border_between(triangle, triangle.left_neighbour()):
                            repr += "/"
                        else:
                            repr += " "
                        repr += " "
                        if triangle.right_neighbour() not in self.triangles:
                            repr += "\\"
                    else:
                        if self.border_between(triangle, triangle.left_neighbour()):
                            repr += "\\"
                        else:
                            repr += " "
                        repr += f"   " # {content}
                        if triangle.right_neighbour() not in self.triangles:
                            repr += "/"
                else:
                    repr += "   "
            repr += "\n "

            # Bottom half of triangle
            for x in range((max_b - min_b) + (max_c - min_c) + 1):
                triangle = self.get_triangle(a, x, max_c)

                if triangle in self.triangles:
                    content = self.contents[triangle][0]
                    if triangle.points_up():
                        if self.border_between(triangle, triangle.left_neighbour()):
                            repr += "/"
                        else:
                            repr += " "
                        repr += f"   " # {content}
                        if triangle.right_neighbour() not in self.triangles:
                            repr += "\\"
                    else:
                        if triangle.left_neighbour() not in self.triangles:
                            repr += " "
                        if self.border_between(triangle, triangle.left_neighbour()):
                            repr += "\\"
                        else:
                            repr += " "
                        repr += " "
                        if triangle.right_neighbour() not in self.triangles:
                            repr += "/"
                else:
                    repr += f"   "

            repr += "\n"

        repr += "          ----- ----- -----\n"
        return repr

triangles = []
for a in range(1, 7):
    for b in range(1, 7):
        if a + b >= 5 and a + b <= 10:
            triangles.append(Triangle(a, b, 11-a-b))
        if a + b >= 4 and a + b <= 9:
            triangles.append(Triangle(a, b, 10-a-b))

hexagon = Board(triangles)

# 54 triangles to cover. 4 matching little pieces (3 triangles each), plus 7 big pieces (6)
pieces = [
    Piece("1", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0)]), # Mini
    Piece("2", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0)]), # Mini
    Piece("3", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0)]), # Mini
    Piece("4", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0)]), # Mini
    Piece("I", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(1, 1, -1), Vector(1, 2, -1), Vector(1, 2, -2)]), # Line
    Piece("T", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(0, 1, 0), Vector(0, 2, 0), Vector(-1, 2, 0)]), # Tick
    Piece("S", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(0, 1, 1), Vector(0, 1, 0), Vector(0, 2, 0)]), # Stacked
    Piece("V", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(1, 1, -1), Vector(2, 1, -1), Vector(2, 1, -2)]), # Angle
    Piece("J", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(0, 1, 0), Vector(0, 1, 1), Vector(-1, 1, 1)]), # Squat J shape
    Piece("P", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(1, 1, -1), Vector(1, 2, -1), Vector(2, 1, -1)]), # P shape
    Piece("O", [Vector(1, 0, 1), Vector(1, 0, 0), Vector(1, 1, 0), Vector(0, 1, 0), Vector(0, 1, 1), Vector(0, 0, 1)]), # Hexagon
]

count = hexagon.solve(pieces)

print(f"There are {count} solutions")
