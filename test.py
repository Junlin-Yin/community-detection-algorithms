import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community.quality import performance, modularity
import numpy as np 
import scipy as sp
from readwrite import import_tsv, export_gml, export_pkl, export_txt
from girvan_newman import girvan_newman
from label_propagation import label_propagation
from markov_cluster import markov_cluster

datasets = ["hot_project_80_norm", "hot_project_100_norm"]
algorithms = ["GN", "LP", "MC"]
functions = [girvan_newman, label_propagation, markov_cluster]

for data in datasets:
    # define file path & build graph
    tsv_path = "tsv/" + data + ".tsv"
    G = import_tsv(tsv_path, directed=False)

    for algorithm, function in zip(algorithms, functions):
        # define file paths  
        # gml_path = "gml/" + data + "_" + algorithm + ".gml"
        txt_path = "txt/" + data + "_" + algorithm + ".txt"
        pkl_path = "pkl/" + data + "_" + algorithm + ".pkl"

        # community detection
        if function == girvan_newman:
            communities = function(G, 15, autothreshold=True)
        elif function == label_propagation:
            communities = function(G)
        elif function == markov_cluster:
            communities = function(G, power=4, inflation=2, numIter=15, decimals=4)
        else:
            communities = []

        # report some key results to stdout
        print(algorithm+":", len(communities), modularity(G, communities), performance(G, communities))

        # report community results to a gml file
        # export_gml(G, communities, gml_path)

        # report community results to a pkl file
        export_pkl(G, communities, pkl_path)

        # report key results and community results to a txt file
        export_txt(data, algorithm, G, communities, txt_path)