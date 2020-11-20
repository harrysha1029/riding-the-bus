import colorsys
import itertools
from typing import List, Optional, Tuple

import dot2tex
import imageio
import networkx as nx
import numpy as np
from tqdm import tqdm

from src.const import *



def R1(rules: RuleSet, n: int, k: int):
    if rules == RuleSet.Lenient:
        return max(k + 1, n - k)
    else:
        return max(k, n - k - 1)


def R2(rules: RuleSet, n: int, k: int):
    if rules == RuleSet.Lenient:
        return max(k + 1, min(n - k + 1, n))
    else:
        return max(k - 1, n - k - 1)


def T(
    rules: RuleSet, n_values: int, n_suits: int, start_state: State, next_state: State
) -> float:
    q, k = start_state
    next_q, next_k = next_state
    if q == 0:
        if next_q == 0:
            return 1 / 2
        elif next_q == 1 and next_k < n_values:
            return 1 / 2 * 1 / n_values
    elif q == 1:
        if next_q == 0:
            return (n_values - R1(rules, n_values, k)) / n_values
        elif next_q == 2:
            if rules == RuleSet.Lenient:
                return 1 / n_values if next_k < R1(rules, n_values, k) else 0
            elif rules == RuleSet.Harsh:
                return 1 / n_values if 0 < next_k <= R1(rules, n_values, k) else 0
    elif q == 2:
        if next_q == 0:
            return (n_values - R2(rules, n_values, k)) / n_values
        if next_q == 3:
            return R2(rules, n_values, k) / n_values
    elif q == 3:
        if next_q == 0:
            return 1 - 1 / n_suits
        if next_q == 4:
            return 1 / n_suits
    elif q == 4:
        if next_q == 4:
            return 1
        else:
            return 0
    return 0


def get_states(n_values: int):
    return (
        [(0, 0)]
        + [(1, i) for i in range(n_values)]
        + [(2, i) for i in range(n_values)]
        + [(3, 0)]
        + [(4, 0)]
    )


def state_to_string(s: State) -> str:
    string = "s" + "_{" + str(s[0])
    if s[0] in [1, 2]:
        string += ", " + str(s[1])
    string += "}"
    return string


def states_to_strings(s: List[State]) -> List[str]:
    return [state_to_string(x) for x in s]


def get_state_strings(n_values: int):
    return states_to_strings(get_states(n_values))


def get_transition_matrix(rules: RuleSet, n_values: int, n_suits: int):
    states = get_states(n_values)
    matrix = np.zeros((len(states), len(states)))

    for i, s1 in enumerate(states):
        for j, s2 in enumerate(states):
            matrix[i, j] = T(rules, n_values, n_suits, s1, s2)
    assert np.allclose(np.sum(matrix, axis=1), 1)
    return matrix


def D(rules: RuleSet, n_values: int, n_suits: int, t: int, state: State):
    # Use numeric states here..
    transition_matrix = get_transition_matrix(rules, n_values, n_suits)
    states = get_states(n_values)
    start_state = np.array([int(s == state) for s in states])
    return np.dot(start_state, np.linalg.matrix_power(transition_matrix, t))


def get_graph(rules: RuleSet, n_values: int, n_suits: int):
    transition_matrix = get_transition_matrix(rules, n_values, n_suits)
    states_string = get_state_strings(n_values)
    g = nx.DiGraph()
    for i, x in enumerate(states_string):
        for j, y in enumerate(states_string):
            if transition_matrix[i, j] > 0 and y != r"s_{0}":
                g.add_edge(x, y)  # , label=transition_matrix[i, j])
    return g


def get_shaded_blue(v):
    rgb = colorsys.hls_to_rgb(1, v, 1)
    v = "".join([hex(int((1 - x) * 255))[2:].ljust(2, "0") for x in rgb])
    return f"#{v}"


def color_graph(g: nx.Graph, dist: List[float], states: List[str]):
    for v, s in zip(dist, states):
        g.nodes[s]["fillcolor"] = get_shaded_blue(v)
        g.nodes[s]["style"] = "filled"
    return g


def get_colored_graph_at_time_t(rules: RuleSet, n_values: int, n_suits: int, t: int):
    matrix = get_transition_matrix(rules, n_values, n_suits)
    graph = get_graph(rules, n_values, n_suits)
    graph.graph["label"] = f"t={t}"
    states = get_state_strings(n_values)
    dist = D(rules, n_values, n_suits, t, START_STATE)
    return color_graph(graph, dist, states)


def index_dist_array(arr: List[float], n_values, state):
    states = get_states(n_values)
    return arr[states.index(state)]


def graph_to_tikz(g):
    agraph = nx.drawing.nx_agraph.to_agraph(g)
    return dot2tex.dot2tex(
                agraph.to_string(),
                figonly=True,
                texmode="math",
                crop=True,
                autosize=True,
            )


def draw_graph(graph: nx.Graph, fname: str = "diagram.svg", print_tikz: bool = False):
    """Draws a graph and saves it to fname

    Args:
        graph (nx.Graph): graph to draw
        fname (str, optional): name of the file to save to.
                                Defaults to "test.svg".
    """
    agraph = nx.drawing.nx_agraph.to_agraph(graph)
    agraph.layout("dot")
    agraph.draw(fname)


def P(rules: RuleSet, n_values, n_suits, t, start_state, target_state):
    dist = D(rules, n_values, n_suits, t, start_state)
    return index_dist_array(dist, n_values, target_state)


def make_tikz_diagram(g, fname):
    tikz = graph_to_tikz(g)
    with open(fname, 'w') as f:
        f.write(tikz)



def make_animation_full(n_values, n_suits, max_T, step, anim_fname, save_tex=False):
    images = []
    for i in range(0, max_T, step):
        g = get_colored_graph_at_time_t(RuleSet.Lenient, n_values, n_suits, i)
        fname = "figs/transitions/{i}.png"
        draw_graph(g, fname=fname)
        images.append(imageio.imread(fname))
        if save_tex:
            make_tikz_diagram(g, f'tex/tikz/full{i}.tex')
    imageio.mimsave(anim_fname, images, duration=0.5)


def index_to_state(index, n_values):
    states = get_states(n_values)
    return states[index]

def state_to_index(state, n_values):
    states = get_states(n_values)
    return states.index(state)

def index_to_question_number(index, n_values):
    return index_to_state(index, n_values)[0]

def dist_by_question(rules, n_values, n_suits, t, start_state):
    dist = D(rules, n_values, n_suits, t, start_state)
    return [
        dist[0],
        sum(dist[1:1+n_values]),
        sum(dist[1+n_values:1+n_values+n_values]),
        dist[-2],
        dist[-1]
    ]

def color_graph_condensed(g: nx.Graph, dist: List[float]):
    for i, v in enumerate(dist):
        g.nodes["q_{" + str(i)+ "}"]['style'] = 'filled'
        g.nodes["q_{" + str(i)+ "}"]['fillcolor'] = get_shaded_blue(v)
    return g

def get_graph_condensed():
    g = nx.DiGraph()
    states = ["q_{" + str(i)+ "}" for i in range(5)]
    g.add_edges_from(zip(states, states[1:]))
    return g

def make_animation_condensed(n_values:int, n_suits:int, max_T, step, anim_fname, save_tex=False):
    images = []
    for i in range(0, max_T, step):
        fname = "figs/transitions/{i}.png"
        dist = dist_by_question(RuleSet.Lenient, n_values,n_suits, i, START_STATE)
        g = color_graph_condensed(get_graph_condensed(), dist)
        g.graph['label'] = f't={i}'
        draw_graph(g, fname=fname)
        images.append(imageio.imread(fname))
        if save_tex:
            make_tikz_diagram(g, f'tex/tikz/{i}.tex')
    imageio.mimsave(anim_fname, images, duration=0.5)

