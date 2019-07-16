import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import quality
import numpy as np 
import scipy as sp
from girvan_newman import girvan_newman
from label_propagation import label_propagation
from markov_cluster import markov_cluster

G = nx.readwrite.gml.read_gml("weighted_graph.gml")

communities_gn = girvan_newman(G, 6)
communities_lp = label_propagation(G)
communities_mc = markov_cluster(G, power=2, inflation=2, numIter=5, decimals=2)

print("gn:", len(communities_gn), quality.modularity(G, communities_gn), quality.performance(G, communities_gn))
print("lp:", len(communities_lp), quality.modularity(G, communities_lp), quality.performance(G, communities_lp))
print("mc:", len(communities_mc), quality.modularity(G, communities_mc), quality.performance(G, communities_mc))
