import networkx
from networkx.algorithms import community

def label_propagation(G, weight='weight'):
    '''Community detection using label propagation algorithm.
    
    Parameters
    ----------
    G : networkx.graph
    
    weight : edge attribute if G is weighted or None if G is unweighted

    Returns
    -------
    list_communities : list
        A list of sets, and each set contains vertices in one community.
    
    Notes
    -----
    This function only deals with weighted and unweighted undirected graph.
    '''
    # H is the undirected version of graph G
    H = G.to_undirected()
    if weight is None:
        communities = community.label_propagation_communities(H)
    else:
        communities = community.asyn_lpa_communities(H, weight=weight)
    list_communities = list(communities)
    return list_communities