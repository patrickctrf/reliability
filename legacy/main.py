from reduction import *

G = nx.Graph()
G.add_node("start", value=0.0)  # The start node is a requirement of the script, every generator must derive from it.

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
