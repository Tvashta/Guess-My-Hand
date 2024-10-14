import random
from itertools import chain
from CardGame import Player, Deck, Card

PARTNERS = {
    "North": "South",
    "East": "West",
    "South": "North",
    "West": "East",
}

SUIT_TO_NUM = {"Hearts": 0, "Spades": 13, "Diamonds": 26, "Clubs": 39}

VAL_TO_NUM = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}

NUM_TO_SUIT = {v: k for k, v in SUIT_TO_NUM.items()}
NUM_TO_VAL = {v: k for k, v in VAL_TO_NUM.items()}

DECK = {
    "North": set(range(1, 53)),
    "East": set(range(1, 53)),
    "South": set(range(1, 53)),
    "West": set(range(1, 53)),
}

DISCARD_PILE = set()


def generate_permutation(perm_size):
    """Generates a permutation dictionary, each card points to one permutation"""
    numbers = list(range(1, 53))
    perms = {}

    for i in range(1, 53):
        perms[i] = random.sample(numbers, perm_size)
    return perms


def initilize_permutations():
    """Generates a dictionary with keys 1 to 12, values are permutations of decreasing size"""
    result = {}
    for key in range(1, 14):
        perm_size = 13 - key
        perms = generate_permutation(perm_size)
        result[key] = perms
    return result


PERMUTATIONS = initilize_permutations()


def card_to_val(card: Card):
    """Converts suit and value into a number from 1-52"""
    return SUIT_TO_NUM[card.suit] + VAL_TO_NUM[card.value]


def val_to_card(val: int) -> Card:
    """Converts a number from 1-52 into a Card object"""
    if val < 1 or val > 52:
        raise ValueError("Value must be between 1 and 52")

    for base in [39, 26, 13, 0]:
        if val > base:
            suit = NUM_TO_SUIT[base]
            break

    # Determine the value
    card_val = val - base
    value = NUM_TO_VAL[card_val]

    return Card(suit, value)


def playing(player: Player, deck: Deck):
    game_round = len(player.played_cards) + 1
    my_cards = [card_to_val(card) for card in player.hand]

    # Find least similar permutations to players cards
    if game_round < 4:
        card_index = 0
        least_sim = 0
        for i, k in enumerate(my_cards):
            perms = PERMUTATIONS[game_round][k]
            sim = len((set(my_cards) & set(perms)) - {k})
            if sim < least_sim:
                card_index = i
                least_sim = sim

        if sim > 0:
            discard = set(my_cards).intersection(
                set(PERMUTATIONS[game_round][my_cards[card_index]])
                - {my_cards[card_index]}
            )
            DISCARD_PILE.update(discard)

        return card_index

    if len(DISCARD_PILE) > 0:
        priority_cards = set(my_cards) & DISCARD_PILE
        if not priority_cards:
            return random.randint(0, len(my_cards) - 1)

        card_to_play = priority_cards.pop()
        return my_cards.index(card_to_play)


def guessing(player: Player, cards, round):
    global DECK
    game_round = len(player.played_cards)

    known_cards = set(card_to_val(card) for card in player.hand)
    known_cards.update(card_to_val(card) for card in player.played_cards)

    for exposed_cards in player.exposed_cards.values():
        known_cards.update(card_to_val(card) for card in exposed_cards)

    DECK[player.name] = DECK[player.name] - known_cards

    if game_round < 4:
        perm_index = card_to_val(player.exposed_cards[PARTNERS[player.name]][-1])
        DECK[player.name] = DECK[player.name] - set(
            PERMUTATIONS[game_round][perm_index]
        )

    if len(DECK[player.name]) < 13 - game_round:
        guess_deck = random.sample(list(DECK[player.name]), len(DECK[player.name]))
        random_deck = random.sample(
            list(set(range(1, 53)) - known_cards),
            13 - game_round - len(DECK[player.name]),
        )
        guess_deck.extend(random_deck)
    else:
        guess_deck = random.sample(list(DECK[player.name]), 13 - game_round)

    card_guesses = [val_to_card(i) for i in guess_deck]

    return card_guesses
