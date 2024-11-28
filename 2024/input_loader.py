def get_input(use_real: bool, example_input: str, code_path: str):
    if (use_real):
        input_path = code_path[:-3] + '_input.txt'
        raw_input = open(input_path, "r").read()
    else:
        raw_input = example_input

    return [l for l in raw_input.split('\n') if l]
