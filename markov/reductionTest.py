import math
from math import e

import networkx as nx
import numpy as np
import sympy as sym
import ttg
from matplotlib import pyplot as plt
from scipy.integrate import quad
from tqdm import tqdm

t = sym.symbols('t')


def expr(fail_rate=0.0):
    return e ** (-fail_rate * t)


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


# Function to check if two nodes are in series
def are_in_series(G, node1, node2):
    # Nodes are in series if each has degree 2 and they are connected to each other
    return G.degree(node1) == 2 and G.degree(node2) == 2 and G.has_edge(node1, node2)


# Create a function to find nodes with exactly two common neighbors and no other neighbors
def find_parallel_nodes(G):
    # Initialize an empty list to store nodes with exactly two common neighbors
    nodes_with_two_common_neighbors = []

    # Iterate over all nodes in the graph
    for node in G.nodes():
        # Get neighbors of the current node
        neighbors = set(G.neighbors(node))

        # Check if the current node has exactly two neighbors
        if len(neighbors) == 2:
            # Iterate over all other nodes in the graph
            for other_node in G.nodes():
                # Skip if it's the same node
                if other_node == node:
                    continue

                # Get neighbors of the other node
                other_neighbors = set(G.neighbors(other_node))

                # Check if the other node also has exactly two neighbors
                if len(other_neighbors) == 2:
                    # Check if the two nodes share the same neighbors
                    if neighbors == other_neighbors:
                        # Add the pair of nodes to the list
                        nodes_with_two_common_neighbors.append((node, other_node))

    # Return the list of nodes with exactly two common neighbors
    return nodes_with_two_common_neighbors


# Function to join nodes in series
def join_series(G, node1, node2):
    new_node = G.nodes[node1]["value"] + G.nodes[node2]["value"]
    G.add_node("(" + node1 + "+" + node2 + ")", value=new_node)
    # Connect the new node to the neighbors of the old nodes
    for neighbor in set(G.neighbors(node1)).union(G.neighbors(node2)):
        if neighbor not in [node1, node2]:
            G.add_edge("(" + node1 + "+" + node2 + ")", neighbor)
    G.remove_node(node1)
    G.remove_node(node2)
    return new_node


# Function to join nodes in parallel
def join_parallel(G, node1, node2):
    new_node = 1 / (1 / G.nodes[node1]["value"] + 1 / G.nodes[node2]["value"] - 1 / (
            G.nodes[node1]["value"] + G.nodes[node2]["value"]))

    G.add_node("(" + node1 + "||" + node2 + ")", value=new_node)
    # Connect the new node to the neighbors of the old nodes
    for neighbor in set(G.neighbors(node1)).union(G.neighbors(node2)):
        if neighbor not in [node1, node2]:
            G.add_edge("(" + node1 + "||" + node2 + ")", neighbor)
    G.remove_node(node1)
    G.remove_node(node2)
    return new_node


def reduce_graph(G, start_node, end_node):
    return None, markov_chain(G)


# Calcula a integral inexplicavel
def itamar_thing(reliability):
    mttf, integration_error = quad(sym.lambdify(t, reliability, 'numpy'), 0, np.inf)
    # sym.integrate(reliability, (t, 0, sym.oo))

    lambda_eq = 1 / (mttf + 1e-9)
    return lambda_eq


def markov_chain(G):
    # Get a list of nodes along with their data
    nodes_names = np.array(G.nodes(data=False))

    # Create a truth table with propositional expressions
    truth_table_generator = ttg.Truths(nodes_names.tolist(), ascending=True)

    fail_rate_list = [G.nodes[node_name]["value"] for node_name in nodes_names]

    # R(t) = Reliability function (algebraic) for each node.
    r_array = np.array([expr(fail_rate) for fail_rate in fail_rate_list])

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
                    y = eq_reliability_table[i]
                    eq_reliability = eq_reliability + eq_reliability_table[i]
                    x = 1

    return itamar_thing(eq_reliability)

    # eq_reliability = 0
    # for i, nodes_working in tqdm(enumerate(truth_table), total=truth_table.shape[0]):
    #     eq_reliability = eq_reliability + eq_reliability_table[i]
    #
    # return eq_reliability.subs(t, 1).evalf()


if __name__ == '__main__':
    G = nx.Graph()
    G.add_node("start",
               value=1.0000)  # The start node is a requirement of the script, every generator must derive from it.

    G.add_node("end",
               value=0.0000)

    # Value is your Lambda. 1/m = Lambda (fails per time unit)
    G.add_node("trafo1", value=0.4)
    G.add_node("trafo2", value=0.3)

    G.add_edge("start", "trafo1")
    G.add_edge("start", "trafo2")
    G.add_edge("trafo1", "end")
    G.add_edge("trafo2", "end")

    # Replace with <YOUR-target-node> for reliability calcs
    target_node = "end"

    # Reduce the graph
    reduced_G, eq_lambda = reduce_graph(G, "start", target_node)

    print("\n\nO valor de Lambda equivalente do seu sistema é: ", eq_lambda)
