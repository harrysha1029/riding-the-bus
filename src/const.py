from enum import Enum
from typing import Callable, List, Tuple

START_STATE = (0, 0)
END_STATE = (4, 0)


class Model(Enum):
    Finite = 1
    Infinite = 2


class RuleSet(Enum):
    Lenient = 1
    Harsh = 2


Card = Tuple[int, int]
Deck = List[Card]
Player = Callable[[int, List[Card], int, int, Deck, Model, RuleSet], int]
State = Tuple[int, int]