import random
from collections import Counter

from src.cards import *
from src.const import *


def human(
    question: int,
    history: List[Card],
    n_values: int,
    n_suits: int,
    deck: Deck,
    model: Model,
    rules: RuleSet,
):
    return int(input("Guess: "))


def drunk_player(
    question: int,
    history: List[Card],
    n_values: int,
    n_suits: int,
    deck: Deck,
    model: Model,
    rules: RuleSet,
):
    if question < 3:
        return random.choice([0, 1])
    else:
        return random.choice(range(n_suits))


def count_lower(card: Card, deck: Deck, rules: RuleSet):
    return sum(card_lower(card, i, rules) for i in deck)


def count_higher(card: Card, deck: Deck, rules: RuleSet):
    return sum(card_higher(card, i, rules) for i in deck)


def count_inside(card1: Card, card2: Card, deck: Deck, rules: RuleSet):
    return sum(card_inside(card1, card2, i, rules) for i in deck)


def count_outside(card1: Card, card2: Card, deck: Deck, rules: RuleSet):
    return sum(card_outside(card1, card2, i, rules) for i in deck)

def count_red(deck):
    return sum(color(card) == 0 for card in deck)

def count_black(deck):
    return sum(color(card) == 1 for card in deck)

def count_suits(deck):
    return Counter([suit(card) for card in deck])


def greedy_player(
    question: int,
    history: List[Card],
    n_values: int,
    n_suits: int,
    deck: Deck,
    model: Model,
    rules: RuleSet,
):
    if question == 0:
        return random.choice([0, 1])
    elif question == 1:
        k = value(history[0])
        return 0 if (k + 1 > n_values - k) else 1
    elif question == 2:
        k = abs(value(history[0]) - value(history[1]))
        return 0 if k + 1 > n_values - k + 1 else 1
    else:
        return random.choice(range(n_suits))

def hyperthymestic_player(
    question: int,
    history: List[Card],
    n_values: int,
    n_suits: int,
    deck: Deck,
    model: Model,
    rules: RuleSet,
):
    if question == 0:
        return 0 if count_red(deck) >= count_black(deck) else 1
    elif question == 1:
        k = history[0]
        return 0 if count_lower(k, deck, rules) >= count_higher(k, deck, rules) else 1
    elif question == 2:
        k1 = history[0]
        k2 = history[1]
        return 0 if count_inside(k1, k2, deck, rules) >= count_outside(k1, k2, deck, rules) else 1
    else:
        return count_suits(deck).most_common(1)[0][0]
