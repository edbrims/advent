from collections import defaultdict
from utils import get_input

use_real = True
example_input = '''
1
10
100
2024
'''
example_input = '''
1
2
3
2024
'''

lines = get_input(use_real, example_input, __file__)

def get_next_secret_number(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

def repeat_secret(initial_secret, times):
    secret = initial_secret
    for i in range(times):
        secret = get_next_secret_number(secret)
    return secret

def add_2000th_secrets(initial_secrets):
    return sum([repeat_secret(s, 2000) for s in initial_secrets])

def score_all_sequences(initial_secret, bananas_by_sequence):
    sequences_already_traded = set()
    sequence = []
    secret = initial_secret
    for i in range(2000):
        next_secret = get_next_secret_number(secret)
        bananas_on_offer = next_secret % 10
        difference = bananas_on_offer - (secret % 10)
        secret = next_secret
        sequence.append(difference)
        if len(sequence) > 4:
            sequence.pop(0)
        sequence_key = tuple(sequence)
        if len(sequence) == 4 and sequence_key not in sequences_already_traded:
            bananas_by_sequence[sequence_key] += bananas_on_offer
            sequences_already_traded.add(sequence_key)

def find_most_bananas(initial_secrets):
    bananas_by_sequence = defaultdict(lambda: 0)
    for initial_secret in initial_secrets:
        score_all_sequences(initial_secret, bananas_by_sequence)

    most_bananas = 0
    for sequence, bananas in bananas_by_sequence.items():
        if bananas > most_bananas:
            most_bananas = bananas
            best_sequence = sequence
    print(f"{best_sequence} earns {most_bananas} bananas")
    return most_bananas

initial_secrets = [int(s) for s in lines]

print(f"Part 1: {add_2000th_secrets(initial_secrets)}") # 13004408787
print(f"Part 2: {find_most_bananas(initial_secrets)}") # 1455
