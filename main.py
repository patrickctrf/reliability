from reduction import *

G = nx.Graph()

# The start node is a requirement of the script, every power source must derive from it.
G.add_node("start", value=(0.0, 0.0))

# Value is your (Lambda and MTTR).
# 1/m = Lambda (fails per year). MTTR = mean time to repair (hours)
G.add_node("gerador", value=(0.1, horas_para_anos(300)))
G.add_node("barra1", value=(0.01, horas_para_anos(300)))
G.add_node("disjuntor1", value=(0.1, horas_para_anos(300)))
G.add_node("trafo1", value=(0.3, horas_para_anos(300)))
G.add_node("disjuntor2", value=(0.2, horas_para_anos(300)))
G.add_node("trafo2", value=(0.1, horas_para_anos(300)))
G.add_node("barra2", value=(0.05, horas_para_anos(300)))

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

# System repairable?
repairable = True

# Reduce the graph
if repairable is True:
    reduced_G, eq_reliability = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de confiabilidade equivalente do seu sistema é: ", eq_reliability)
else:
    reduced_G, eq_lambda = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de Lambda equivalente do seu sistema é: ", eq_lambda)
