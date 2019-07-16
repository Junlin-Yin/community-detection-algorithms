import networkx as nx 
from networkx.algorithms import community
import itertools

def girvan_newman(G, k, weight='weight'):
    '''Community detection using Girvan-Newman algorithm.
    
    Parameters
    ----------
    G : networkx.graph

    k : number of communities
    
    weight : edge attribute if G is weighted or None if G is unweighted

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

    # k must be not larger than number of nodes, or return an empty set
    if k > len(G.nodes()):
        return []

    # get (k-1)th community partition
    for com in itertools.islice(communities, k-1):
        list_communities = list(com)
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