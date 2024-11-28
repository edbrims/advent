input = open("day_20_input.txt", "r").read()

# Example 1
# input = '''
# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a'''

# # Example 2
# input = '''
# broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output'''

lines = [l for l in input.split('\n') if l]

class Module:
    def __init__(self, name, type, targets):
        self.name = name
        self.type = type
        self.targets = targets
        self.on = False # Only flip-flops
        # self.highs_from = set()
        self.input_highs = {} # Only conjunctions
    def __repr__(self):
        on_string = ''
        if self.type == 'flip-flop':
            on_string = ' ON' if self.on else ' OFF'
        return f'{self.type} {self.name}{on_string}: {self.targets}'

class Pulse:
    def __init__(self, source, is_high, target):
        self.source = source
        self.target = target
        self.is_high = is_high
    def __repr__(self):
        high_string = 'high' if self.is_high else 'low'
        # return f'{high_string} to {self.target}'
        return f'{self.source} -{high_string}-> {self.target}'

modules = {}

for line in lines:
    parts = line.split(' -> ')
    if parts[0] == 'broadcaster':
        type = 'broadcaster'
        name = parts[0]
    elif parts[0][0] == '%':
        type = 'flip-flop'
        name = parts[0][1:]
    elif parts[0][0] == '&':
        type = 'conjunction'
        name = parts[0][1:]
    else:
        print(f'What is {parts[0]}?')
    targets = parts[1].split(', ')

    modules[name] = Module(name, type, targets)

# Tell conjunctions about their inputs
for module in modules.values():
    for target_name in module.targets:
        # print(f'Telling {target_name} about its input {module}')
        if target_name not in modules:
            # print(f'No module {target_name}')
            continue
        target_module = modules[target_name]
        if target_module.type == 'conjunction':
            target_module.input_highs[module.name] = False

    # print(f'{type} {name}: {targets}')
# print(modules)

def send_pulses(is_high, source, targets, queue):
    for target in targets:
        queue.append(Pulse(source, is_high, target))

low_turns = {'zz': [], 'mh': [], 'kd': [], 'cm': []}

def press_button(which_turn):
    queue = [Pulse('button', False, 'broadcaster')]

    low_pulses_handled = 0
    high_pulses_handled = 0
    while queue:
        input_pulse : Pulse = queue.pop(0)
        input_is_high = input_pulse.is_high
        if input_is_high:
            high_pulses_handled += 1
        else:
            low_pulses_handled += 1

        if input_pulse.target not in modules:
            if input_pulse.target == 'rx' and not input_pulse.is_high:
                print(f'Got a low one to rx!')
                return -1
            # print(f'Processing {input_pulse} - no target! Dropping')
            continue

        module : Module = modules[input_pulse.target]
        # print(f'Processing {input_pulse} ({module.type})')
        if module.type == 'broadcaster':
            send_pulses(input_is_high, module.name, module.targets, queue)
            # for target in module.targets:
            #     queue.append(Pulse(module.name, input_is_high, target))
        elif module.type == 'flip-flop':
            if not input_is_high:
                module.on = not module.on
                # print(f'{module.name} got a low pulse, flipped to {module.on}')
                output_is_high = module.on
                send_pulses(output_is_high, module.name, module.targets, queue)
        elif module.type == 'conjunction':
            most_recent_was_high = module.input_highs[input_pulse.source]
            module.input_highs[input_pulse.source] = input_is_high
            # Send high if there is at least one low input
            output_is_high = False in module.input_highs.values()

            if module.name in low_turns and not output_is_high:
                # print(f'{module.name} sending low on {which_turn}')
                low_turns[module.name].append(which_turn)

            send_pulses(output_is_high, module.name, module.targets, queue)
    return [high_pulses_handled, low_pulses_handled]


high_pulses_handled = 0
low_pulses_handled = 0
for i in range(1000):
    pulses = press_button(i+1)
    high_pulses_handled += pulses[0]
    low_pulses_handled += pulses[1]

print(f'Part 1: {high_pulses_handled * low_pulses_handled}')
# 938065580 is right!

# Part 2
for i in range(20000):
    pulses = press_button(i+1)

overall_cycle_length = 1
for conjunction in low_turns.keys():
    low_turn = low_turns[conjunction]
    differences = [low_turn[i+1] - low_turn[i] for i in range(len(low_turn) - 1)]
    print(f'{conjunction} cycle: {differences}')
    if min(differences) != max(differences):
        print(f'These differences don\'t work: {differences}')
    overall_cycle_length *= differences[0] # Reall LCM, but this'll do.

print(f'Part 2: {overall_cycle_length}')
# 250628960065793 is right!
