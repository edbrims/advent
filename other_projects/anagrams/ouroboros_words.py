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
    for i in range(3,len(word) - 1):
        if word[-i:] == word[:i] and word != f"{word[:i]}{word[:i]}":
            overlap_length = len(word) - i
            print(f"{word[:i]} {word} ({overlap_length})")
