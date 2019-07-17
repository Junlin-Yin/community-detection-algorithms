import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import quality
import numpy as np 
import scipy as sp
from readwrite import import_tsv, export_gml
from girvan_newman import girvan_newman
from label_propagation import label_propagation
from markov_cluster import markov_cluster

paths = ["hot_project_50", "hot_project_50_norm"]

for path in paths:
    tsv_path = "tsv/" + path + ".tsv"
    gml_path = "gml/" + path

    G = import_tsv(tsv_path, directed=False)

    communities_gn = girvan_newman(G, 15)
    communities_lp = label_propagation(G)
    communities_mc = markov_cluster(G, power=5, inflation=2, numIter=15, decimals=4)

    print("gn:", len(communities_gn), quality.modularity(G, communities_gn), quality.performance(G, communities_gn))
    print("lp:", len(communities_lp), quality.modularity(G, communities_lp), quality.performance(G, communities_lp))
    print("mc:", len(communities_mc), quality.modularity(G, communities_mc), quality.performance(G, communities_mc))

    export_gml(G, communities_gn, gml_path+"_gn.gml")
    export_gml(G, communities_lp, gml_path+"_lp.gml")
    export_gml(G, communities_mc, gml_path+"_mc.gml")