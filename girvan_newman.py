import networkx as nx 
from networkx.algorithms import community
from networkx.algorithms.community import quality
import itertools

def girvan_newman(G, k, weight='weight', autothreshold=False):
    '''Community detection using Girvan-Newman algorithm.
    
    Parameters
    ----------
    G : networkx.graph

    k : number of communities
    
    weight : edge attribute if G is weighted or None if G is unweighted

    autothreshold : thresholding automatically according to modularity value

    Returns
    -------
    list_communities : list
        A list of k sets, and each set contains vertices in one community.
    
    Notes
    -----
    This function only deals with undirected graph.
    '''
    # determine most_valuable_edge according to weighted or not
    mvg = None if weight is None else most_valuable_edge
    communities = community.girvan_newman(G.to_undirected(), most_valuable_edge=mvg)

    if not autothreshold:
        # k must be not larger than number of nodes, or return an empty set
        if k > len(G.nodes()):
            return []

        # get (k-1)th community partition
        for com in itertools.islice(communities, k-1):
            list_communities = list(com)
    else:
        # find the list_communities that contributes to maximum modularity
        max_modularity = float('-inf')
        for com in itertools.islice(communities, k-1):
            cur_list_communities = list(com)
            cur_modularity = quality.modularity(G, cur_list_communities)

            if cur_modularity > max_modularity:
                list_communities = cur_list_communities
                max_modularity = cur_modularity

    return list_communities

def most_valuable_edge(G):
    """Returns the edge with the highest betweenness centrality in the directed graph `G`.
    """
    betweenness = nx.edge_betweenness_centrality(G)
    # betweenness / weight for each edge
    for (vs, b) in betweenness.items():
        w = G[vs[0]][vs[1]]['weight']
        betweenness[vs] /= w
    return max(betweenness, key=betweenness.get)