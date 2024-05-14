from reduction import *

G = nx.Graph()

# The start node is a requirement of the script, every power source must derive from it.
G.add_node("start", value=(0.0, 0.0))

# Value is your (Lambda and MTTR).
# 1/m = Lambda (fails per year). MTTR = mean time to repair (hours)

G.add_node("barra11", value=(0.000125, horas_para_anos(128)))
G.add_node("cabo11", value=(0.0141, horas_para_anos(40.4)))
G.add_node("cabo12", value=(0.0141, horas_para_anos(40.4)))
G.add_node("cabo21", value=(0.0141, horas_para_anos(40.4)))
G.add_node("cabo22", value=(0.0141, horas_para_anos(40.4)))
G.add_node("cabo31", value=(0.0141, horas_para_anos(40.4)))
G.add_node("cabo32", value=(0.0141, horas_para_anos(40.4)))
G.add_node("disjuntor11", value=(0.0096, horas_para_anos(9.6)))
G.add_node("disjuntor12", value=(0.0096, horas_para_anos(9.6)))
G.add_node("trafo21", value=(0.0059, horas_para_anos(297.4)))
G.add_node("trafo22", value=(0.0059, horas_para_anos(297.4)))
G.add_node("tie21", value=(0.0096, horas_para_anos(9.6)))
G.add_node("barra21", value=(0.000125, horas_para_anos(128)))
G.add_node("barra22", value=(0.000125, horas_para_anos(128)))

# Ramo esquerdo
G.add_edge("start", "barra11")
G.add_edge("barra11", "cabo11")
G.add_edge("barra11", "cabo12")
G.add_edge("cabo11", "disjuntor11")
G.add_edge("cabo12", "disjuntor12")
G.add_edge("disjuntor11", "cabo21")
G.add_edge("disjuntor12", "cabo22")
G.add_edge("cabo21", "trafo21")
G.add_edge("cabo22", "trafo22")
G.add_edge("trafo21", "cabo31")
G.add_edge("trafo22", "cabo32")
G.add_edge("cabo31", "barra21")
G.add_edge("cabo32", "barra22")
G.add_edge("tie21", "barra21")
G.add_edge("tie21", "barra22")

# Replace with <YOUR-target-node> for reliability calcs
target_node = "barra21"

# System repairable?
repairable = True

# Reduce the graph
if repairable is True:
    reduced_G, eq_reliability = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de confiabilidade equivalente do seu sistema é: ", eq_reliability)
else:
    reduced_G, eq_lambda = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de Lambda equivalente do seu sistema é: ", eq_lambda)
