from utils import get_input

use_real = True
example_input = '''
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
'''

example_input = '''
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''

class Machine:
    def __init__(self, register_a, register_b, register_c, program):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = [int(c) for c in program.split(",")]
        self.instruction_pointer = 0
        self.out = []

    def __repr__(self):
        return f'''Register A: {self.register_a}
Register B: {self.register_b}
Register C: {self.register_c}

Program: {", ".join([str(c) for c in self.program])}
Output: {self.out_text()}'''

    def out_text(self):
        return ",".join([str(c) for c in self.out])

    def combo(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        raise Exception(f"Bad combo operand {operand}")

    def run_opcode(self, opcode, operand):
        if opcode == 0:
            # adv: A/2^combo --> A
            self.register_a = self.register_a // (2 ** self.combo(operand))
        elif opcode == 1:
            # bxl: B xor literal --> B
            self.register_b = self.register_b ^ operand
        elif opcode == 2:
            # bst: combo % 8 --> B
            self.register_b = self.combo(operand) % 8
        elif opcode == 3:
            # jnz: Jump to literal
            if self.register_a != 0:
                self.instruction_pointer = operand
                return # So we don't increase by 2.
        elif opcode == 4:
            # bxc: b XOR c --> B
            self.register_b = self.register_b ^ self.register_c
        elif opcode == 5:
            # out: combo % 8 --> output
            output = self.combo(operand) % 8
            self.out.append(output)
        elif opcode == 6:
            # bdv: A/2^combo --> B
            self.register_b = self.register_a // (2 ** self.combo(operand))
        elif opcode == 7:
            # cdv: A/2^combo --> C
            self.register_c = self.register_a // (2 ** self.combo(operand))

        self.instruction_pointer += 2

    def run(self):
        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1]
            self.run_opcode(opcode, operand)
        return self

def load_machine(lines):
    return Machine(int(lines[0][12:]),
                   int(lines[1][12:]),
                   int(lines[2][12:]),
                   lines[3][9:])

lines = get_input(use_real, example_input, __file__)

# All the tests...
# # If register C contains 9, the program 2,6 would set register B to 1.
# print(Machine(0, 0, 9, "2,6").run().register_b)
# # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
# print(Machine(10, 0, 9, "5,0,5,1,5,4").run().out)
# # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
# print(Machine(2024, 0, 0, "0,1,5,4,3,0").run().out)
# print(Machine(2024, 0, 0, "0,1,5,4,3,0").run().register_a)
# # If register B contains 29, the program 1,7 would set register B to 26.
# print(Machine(0, 29, 0, "1,7").run().register_b)
# # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
# print(Machine(0, 2024, 43690, "4,0").run().register_b)

machine = load_machine(lines)
machine.run()
print(f"Part 1: {machine.out_text()}") # 1,5,7,4,1,6,0,3,0

# OK, it's actually much much simpler. Forget all the stuff above, this is the program.
def run_program(a):
    out = []
    verbose = False
    while a > 0:
        if verbose:
            print(f"a={a:b}")
        b = a % 8 # Last 3 bits of A
        if verbose:
            print(f"b={b:b} (last 3 bits of a)")
        b = b ^ 3 # Flip the last 2 bits of b
        if verbose:
            print(f"b={b:b}={b} (flipped last 2 bits)")        
        c = a >> b # A without its last b bits
        if verbose:
            print(f"c={c:b} (Dropped {b} bits of a)")        
        b = b ^ c # XOR c with b
        if verbose:
            print(f"b={b:b} (XOR with c)")        
        b = b ^ 3 # Flip the last 2 bits of b
        if verbose:
            print(f"b={b:b} (flipped last 2 bits)")        
        a = a >> 3 # Reduce A by 3 bits
        if verbose:
            print(f"a={a:b} (Dropped 3 bits)")        
        out.append(b % 8)
        if verbose:
            print(f"Output {b%8:b} (Last 3 bits of b)")
            print()
    return out

print(run_program(51342988))
# Looking for 2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0
print(f"Part 2: {0}")
