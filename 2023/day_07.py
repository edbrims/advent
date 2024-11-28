# Day 7
input = open("day_07_input.txt", "r").read()

# Test
# input = '''32T3K 765
# T55J5 684
# KK677 28
# KTJJT 220
# QQQJA 483'''


def card_str_to_num(card_string):
    cards = []
    for char in card_string:
        if char == 'A':
            cards.append(14)
        elif char == 'K':
            cards.append(13)
        elif char == 'Q':
            cards.append(12)
        elif char == 'J':
            cards.append(11)
        elif char == 'T':
            cards.append(10)
        else:
            cards.append(int(char))
    return cards

score_names = ['', 'High card', 'One pair', 'Two pair', 'Three of a kind', 'Full house', 'Four of a kind', 'Five of a kind']

# 7: Five of a kind
# 6: Four of a kind
# 5: Full house
# 4: Three of a kind
# 3: Two pair
# 2: One pair
# 1: High card
def score_hand(cards):
    cards = sorted(cards)

    if cards[0] == cards[4]:
        # Five of a kind
        return 7

    if cards[0] == cards[3] or cards[1] == cards[4]:
        # Four of a kind
        return 6

    if (cards[0] == cards[2] and cards[3] == cards[4]) or (cards[0] == cards[1] and cards[2] == cards[4]):
        # Full house
        return 5

    if cards[0] == cards[2] or cards[1] == cards[3] or cards[2] == cards[4]:
        # Three of a kind
        return 4

    if (cards[0] == cards[1] and cards[2] == cards[3]) or (cards[0] == cards[1] and cards[3] == cards[4]) or (cards[1] == cards[2] and cards[3] == cards[4]):
        # Two pair
        return 3

    if cards[0] == cards[1] or cards[1] == cards[2] or cards[2] == cards[3] or cards[3] == cards[4]:
        # One pair
        return 2

    return 1

def second_sorting(cards):
    total = 0
    for card in cards:
        total = total * 15 + card
    return total

# score_hand(card_str_to_num('KK2KK'))
hand_infos = []
hands = [l for l in input.split('\n') if l]
for hand in hands:
    card_string, bid_str = hand.split(' ')
    bid = int(bid_str)
    cards = card_str_to_num(card_string)
    score = score_hand(cards)
    magic_number = second_sorting(cards)
    overall_score = score * 10000000 + magic_number
    hand_infos.append({'card_string': card_string, 'overall_score': overall_score, 'bid': bid, 'score': score_names[score]})

sorted_hands = sorted(hand_infos, key=lambda d: d['overall_score'])
for i in range(len(sorted_hands)):
    sorted_hands[i]['rank'] = i+1

winnings = 0
for hand in sorted_hands:
    winnings += hand['bid'] * hand['rank']
print(f'Part 1: {winnings}')

# 250370104 is right.

# Part 2
# Replacement functions
def card_str_to_num(card_string):
    cards = []
    for char in card_string:
        if char == 'A':
            cards.append(14)
        elif char == 'K':
            cards.append(13)
        elif char == 'Q':
            cards.append(12)
        elif char == 'J':
            cards.append(1) # Joker scores lower than a 2.
        elif char == 'T':
            cards.append(10)
        else:
            cards.append(int(char))
    return cards

# 7: Five of a kind
# 6: Four of a kind
# 5: Full house
# 4: Three of a kind
# 3: Two pair
# 2: One pair
# 1: High card
def score_hand(cards):
    cards = sorted([c for c in cards if c != 1])

    if len(cards) <= 1:
        # Five of a kind (JJJJ5)
        return 7
    if cards[0] == cards[-1]:
        # Five of a kind, regardless of jokers (JJ333)
        return 7

    if cards[0] == cards[-2] or cards[1] == cards[-1]:
        # Four of a kind (JJ466)
        return 6

    # Urgh, let's just write it all out from here...
    if len(cards) == 5:
        if (cards[0] == cards[2] and cards[3] == cards[4]) or (cards[0] == cards[1] and cards[2] == cards[4]):
            # Full house
            return 5

        if cards[0] == cards[2] or cards[1] == cards[3] or cards[2] == cards[4]:
            # Three of a kind
            return 4

        if (cards[0] == cards[1] and cards[2] == cards[3]) or (cards[0] == cards[1] and cards[3] == cards[4]) or (cards[1] == cards[2] and cards[3] == cards[4]):
            # Two pair
            return 3

        if cards[0] == cards[1] or cards[1] == cards[2] or cards[2] == cards[3] or cards[3] == cards[4]:
            # One pair
            return 2

        return 1

    elif len(cards) == 4:
        # One joker.
        if cards[0] == cards[1] and cards[2] == cards[3]:
            # Full house JAABB
            return 5

        if cards[0] == cards[1] or cards[1] == cards[2] or cards[2] == cards[3]:
            # Three of a kind JAABC
            return 4

        # Everything else is one pair. It's impossible to get two pair or high card with one joker.
        return 2

    elif len(cards) == 3:
        # Two jokers.
        # All that's left is three different cards, JJABC. Otherwise we'd have hit a 4/5 case above.
        # So that's three of a kind.
        return 4

    print(f'Could not score hand {cards}')


# score_hand(card_str_to_num('KK2KK'))
hand_infos = []
hands = [l for l in input.split('\n') if l]
for hand in hands:
    card_string, bid_str = hand.split(' ')
    bid = int(bid_str)
    cards = card_str_to_num(card_string)
    score = score_hand(cards)
    magic_number = second_sorting(cards)
    overall_score = score * 10000000 + magic_number
    hand_infos.append({'card_string': card_string, 'overall_score': overall_score, 'bid': bid, 'score': score_names[score]})

sorted_hands = sorted(hand_infos, key=lambda d: d['overall_score'])
for i in range(len(sorted_hands)):
    sorted_hands[i]['rank'] = i+1

# print(sorted_hands)
winnings = 0
for hand in sorted_hands:
    winnings += hand['bid'] * hand['rank']
print(f'Part 2: {winnings}')

# 251735672
