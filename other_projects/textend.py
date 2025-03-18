starting_word = "text"
available_letters = ["e", "x", "t", "e", "n", "d"]
cash = 20
score = 0

def get_valid_words():
    input_path = __file__[:-10] + "anagrams/words.txt"
    input = open(input_path, "r").read()
    return {w for w in input.split('\n') if w}

def display_status():
    print(f"Your cash: ${cash}")
    print(f"Your score: {score}")
    print(f"Current word: {current_word.upper()}")
    print(f"Available letters: {[l.upper() for l in sorted(available_letters)]}")

def get_overlap(first_word, second_word):
    for i in range(min(len(first_word) - 1, len(second_word) - 1), 1, -1):
        if first_word[-i:] == second_word[:i]:
            return first_word[-i:]
    return None


def can_make(word, available_letters):
    letters = [l for l in word]
    still_available = available_letters.copy()
    for letter in letters:
        if letter in still_available:
            still_available.remove(letter)
        else:
            return False
    return True

current_word = starting_word
word_chain = [starting_word]
valid_words = get_valid_words()

while cash > 0:
    print()
    display_status()
    move = input("Enter an overlapping word, or two letters to make a swap (for $1), or just press enter to end the game.   ")
    if not move:
        break

    if len(move) == 2:
        letter_to_remove = move[0].lower()
        if letter_to_remove not in available_letters:
            print(f"You don't have a {letter_to_remove.upper()} to remove.")
            continue

        cash -= 1
        available_letters.remove(letter_to_remove)
        available_letters.append(move[1].lower())
        continue

    new_word = move.lower()
    print()

    if not can_make(new_word, available_letters):
        print(f"Sorry, you don't have the letters to make {new_word}")
        continue

    if new_word not in valid_words:
        print(f"Sorry, {new_word.upper()} is not a valid word")
        continue

    overlap = get_overlap(current_word, new_word)
    if not overlap:
        print(f"Sorry, not allowed because there is no overlap between {current_word} and {new_word}")
        continue

    print(f"Your overlap {overlap.upper()} ({len(overlap)}) scores you {len(overlap)} × {len(new_word)} = {len(overlap) * len(new_word)} points")
    score += len(overlap) * len(new_word)
    word_chain.append(new_word)
    current_word = new_word

print()
print(f"Final score: {score}")
print(f"Word chain: {[w.upper() for w in word_chain]}")
