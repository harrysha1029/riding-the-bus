import itertools

import pandas as pd
import plotly.express as px
import numpy as np
from tqdm import tqdm

from src.cards import *
from src.const import *
from src.players import *
from src.rtb import *
from src.stats import *
from src.markov import *
import src.rl as rl

import colorsys
import imageio


N = 13
M = 4

# ======= Run Simulations =======a
# get_stats().to_csv("data/big.csv")

# ======= get nd table =============
# get_nd_table().to_csv("data/nd_table.csv")


# no_memory = collect_stats(greedy_player, N, M, Model.Finite, RuleSet.Harsh, 10000)
# memory = collect_stats(hyperthymestic_player, N, M, Model.Finite, RuleSet.Harsh, 10000)
# report_success_prob_by_question(no_memory)
# report_success_prob_by_question(memory)

# ======= Run RL ======
# rl.run_rl(N, M).to_csv("data/rl.csv", index=False)


# =========== Compute w/ uniform prior =====
# pairs = itertools.product(range(13), repeat=2)
# p = [T(RuleSet.Harsh, N, M, (2, abs(i-j)), (3,0)) for i , j in pairs]
# print(sum(p) / 13**2)

# ts = [T(RuleSet.Harsh, N, M, (2, k), (3, 0)) for k in range(13)]
# ps = [P(RuleSet.Harsh, N, M, 2, START_STATE, (2, k)) for t, k in zip(ts, range(0, 13))]
# print(sum(t*p/sum(ps) for t, p in zip(ts, ps)))
# print(ps)

# print(sum(ps))

# =========== Simulate inifinite deck n_guesses ======

def simulate_infinite_n_guesses(n_values, n_suits):
    stats = collect_stats(greedy_player, n_values, n_suits, Model.Infinite, RuleSet.Lenient, 100000)
    report_success_prob_by_question(stats)
    stats.to_csv("data/guesses_stats.csv", index=False)
simulate_infinite_n_guesses(N, M)

# ========= Make animations ===========
# make_animation_condensed(4, 4, 40, 1, 'animation_condensed.gif', save_tex=True)
# make_animation_full(4, 4, 40, 1, 'animation.gif', save_tex=True)


#======= Make diagram ======
# g = get_graph(RuleSet.Lenient, n_values, 4)
# make_tikz_diagram(g)


#======= Run with greedy_player ======
# rtb(greedy_player, N, M, Model.Infinite, RuleSet.Harsh, True)


#======= Collect and report statistics ======
# df = collect_stats(greedy_player, N, M, Model.Infinite, RuleSet.Harsh, 100000)
# report_success_prob_by_question(df)


#======= Report theoretical v.s Markov Chain values after 4 steps =======

# def terms(n, k):
#     return min(n, 2*(n-k))*max(k+1, min(n-k+1, n))

# def terms_harsh(n, k):
#     return min(n, 2*(n-k))*max(k-1, n-k-1)

# x = sum(terms_harsh(N, k) for k in range(1,N))/(2*M*N**3)
# print(x)

# transition_matrix = get_transition_matrix(RuleSet.Harsh, N, M)

#======== Testing T, R ================
# print(T(RuleSet.Lenient, 5, 4, (1, 1), (2, 4)))
# print(R(RuleSet.Lenient, 5, (1, 1)))