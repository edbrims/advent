from collections import defaultdict
import re
import unicodedata

def read(list_name):
    input = open(f"{list_name}.txt", "r").read()
    return [l for l in input.split('\n') if l]

# lines = read("words")
lines = read("vital") + read("books") + read("films") + read("songs") + read("words")

def default():
    return set()

words = set()

for line in lines:
    displayed = re.sub(' \(Level [0-9]+\)', '', line.strip())
    lowercase = unicodedata.normalize('NFD', displayed.lower())
    without_brackets = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", lowercase)
    word = ''.join([c for c in without_brackets if c in 'qwertyuiopasdfghjklzxcvbnm'])

    # if word and len(word) < 7:
    #     continue

    words.add(word)

for word in words:
    if word and len(word) < 8:
        continue

    for i in range(1, len(word)):
        part1 = word[:i]
        part2 = word[i:]

        if (len(part1) == 1 or len(part2) == 1):
            continue

        # if (part1 in words and part2 in words):
        #     continue

        rotated_word = part2 + part1
        # print(rotated_word)

        angle_size = min(len(part1), len(part2)) / len(rotated_word)
        if (angle_size <= 0.25 or angle_size >= 0.5):
            continue

        if (rotated_word != word and rotated_word in words):
            print(f'{word}, {rotated_word} ({min(len(part1), len(part2))}/{len(rotated_word)} = {angle_size})')
