import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import quality
import numpy as np 
import scipy as sp
from girvan_newman import girvan_newman
from label_propagation import label_propagation
from markov_cluster import markov_cluster

def export_gml(G, communities, path):
    # get a copy of the original graph
    G_copy = G.copy()

    # build node group dictionary
    node_group = {}
    com_num = 0
    for community in communities:
        for v in community:
            node_group[v] = {'community': com_num}
        com_num += 1

    # set node group as G_copy's node attribute
    nx.set_node_attributes(G_copy, node_group)

    # export G_copy to .gml file
    nx.write_gml(G_copy, path)
    print("Already export gml file!")

G = nx.readwrite.gml.read_gml("weighted_graph.gml")

communities_gn = girvan_newman(G, 6)
communities_lp = label_propagation(G)
communities_mc = markov_cluster(G, power=2, inflation=2, numIter=5, decimals=2)

print("gn:", len(communities_gn), quality.modularity(G, communities_gn), quality.performance(G, communities_gn))
print("lp:", len(communities_lp), quality.modularity(G, communities_lp), quality.performance(G, communities_lp))
print("mc:", len(communities_mc), quality.modularity(G, communities_mc), quality.performance(G, communities_mc))

export_gml(G, communities_lp, "test_lp.gml")