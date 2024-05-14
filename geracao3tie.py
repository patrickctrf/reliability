from reduction import *

G = nx.Graph()

# The start node is a requirement of the script, every power source must derive from it.
G.add_node("start", value=(0.0, 0.0))

# Value is your (Lambda and MTTR).
# 1/m = Lambda (fails per year). MTTR = mean time to repair (hours)
G.add_node("gerador1", value=(0.1691, horas_para_anos(478)))
G.add_node("gerador2", value=(0.1691, horas_para_anos(478)))
G.add_node("gerador3", value=(0.1691, horas_para_anos(478)))
G.add_node("gerador4", value=(0.1691, horas_para_anos(478)))
G.add_node("barra11", value=(0.000125, horas_para_anos(128)))
G.add_node("barra12", value=(0.000125, horas_para_anos(128)))
G.add_node("barra13", value=(0.000125, horas_para_anos(128)))
G.add_node("barra14", value=(0.000125, horas_para_anos(128)))
G.add_node("tie11", value=(0.0096, horas_para_anos(9.6)))
G.add_node("tie12", value=(0.0096, horas_para_anos(9.6)))
G.add_node("tie13", value=(0.0096, horas_para_anos(9.6)))

# alimentacao superior
G.add_edge("start", "gerador1")
G.add_edge("start", "gerador2")
G.add_edge("start", "gerador3")
G.add_edge("start", "gerador4")
G.add_edge("gerador1", "barra11")
G.add_edge("gerador2", "barra12")
G.add_edge("gerador3", "barra13")
G.add_edge("gerador4", "barra14")
G.add_edge("barra11", "tie11")
G.add_edge("barra12", "tie12")
G.add_edge("barra13", "tie13")
G.add_edge("barra12", "tie11")
G.add_edge("barra13", "tie12")
G.add_edge("barra14", "tie13")

# Replace with <YOUR-target-node> for reliability calcs
target_node = "barra14"

# System repairable?
repairable = True

# Reduce the graph
if repairable is True:
    reduced_G, eq_reliability = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de confiabilidade equivalente do seu sistema é: ", eq_reliability)
else:
    reduced_G, eq_lambda = reduce_graph(G, "start", target_node, repairable)
    print("\n\nO valor de Lambda equivalente do seu sistema é: ", eq_lambda)
