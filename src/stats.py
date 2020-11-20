import pandas as pd
from tqdm import tqdm
import plotly.express as px

from src.const import *
from src.rtb import rtb
from src.markov import *
from src.players import *

def get_stats():
    NM_COMBINATIONS = [
        (13, 4)
        , (13, 10)
        , (13, 20)
        , (20, 4)
        , (40, 4)
    ]
    dfs = []
    for player, rules, (n, m) in itertools.product([drunk_player, hyperthymestic_player, greedy_player], [RuleSet.Lenient, RuleSet.Harsh], NM_COMBINATIONS):
        df = collect_stats(player, n, m, Model.Finite, rules, 10000).assign(player=player.__name__, n_values=n, n_suits=m, rules=str(rules))
        dfs.append(df)
    return pd.concat(dfs)

def get_nd_table():
    NM_COMBINATIONS = [
        (13, 4)
        , (13, 10)
        , (13, 20)
        , (20, 4)
        , (50, 4)
    ]
    rows = []
    for rules, (n, m) in itertools.product([RuleSet.Lenient, RuleSet.Harsh], NM_COMBINATIONS):
        p = P(rules, n, m, 4, START_STATE, END_STATE)
        rows.append([str(rules),n, m, 1/p-1, p])
    return pd.DataFrame(rows, columns=['Variant', "n", "m", 'E[Nd]', 'Probability of winning on first try'])


def collect_stats(
    player: Player,
    n_values: int,
    n_suits: int,
    model: Model,
    rules: RuleSet,
    n_samples: int,
):
    results = [
        rtb(player, n_values, n_suits, model, rules, False)
        for _ in tqdm(range(n_samples))
    ]
    return pd.DataFrame(results).fillna(0)


def report_success_prob_by_question(df: pd.DataFrame, p=False):
    if p:
        print("Mean number of drinks", df.n_drinks.mean())
        print("Implied success prob", 1 / (df.n_drinks.mean() + 1))
        print("Success on Q0: ", df.n_correct_q0.sum() / df.n_q0.sum())
        print("Success on Q1: ", df.n_correct_q1.sum() / df.n_q1.sum())
        print("Success on Q2: ", df.n_correct_q2.sum() / df.n_q2.sum())
        print("Success on Q3: ", df.n_correct_q3.sum() / df.n_q3.sum())
    return df.n_correct_q0.sum() / df.n_q0.sum(), df.n_correct_q1.sum() / df.n_q1.sum(), df.n_correct_q2.sum() / df.n_q2.sum(), df.n_correct_q3.sum() / df.n_q3.sum()


def plot_distribution_by_question(n_values, n_suits):
    l = [dist_by_question(RuleSet.Lenient, n_values, n_suits, i, START_STATE) for i in range(0,50)]
    df = pd.DataFrame(l, columns=[f'question{i}'for i in range(4)] + ['final'])
    fig = px.line(df, template='plotly_white')
    fig.update_layout(
        xaxis_title="Timestep",
        yaxis_title="Probability",
        legend_title="State",
    )
    fig.write_image("tex/imgs/dist_questions.png")