import networkx
from networkx.algorithms import community
from networkx.algorithms.community import quality

def label_propagation(G, weight='weight', iterNum=6):
    '''Community detection using label propagation algorithm.
    
    Parameters
    ----------
    G : networkx.graph
    
    weight : edge attribute if G is weighted or None if G is unweighted

    iterNum : number to repeat label propagation algorithm

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
    max_modularity = float('-inf')
    for i in range(iterNum):
        if weight is None:
            cur_list_communities = list(community.label_propagation_communities(H))
        else:
            cur_list_communities = list(community.asyn_lpa_communities(H, weight=weight))
        
        cur_modularity = quality.modularity(H, cur_list_communities)
        if(cur_modularity > max_modularity):
            list_communities = cur_list_communities
            max_modularity = cur_modularity

    return list_communities