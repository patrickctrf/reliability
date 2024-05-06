import networkx as nx
from matplotlib import pyplot as plt


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
    new_node = 1 / (1 / G.nodes[node1]["value"] + 1 / G.nodes[node2]["value"] - 1 / (G.nodes[node1]["value"] + G.nodes[node2]["value"]))

    G.add_node("(" + node1 + "||" + node2 + ")", value=new_node)
    # Connect the new node to the neighbors of the old nodes
    for neighbor in set(G.neighbors(node1)).union(G.neighbors(node2)):
        if neighbor not in [node1, node2]:
            G.add_edge("(" + node1 + "||" + node2 + ")", neighbor)
    G.remove_node(node1)
    G.remove_node(node2)
    return new_node


def reduce_graph(G, start_node, end_node):
    # Start and end nodes makes to slice the graph
    G.add_node("end", value=0.0)
    G.add_edge("end", end_node)
    end_node = "end"

    # plot_graph(G)

    # slice only the paths that matters for us
    all_paths_list = list(nx.all_simple_paths(G, source=start_node, target=end_node))
    minimum_nodes = list(set([x for sublist in all_paths_list for x in sublist]))
    G = nx.Graph(G.subgraph(minimum_nodes))
    # plot_graph(G)

    reduced = False
    while not reduced:
        reduced = True
        # Look for series nodes and join them
        for node1, node2 in list(G.edges()):
            if are_in_series(G, node1, node2):
                join_series(G, node1, node2)
                reduced = False
                break
        # Looks for parallel nodes and join them
        parallel_nodes = find_parallel_nodes(G)
        if len(parallel_nodes) > 0:
            reduced = False
            (node1, node2) = parallel_nodes[0]
            join_parallel(G, node1, node2)

        # plot_graph(G)

    G.remove_node("start")
    G.remove_node("end")

    # Aggregating the helper nodes to convert the graph into a float64 die.
    node_values = [data["value"] for node, data in G.nodes(data=True)]
    aggregate = 0
    for node, data in G.nodes(data=True):
        aggregate += data["value"]

    return G, aggregate / len(node_values)


