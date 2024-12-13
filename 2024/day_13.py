from utils import get_input, XYVector

use_real = True
example_input = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

class Machine:
    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize

    def __repr__(self):
        return f"[A: {self.a}, B: {self.b}, prize {self.prize}]"

lines = get_input(use_real, example_input, __file__)

def load_machines(lines, prize_offset):
    machines = []
    for i in range(len(lines) // 3):
        buttonACoordStrings = lines[3*i][12:].split(", Y+")
        buttonACoords = XYVector(buttonACoordStrings[0], buttonACoordStrings[1])
        buttonBCoordStrings = lines[3*i + 1][12:].split(", Y+")
        buttonBCoords = XYVector(buttonBCoordStrings[0], buttonBCoordStrings[1])
        prizeCoordStrings = lines[3*i + 2][9:].split(", Y=")
        prize = XYVector(prizeCoordStrings[0], prizeCoordStrings[1]).add(XYVector(prize_offset, prize_offset))
        machines.append(Machine(buttonACoords, buttonBCoords, prize))
    return machines

def bestTime(machine):
    # Press button A aTimes, button B bTimes
    #
    # Solving these two equations for ta and tb
    # ta * xa + tb * xb = xp
    # ta * ya + tb * yb = yp
    #
    # tb = (xp-ta*xa)/xb = (yp-ta*ya)/yb
    # yb*xp - ta*xa*yb = xb*yp - ta*ya*xb
    # ta(ya*xb - xa*yb) = (xb*yp-yb*xp)
    # ta = (xb*yp-yb*xp)/(ya*xb-xa*yb)
    if machine.a.y * machine.b.x == machine.a.x * machine.b.y:
        # A and B vectors are parallel. Turns out this never happens.
        raise Exception(f"{machine} has parallel vectors")

    aTimes = ((machine.b.x * machine.prize.y - machine.b.y * machine.prize.x) /
              (machine.a.y * machine.b.x - machine.a.x * machine.b.y))
    bTimes = ((machine.a.x * machine.prize.y - machine.a.y * machine.prize.x) /
              (machine.b.y * machine.a.x - machine.b.x * machine.a.y))

    aTimesInt = int(aTimes)
    bTimesInt = int(bTimes)
    if aTimes == aTimesInt and bTimes == bTimesInt and aTimes >= 0 and bTimes >= 0:
        return 3 * aTimesInt + bTimesInt
    return None

def totalBestTime(machines):
    total = 0
    for machine in machines:
        best = bestTime(machine)
        if best:
            total += best
    return total

small_machines = load_machines(lines, 0)
big_machines = load_machines(lines, 10000000000000)

print(f"Part 1: {totalBestTime(small_machines)}") # 29187
print(f"Part 2: {totalBestTime(big_machines)}") # 99968222587852
