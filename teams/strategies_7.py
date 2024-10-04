import copy
import random
import numpy as np
from CardGame import Card, Deck, Player

# G7 is the best


SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
NUM_CARDS = len(SUITS) * len(VALUES)

# This is deprecated but for the sake of structure i'll leave it
CARD_PROBABILITIES = {num:1/39 for num in range(NUM_CARDS)}

# Create a dictionary that maps 0-51 to (value, suit)
NUM_TO_CARD = {
    i: (SUITS[i // 13], VALUES[i % 13])  # i % 13 gives the card value, i // 13 gives the suit
    for i in range(NUM_CARDS)
}

REV_CARD_TO_NUM = {value:key for key, value in NUM_TO_CARD.items()} 

def update_prob_based_on_correct_answers(probability_dict, guessed_cards, correct_answers):
    """
    Updates the probabilities for the cards in the guessed_cards list.

    Args:
        probability_dict (dict): A dictionary where keys are integers (0-51) representing cards
                                and probabilities.
        guessed_cards (list): A list of card indices representing the guessed cards.
        
    Returns:
        None: The probability_dict is updated in-place.
    """

    perc_correct = correct_answers / len(guessed_cards)  # Factor to boost guessed cards
    perc_wrong =  1 - perc_correct

    for card in guessed_cards:
            probability_dict[card] *= perc_correct

    non_guessed_cards = [card for card in probability_dict if card not in guessed_cards]

    for card in non_guessed_cards:
        probability_dict[card] *= perc_wrong

    normalize(probability_dict)

def normalize(probability_dict):
    total_prob = sum(probability_dict.values())
    if total_prob > 0:
        for card in probability_dict:
            probability_dict[card] /= total_prob

def playing(player, deck):
    """
    Max First strategy
    """
    if not player.hand:
        return None
    
    value_order = deck.values
    max_index = 0
    max_value = -1

    
    

    for i, card in enumerate(player.hand):
        value = value_order.index(card.value)
        if value > max_value:
            max_value = value
            max_index = i
    
    return max_index

def normalize_probabilities(prob_dict):
    total = sum(prob_dict.values())
    if total > 0:
        for card in prob_dict:
            prob_dict[card] /= total
    else:
        # This is after all the cards have been played - so no exception
        prob_dict[0] = 1
    return prob_dict

def zero_probabilities(prob_dict, cards):
    for card in cards:
        suit = card.suit
        val = card.value
        num = REV_CARD_TO_NUM[(suit, val)]
        prob_dict[num] = 0.0
    return normalize_probabilities(prob_dict)


def guessing(player, cards, round):
    card_probs = {num:1/39 for num in range(NUM_CARDS)}
    card_probs = zero_probabilities(card_probs, player.hand)
    exposed_cards = [i for j in list(player.exposed_cards.values()) for i in j]
    card_probs = zero_probabilities(card_probs, exposed_cards)
    card_probs = zero_probabilities(card_probs, player.played_cards)

    choice = np.random.choice(
        list(card_probs.keys()),
        13 - round,
        p=list(card_probs.values()),
        replace=False)
    card_choices = [NUM_TO_CARD[card] for card in choice]
    card_choices_obj = [Card(card[0], card[1]) for card in card_choices]
    return card_choices_obj
    return random.sample(cards, 13 - round)