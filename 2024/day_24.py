from collections import defaultdict
from utils import get_input

use_real = True
example_input = '''
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
'''

class Gate:
    def __init__(self, wire_1, wire_2, operator, output):
        self.wire_1 = wire_1
        self.wire_2 = wire_2
        self.operator = operator
        self.output = output

    def __repr__(self):
        return f"{self.wire_1} {self.operator} {self.wire_2} -> {self.output}"

    def evaluate(self, values, gates):
        if self.output in values:
            return values[self.output]

        # print(f"Evaluating {self}. {self.wire_1} in {values}? {self.wire_1 in values}")
        if self.wire_1 in values:
            value_1 = values[self.wire_1]
        else:
            value_1 = gates[self.wire_1].evaluate(values, gates)

        if self.wire_2 in values:
            value_2 = values[self.wire_2]
        else:
            value_2 = gates[self.wire_2].evaluate(values, gates)

        if self.operator == "AND":
            answer = value_1 and value_2
        if self.operator == "OR":
            answer = value_1 or value_2
        if self.operator == "XOR":
            answer = (value_1 != value_2)
        values[self.output] = answer
        return answer

def read_values_and_gates():
    [initial_value_strings, gate_strings] = get_input(use_real, example_input, __file__, True)

    values = defaultdict(lambda: 0)
    for line in initial_value_strings:
        [wire, value] = line.split(": ")
        values[wire] = (value == "1")

    gates = {}
    for gate_string in gate_strings:
        [input, output] = gate_string.split(" -> ")
        [wire_1, operator, wire_2] = input.split(" ")
        gates[output] = Gate(wire_1, wire_2, operator, output)

    return [values, gates]

def read_z_wires(values, gates):
    number = 0
    for i in range(100):
        z_wire = f"z{i:02}"
        if z_wire not in gates:
            break
        z_gate = gates[z_wire]
        z_wire_value = z_gate.evaluate(values, gates)
        if z_wire_value:
            number += (1 << i)
    return number

[values, gates] = read_values_and_gates()

print(f"Part 1: {read_z_wires(values, gates)}") # 53190357879014
print(f"Part 2: {0}")
