from math import e

import networkx as nx
import numpy as np
import sympy as sym
import ttg
from matplotlib import pyplot as plt
from scipy.integrate import quad
from tqdm import tqdm

t = sym.symbols('t')


def expr(fail_rate=0.0, mttr=None):

    if mttr is None:
        return e ** (-fail_rate * t)
    else:
        # increment for numerical stability
        fail_rate = fail_rate + 1e-9
        mttr = mttr + 1e-9
        return (1 / fail_rate) / (mttr + 1 / fail_rate)


def horas_para_anos(horas):
    # Considerando que 1 ano tem 365.25 dias
    dias = horas / 24
    anos = dias / 365.25
    return anos


def plot_graph(G):
    pos = nx.spring_layout(G)

    nx.draw(G, pos)

    # Draw node labels
    node_labels = nx.get_node_attributes(G, "value")
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, "value")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()


def reduce_graph(G, start_node, end_node, repairable=False):
    # Start and end nodes makes to slice the graph
    G.add_node("end", value=(0.0, 0.0)) if repairable else G.add_node("end", value=0.0)
    G.add_edge("end", end_node)
    end_node = "end"

    return None, markov_chain(G, repairable)


# Calcula a integral inexplicavel
def itamar_thing(reliability):
    mttf, integration_error = quad(sym.lambdify(t, reliability, 'numpy'), 0, np.inf)

    return 1 / (mttf + 1e-9)


def markov_chain(G, repairable=False):
    # Get a list of nodes along with their data
    nodes_names = np.array(G.nodes(data=False))

    # Create a truth table with propositional expressions
    truth_table_generator = ttg.Truths(nodes_names.tolist(), ascending=True)

    fail_rate_list = [G.nodes[node_name]["value"] for node_name in nodes_names]

    # R(t) = Reliability function (algebraic) for each node.
    if repairable is False:
        r_array = np.array([expr(fail_rate) for fail_rate in fail_rate_list])
    else:
        r_array = np.array([expr(fail_rate, mttr) for (fail_rate, mttr) in fail_rate_list])

    # If 1, node is working. If 0, the respective node is in fail state.
    truth_table = truth_table_generator.as_pandas.values
    ones_matrix = np.ones_like(truth_table)
    complementary_truth_table = ones_matrix - truth_table  # Replace 1 by 0 and 0 by 1.

    # Prob of node working: R(t). Prob of node failing: 1 - R(t).
    reliability_truth_table = (truth_table * r_array) + (complementary_truth_table * (ones_matrix - r_array))

    # Compute the algebraic productory for each row.
    eq_reliability_table = np.prod(reliability_truth_table, axis=1)

    eq_reliability = 0
    for i, nodes_working in tqdm(enumerate(truth_table), total=truth_table.shape[0]):
        # Get graph composed by non-failed nodes only.
        non_failed_nodes = nodes_names[nodes_working == 1].tolist()
        subgraph = G.subgraph(non_failed_nodes)

        # If you have a path from start to end, the system still works
        if subgraph.has_node("start"):
            if subgraph.has_node("end"):
                if nx.has_path(subgraph, "start", "end"):
                    eq_reliability = eq_reliability + eq_reliability_table[i]

    if repairable is False:
        return itamar_thing(eq_reliability)
    else:
        return eq_reliability


if __name__ == '__main__':
    G = nx.Graph()
    G.add_node("start",
               value=0.0)  # The start node is a requirement of the script, every generator must derive from it.

    # Value is your Lambda. 1/m = Lambda (fails per time unit)
    G.add_node("gerador", value=0.1)
    G.add_node("barra1", value=0.1)
    G.add_node("disjuntor1", value=0.1)
    G.add_node("trafo1", value=0.3)
    G.add_node("disjuntor2", value=0.2)
    G.add_node("trafo2", value=0.1)
    G.add_node("barra2", value=0.5)

    G.add_edge("start", "gerador")
    G.add_edge("gerador", "barra1")
    G.add_edge("barra1", "disjuntor1")
    G.add_edge("barra1", "disjuntor2")
    G.add_edge("disjuntor1", "trafo1")
    G.add_edge("disjuntor2", "trafo2")
    G.add_edge("trafo1", "barra2")
    G.add_edge("trafo2", "barra2")

    # Replace with <YOUR-target-node> for reliability calcs
    target_node = "barra2"

    # Reduce the graph
    reduced_G, eq_lambda = reduce_graph(G, "start", target_node)

    print("\n\nO valor de Lambda equivalente do seu sistema é: ", eq_lambda)
