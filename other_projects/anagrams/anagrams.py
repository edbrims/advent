from collections import defaultdict
import re
import unicodedata

def read(list_name):
    input = open(f"{list_name}.txt", "r").read()
    return [l for l in input.split('\n') if l]

lines = read("vital") #+ read("books") + read("films") + read("songs") + read("words")

def default():
    return set()

unique_letters = defaultdict(default)
names = defaultdict(default)

for line in lines:
    displayed = re.sub(' \(Level [0-9]+\)', '', line.strip())
    lowercase = unicodedata.normalize('NFD', displayed.lower())
    without_brackets = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", lowercase)
    letters = ''.join([c for c in without_brackets if c in 'qwertyuiopasdfghjklzxcvbnm'])

    if letters and len(letters) < 7:
        continue

    sorted_letters = ''.join(sorted([c for c in without_brackets if c in 'qwertyuiopasdfghjklzxcvbnm']))
    unique_letters[sorted_letters].add(letters)
    names[sorted_letters].add(displayed)

for letters in unique_letters.keys():
    if (len(unique_letters[letters]) > 1):
        print(', '.join(names[letters]))
