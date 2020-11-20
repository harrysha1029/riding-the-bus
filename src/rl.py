from src.const import *
import pandas as pd
import numpy as np
import src.markov as markov
from src.cards import *

# TODO generalize this to other values of n_values, n_suits.

def get_states(n_values:int):
    return markov.get_states(n_values) + [(5,0)]

def T(
    rules: RuleSet, n_values: int, n_suits: int, start_state: State, next_state: State, a:int
) -> float:
    if next_state == (0,0):
        return 0
    question, k1 = start_state
    next_question, k2 = next_state
    if question == 0 and a < 2: 
        if next_question == 1:
            return 1/n_values 
        if next_question == 5:
            return 1/2
    if question == 1 and a < 2:
        num_higher = num_values_lower(k1, n_values, rules)
        num_lower = num_values_higher(k1, n_values, rules)
        if next_question == 2:
            if a == 0:
                if rules == RuleSet.Lenient:
                    return 1 / n_values if k2 < num_lower else 0
                elif rules == RuleSet.Harsh:
                    return 1 / n_values if 0 < k2 <= num_lower else 0
            if a == 1:
                if rules == RuleSet.Lenient:
                    return 1 / n_values if k2 < num_higher else 0
                elif rules == RuleSet.Harsh:
                    return 1 / n_values if 0 < k2 <= num_higher else 0
        if next_question == 5:
            if a == 0:
                return 1-num_lower/n_values
            if a == 1:
                return 1-num_higher/n_values
    if question == 2 and a < 2:
        num_in = num_values_inside(0, k1, n_values, rules)
        num_out = num_values_outside(0, k1, n_values, rules)
        if next_question == 3:
            if a == 0:
                return num_in / n_values
            if a == 1:
                return num_out / n_values
        if next_question == 5:
            if a == 0:
                return 1 - num_in / n_values
            if a == 1:
                return 1 - num_out / n_values

    if question == 3:
        if next_question == 4:
            return 1/n_suits
        if next_question == 5:
            return 1-1/n_suits

    if question == 4 and next_question == 5:
        return 1

    return 0


ACTIONS = list(range(4))

def reward(s):
    return 1 if s == (4, 0) else 0

def state_action_value(rules, n_values, n_suits, s, a, v):
    states = get_states(n_values)
    ts = [T(rules, n_values, n_suits, s, s2, a) for s2 in states]
    rs = [reward(s2) + v[i] for i, s2 in enumerate(states)]
    return sum([t*r for t, r in zip(ts, rs)])

def value_iteration(rules, n_values, n_suits):
    states = get_states(n_values)
    values = [0 for _ in states]
    for _ in range(1000):
        new_values = values.copy()
        for i, s in enumerate(states):
            estimates = [
                state_action_value(rules, n_values, n_suits, s, a, values) for a in ACTIONS
            ]
            new_values[i] = max(estimates)

        if sum(np.array(new_values)-np.array(values)) < 0.000001:
            return new_values
        values = new_values


def get_optimal_policy_from_value_function(rules, n_values, n_suits, v):
    states = get_states(n_values)
    policy = []
    for s in states:
        scores = [
            state_action_value(rules, n_values, n_suits, s, a, v) for a in ACTIONS
        ]
        policy.append(np.argmax(scores))
    return policy

def print_value_function(values, n_values):
    states = get_states(n_values)
    for x, v in zip(states, values):
        print(markov.state_to_string(x), v)

def print_policy(policy, n_values):
    for s, p in zip(get_states(n_values), policy):
        print(markov.state_to_string(s), p)

QUESTION_TO_P_TO_STR = {
    0: {0:'0', 1:"1"}
    , 1: {0:'lower', 1:"higher"}
    , 2: {0:'inside', 1:"outside"}
    , 3: {0:'0', 1:"1", 2:"1", 3:"3"}
    , 4: {0:'0', 1:"1", 2:"1", 3:"3"}
    , 5: {0:'0', 1:"1", 2:"1", 3:"3"}
}

def run_rl(n_values, n_suits):
    values = value_iteration(RuleSet.Lenient, n_values, n_suits)
    policy = get_optimal_policy_from_value_function(RuleSet.Lenient, n_values, n_suits, values)
    states = get_states(n_values)
    rows = []
    for s, v, p in zip(states, values, policy):
        s_string = markov.state_to_string(s)
        p_string = QUESTION_TO_P_TO_STR[s[0]][p]
        rows.append([s_string, v, p_string])
    return pd.DataFrame(rows, columns=['State', 'Value', 'Guess'])
