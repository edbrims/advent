from enum import Enum

def display_suit(suit):
    if suit == Suit.SPADES:
        return '♠'
    if suit == Suit.HEARTS:
        return '♥'
    if suit == Suit.DIAMONDS:
        return '♦'
    if suit == Suit.CLUBS:
        return '♣'
    return str(suit)
def display_value(value):
    if value == 1:
        return 'A'
    if value == 11:
        return 'J'
    if value == 12:
        return 'Q'
    if value == 13:
        return 'K'
    return str(value)

class Suit(Enum):
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

class FaroDirection(Enum):
    IN = 1
    OUT = 2

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f'{display_value(self.value)}{display_suit(self.suit)}'

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value and self.suit == __value.suit

    def __hash__(self) -> int:
        return self.value + self.suit.__hash__() * 100

class Order(Enum):
    SPANISH_NEW_DECK = 1
    US_NEW_DECK = 2
    JOSHUA_JAY_NEW_DECK = 3
    MNEMONICA = 4
    PARTICLE = 5
    BIKONICA = 6
    MISHRA = 7
    EDONICA = 8

def ascending_suit():
    return range(1, 14)
def descending_suit():
    return range(13, 0, -1)

def partial_faro(cards, faro_direction, number_in_top = 26):
    if number_in_top * 2 > len(cards):
        raise Exception('I haven\'t thought about how to do a partial faro with more than half the cards')

    faroed = []
    top_block = cards[:number_in_top]
    bottom_block = cards[number_in_top:]
    for i in range(number_in_top):
        if faro_direction == FaroDirection.OUT:
            faroed.append(top_block[i])
            faroed.append(bottom_block[i])
        else:
            faroed.append(bottom_block[i])
            faroed.append(top_block[i])
    if number_in_top < len(bottom_block):
        faroed = faroed + bottom_block[number_in_top:]
    if set(faroed) != set(cards):
        print('Cards don\'t match!')
    if len(faroed) != len(cards):
        print('Wrong number of cards!')
    return faroed

def faro(cards, faro_direction):
    return partial_faro(cards, faro_direction, len(cards) // 2)

def antifaro(cards, num_piles):
    antifaroed_cards = []
    for i in range(num_piles):
        antifaroed_cards.extend([cards[j] for j in range(i, len(cards), num_piles)])
    return antifaroed_cards

def cut_to_face(cards, card):
    index = cards.index(card)
    return cards[index + 1:] + cards[:index + 1]

def print_colours(cards):
    print(''.join(['.' if card.suit in {Suit.SPADES, Suit.CLUBS} else 'R' for card in cards]))
def print_cards(cards, intro = ''):
    print(intro + ' '.join([str(card) for card in cards]))

def n_faros(cards, n):
    for i in range(n):
        cards = faro(cards, FaroDirection.OUT)
    return cards

def shuffle_to_mnemonica(cards, face_card):
    cards = n_faros(cards, 4)
    # cards = antifaro(antifaro(cards, 4), 4) # Equivalent to 4 antifaros = 4 faros
    cards = cards[:26][::-1] + cards[26:]
    cards = partial_faro(cards, FaroDirection.OUT, 18)
    cards = cut_to_face(cards, face_card)
    return cards

def akakkaka():
    return [ascending_suit(), ascending_suit(), descending_suit(), descending_suit()]

def akkaakka():
    return [ascending_suit(), descending_suit(), ascending_suit(), descending_suit()]

def get_new_deck(runs, suit_order):
    deck = []
    for (run, suit) in zip(runs, suit_order):
        deck.extend([Card(v, suit) for v in run])
    return deck

def get_particle_deck(suit_order):
    return n_faros(get_deck(Order.JOSHUA_JAY_NEW_DECK), 2)

    # Equivalently:
    # deck = []
    # for (red, black) in zip(ascending_suit(), descending_suit()):
    #     deck.append(Card(red, suit_order[0]))
    #     deck.append(Card(black, suit_order[1]))
    #     deck.append(Card(red, suit_order[2]))
    #     deck.append(Card(black, suit_order[3]))
    # return deck

def get_deck(order):
    if order == Order.SPANISH_NEW_DECK:
        return get_new_deck(akakkaka(), [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS])
    if order == Order.US_NEW_DECK:
        return get_new_deck(akakkaka(), [Suit.HEARTS, Suit.CLUBS, Suit.DIAMONDS, Suit.SPADES])
    if order == Order.JOSHUA_JAY_NEW_DECK:
        return get_new_deck(akkaakka(), [Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS])
    if order == Order.PARTICLE:
        return get_particle_deck([Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS])
    if order == Order.MNEMONICA:
        return shuffle_to_mnemonica(get_deck(Order.SPANISH_NEW_DECK), Card(9, Suit.DIAMONDS))
    if order == Order.BIKONICA:
        return shuffle_to_mnemonica(get_deck(Order.US_NEW_DECK), Card(9, Suit.DIAMONDS))
    if order == Order.MISHRA:
        return shuffle_to_mnemonica(get_new_deck(akakkaka(), [Suit.HEARTS, Suit.CLUBS, Suit.SPADES, Suit.DIAMONDS]), Card(9, Suit.SPADES))
    if order == Order.EDONICA:
        return shuffle_to_mnemonica(get_new_deck(akakkaka(), [Suit.CLUBS, Suit.HEARTS, Suit.DIAMONDS, Suit.SPADES]), Card(9, Suit.DIAMONDS))


def count_faros_to_restore(max_cards):
    print(f'Cards,Out-faros,In-faros')
    for num_cards in range(2, max_cards + 1, 2):
        original_order = list(range(num_cards))
        cards = list(range(num_cards))
        num_out_faros = 0
        while num_out_faros == 0 or cards != original_order:
            cards = faro(cards, FaroDirection.OUT)
            num_out_faros += 1
        cards = list(range(num_cards))
        num_in_faros = 0
        while num_in_faros == 0 or cards != original_order:
            cards = faro(cards, FaroDirection.IN)
            num_in_faros += 1
        print(f'{num_cards},{num_out_faros},{num_in_faros}')

def get_value_spellings(value):
    if value == 1:
        return ['A', 'Ace']
    if value == 2:
        return ['12', 'Two']
    if value == 3:
        return ['123', 'Three']
    if value == 4:
        return ['1234', 'Four']
    if value == 5:
        return ['12345', 'Five']
    if value == 6:
        return ['123456', 'Six']
    if value == 7:
        return ['1234567', 'Seven']
    if value == 8:
        return ['12345678', 'Eight']
    if value == 9:
        return ['123456789', 'Nine']
    if value == 10:
        return ['123456789T', 'Ten']
    if value == 11:
        return ['A23456789TJ', 'Jack']
    if value == 12:
        return ['A23456789TJQ', 'Queen']
    if value == 13:
        return ['A23456789TJQK', 'King']

def get_suit_spelling(suit):
    if suit == Suit.SPADES:
        return 'Spades'
    if suit == Suit.HEARTS:
        return 'Hearts'
    if suit == Suit.DIAMONDS:
        return 'Diamonds'
    if suit == Suit.CLUBS:
        return 'Clubs'


def spell_to_card(card, number):
    value_spellings = get_value_spellings(card.value)
    suit_spelling = get_suit_spelling(card.suit)
    spellings = []
    for value_spelling in value_spellings:
        spellings.append(value_spelling)
        spellings.append(f'{value_spelling}{suit_spelling[:-1]}')
        spellings.append(f'{value_spelling}{suit_spelling}')
        spellings.append(f'{value_spelling} {suit_spelling}')
        spellings.append(f'{value_spelling}Of{suit_spelling}')
        spellings.append(f'{value_spelling} of {suit_spelling}')

    for spelling in spellings:
        if len(spelling) == number:
            return f'"{spelling}" - spell to card'
        if len(spelling) == 53 - number:
            return f'"{spelling}" - spell from bottom'
        if len(spelling) == number - 1:
            return f'"{spelling}" - next card'
        if len(spelling) == 52 - number:
            return f'"{spelling}" - remove from bottom, next card'
        if len(spelling) == number + 1:
            return f'"{spelling}" - double lift'
    return None

def print_spellings(cards):
    for i in range(len(cards)):
        card = cards[i]
        spelling = spell_to_card(card, i+1)
        print(f'{card}: {spelling}')



# print_cards(get_deck(Order.MNEMONICA))
# print_cards(get_deck(Order.EDONICA))

deck = get_deck(Order.PARTICLE)
print_cards(deck)
print_cards(antifaro(deck, 4))


# print_cards(get_deck(Order.JOSHUA_JAY_NEW_DECK), "J: ")


# print_cards(get_deck(Order.BIKONICA))

# count_faros_to_restore(100)

# deck = get_deck(Order.EDONICA)
# print_cards(deck)
# print_spellings(deck)
