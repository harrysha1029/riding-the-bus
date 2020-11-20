from collections import defaultdict

from src.cards import *
from src.const import *


def check0(guess, history: List[Card], n_values: int, n_suits: int, rules: RuleSet):
    return color(history[0]) == guess


def check1(guess, history: List[Card], n_values: int, n_suits: int, rules: RuleSet):
    if guess == 0:
        return card_lower(history[0], history[1], rules)
    else:
        return card_higher(history[0], history[1], rules)


def check2(guess, history: List[Card], n_values: int, n_suits: int, rules: RuleSet):
    if guess == 0:
        return card_inside(history[0], history[1], history[2], rules)
    else:
        return card_outside(history[0], history[1], history[2], rules)


def check3(guess, history: List[Card], n_values: int, n_suits: int, rules: RuleSet):
    return suit(history[3]) == guess


def check_guess(
    question: int,
    guess: int,
    history: List[Card],
    n_values: int,
    n_suits: int,
    rules: RuleSet,
) -> bool:
    QUESTION_TO_CHECK_FN = {
        0: check0,
        1: check1,
        2: check2,
        3: check3,
    }
    return QUESTION_TO_CHECK_FN[question](guess, history, n_values, n_suits, rules)


def print_question(q, n_suits):
    if q == 0:
        print("Color of the card (0 or 1)?")
    elif q == 1:
        print("Lower (0) or Higher (1)?")
    elif q == 2:
        print("Inside (0) or Outside (1)?")
    elif q == 3:
        print(f"Suit (0-{n_suits -1})")


def is_valid_guess(question, guess, n_suits):
    if question in [0, 1, 2]:
        return guess in [0, 1]
    if question == 3:
        return 0 <= guess < n_suits
    return False


def get_guess(
    player: Player,
    question: int,
    history: List[Card],
    n_values,
    n_suits: int,
    deck: Deck,
    model: Model,
    rules: RuleSet,
):
    while True:
        try:
            guess = player(question, history, n_values, n_suits, deck, model, rules)
            if is_valid_guess(question, guess, n_suits):
                return guess
        except ValueError:
            pass


def rtb(
    player: Player,
    n_values: int,
    n_suits: int,
    model: Model,
    rules: RuleSet,
    show: bool = False,
):
    stats = defaultdict(int)  # type: ignore
    deck = get_deck(n_values, n_suits)
    question = 0
    history: List[Card] = []
    while True:
        stats[f"n_q{question}"] += 1
        stats[f"n_guesses"] += 1
        if show:
            print_question(question, n_suits)
        guess = get_guess(
            player, question, history, n_values, n_suits, deck, model, rules
        )
        if show:
            print(guess)
        card = draw(deck, model)
        history.append(card)
        if show:
            print(card)
        if check_guess(question, guess, history, n_values, n_suits, rules):
            stats[f"n_correct_q{question}"] += 1
            question += 1
            if question == 4:
                if show:
                    print("Congrats!")
                return stats
        else:
            stats[f"n_incorrect_q{question}"] += 1
            stats[f"n_drinks"] += 1
            if show:
                print("Drink!\n")
            history = []
            question = 0
        if len(deck) == 0:
            deck = get_deck(n_values, n_suits)
