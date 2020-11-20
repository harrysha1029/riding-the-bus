import itertools
import random
from enum import Enum
from typing import List, Tuple

import src.utils as utils
from src.const import *


def suit(card: Card) -> int:
    return card[1]


def value(card: Card) -> int:
    return card[0]


def color(card: Card):
    return suit(card) % 2


def get_deck(n_values: int, n_suits: int) -> Deck:
    d = list(itertools.product(range(n_values), range(n_suits)))
    random.shuffle(d)
    return d


def card_inside(c1: Card, c2: Card, t: Card, rules:RuleSet) -> bool:
    return inside(value(c1), value(c2), value(t), rules)


def card_outside(c1: Card, c2: Card, t: Card, rules:RuleSet) -> bool:
    return outside(value(c1), value(c2), value(t), rules)


def card_higher(c1: Card, t: Card, rules:RuleSet) -> bool:
    return higher(value(c1), value(t), rules)


def card_lower(c1: Card, t: Card, rules:RuleSet) -> bool:
    return lower(value(c1), value(t), rules)




def draw(d: Deck, model: Model) -> Card:
    if model == Model.Infinite:
        return random.choice(d)
    else:
        return d.pop()


def inside(x1: int, x2: int, y: int, rules: RuleSet) -> bool:
    if rules == RuleSet.Lenient:
        return min(x1, x2) <= y <= max(x1, x2)
    else:
        return min(x1, x2) < y < max(x1, x2)


def outside(x1:int, x2:int, y:int, rules:RuleSet) -> bool:
    if rules == RuleSet.Lenient:
        return min(x1, x2) >= y or y >= max(x1, x2)
    else:
        return min(x1, x2) > y or y > max(x1, x2)


def lower(v1:int, v2:int, rules:RuleSet) -> bool:
    if rules == RuleSet.Lenient:
        return v2 <= v1
    else:
        return v2 < v1


def higher(v1:int, v2:int, rules:RuleSet) -> bool:
    if rules == RuleSet.Lenient:
        return v2 >= v1
    else:
        return v2 > v1

def num_values_higher(v, n_values:int, rules:RuleSet):
    return sum(higher(v, v2, rules) for v2 in range(n_values))
def num_values_lower(v, n_values:int, rules:RuleSet):
    return sum(lower(v, v2, rules) for v2 in range(n_values))
def num_values_inside(v, v2, n_values:int, rules:RuleSet):
    return sum(inside(v, v2, v3, rules) for v3 in range(n_values))
def num_values_outside(v, v2, n_values:int, rules:RuleSet):
    return sum(outside(v, v2, v3, rules) for v3 in range(n_values))