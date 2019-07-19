import networkx as nx
import numpy as np
import time
from pickle import dump
from networkx.algorithms.community.quality import performance, modularity

def import_tsv_mat(path, directed=False):
    '''Import tsv file and return the adjacenty matrix and the label list.

    Design for jupyter notebook.
    '''
    # fetch data from tsv file
    X = np.genfromtxt(path, delimiter='\t', encoding='utf8', dtype=None)
    
    # label list
    labels = []
    for label in [x[0] for x in X]:
        if label in labels:
            continue
        labels.append(label)
    for label in [x[1] for x in X]:
        if label in labels:
            continue
        labels.append(label)

    # adjmat
    adjmat = np.zeros((len(labels), len(labels)))
    if directed:
        for (s0, s1, w) in X:
            adjmat[labels.index(s0), labels.index(s1)] = w
    else:
        for (s0, s1, w) in X:
            adjmat[labels.index(s0), labels.index(s1)] = adjmat[labels.index(s1), labels.index(s0)] = w   
    return adjmat, labels

def mat2graph(adjmat, labels):
    '''build the graph according to the adjacency matrix and the label list
    '''
    G = nx.Graph()
    for (i, j) in [(i, j) for i in range(adjmat.shape[0]) for j in range(adjmat.shape[1]) if i != j and adjmat[i,j] != 0]:
        G.add_edge(labels[i], labels[j], weight=adjmat[i,j])
    return G

def import_tsv(path, directed=False):
    '''Import tsv file to construct the adjacency matrix and finally return the graph
    '''
    # fetch data from tsv file
    X = np.genfromtxt(path, delimiter='\t', encoding='utf8', dtype=None)
    
    # label list
    labels = []
    for label in [x[0] for x in X]:
        if label in labels:
            continue
        labels.append(label)
    for label in [x[1] for x in X]:
        if label in labels:
            continue
        labels.append(label)

    # adjmat
    adjmat = np.zeros((len(labels), len(labels)))
    if directed:
        for (s0, s1, w) in X:
            adjmat[labels.index(s0), labels.index(s1)] = w
    else:
        for (s0, s1, w) in X:
            adjmat[labels.index(s0), labels.index(s1)] = adjmat[labels.index(s1), labels.index(s0)] = w

    # graph
    G = nx.Graph()
    for (i, j) in [(i, j) for i in range(adjmat.shape[0]) for j in range(adjmat.shape[1]) if i != j and adjmat[i,j] != 0]:
        G.add_edge(labels[i], labels[j], weight=adjmat[i,j])
    print('[Done] import tsv file:', path)
    return G

def export_gml(G, communities, path):
    '''export community result to a gml file for visualization
    '''
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
    print("[Done] export gml file:", path)

def export_pkl(G, communities, path):
    '''export community result to a pkl file for visualization
    '''
    with open(path, 'wb') as f:
        dump((G, tuple(communities)), f)
    
    print("[Done] export pkl file:", path)

def export_txt(G, communities, dataset, algorithm, threshold, path):
    '''export community result to a txt file for manually analysis
    '''
    with open(path, 'w') as f:
        # write some key information first
        line = "dataset: " + dataset + "\n"
        line += "algorithm: " + algorithm + "\n"
        line += "threshold: " + str(threshold) + "\n"
        line += "time: " + time.asctime(time.localtime(time.time())) + "\n"
        line += "-------------------------------------\n"
        line += "communities: " + str(len(communities)) + "\n"
        line += "modularity: " + str(round(modularity(G, communities), 3)) + "\n"
        line += "performance: " + str(round(performance(G, communities), 3)) + "\n"
        line += "=====================================\n"
        f.write(line)

        # write community line by line
        for community in communities:
            namelist = list(community)
            line = ", ".join(namelist)
            f.write(line+'\n')

    print("[Done] export txt file:", path)