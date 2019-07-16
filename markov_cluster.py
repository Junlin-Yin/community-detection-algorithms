import networkx as nx 
import operator
import numpy as np 
import scipy as sp 

def markov_cluster(G, power=2, inflation=2, numIter=5, decimals=2):
    '''Community detection using Markov Clustering algorithm.
    
    Parameters
    ----------
    G : networkx.graph

    power : exponent number in expanding step, default value is 2

    inflation : exponent number in inflating step, default value is 2

    numIter : number of iteration, default value is 5; numIter gets larger, the communities gets fewer
    
    decimals : precision degree when rounding the finalMatrix, default value is 2

    Returns
    -------
    list_communities : list
        A list of sets, and each set contains vertices in one community.
    
    Notes
    -----
    This function can deals with both undirected and directed graph. 
    Whether weighted or unweighted graphs are both ok.
    '''
    adjmat = nx.adj_matrix(G)
    adjmat = np.copy(adjmat.todense())

    one_mat = np.eye(len(adjmat), dtype=float)
    adjmat = adjmat + one_mat

    columnSum = np.sum(adjmat, axis=0)
    inflateMat = adjmat / columnSum
     
    for i in range(numIter):
        expand = _expand(inflateMat, power)
        inflateMat = _inflate(expand, inflation)

    finalMat = np.round(inflateMat, decimals=decimals)
    list_communities = mining_communities(G, finalMat)
    return list_communities

def mining_communities(G, finalMat):
    '''Detect communities with final matrix
    '''
    # find all the vertical vectors in final matrix and put them into a set
    # each unique vertical vector represent a community
    vvectors = set([tuple(finalMat[:,i]) for i in range(finalMat.shape[1])])

    # fetch the ordered label list
    labels = list(G.nodes())

    list_communities = []
    for vvector in vvectors:
        # recognize each community
        community = [labels[i] for i in range(finalMat.shape[1]) if operator.eq(tuple(finalMat[:,i]), vvector) == True]
        
        # add current community into list_communities
        list_communities.append(set(community))
    return list_communities

def _expand(probabilityMat, power):
    '''Expand by taking the power of the matrix
    '''
    expandMat = np.copy(probabilityMat)
    for i in range(power - 1):
        expandMat = np.dot(expandMat, probabilityMat)
    return expandMat

def _inflate(expandMat, inflation):
    '''Inflate by taking inflation of the resulting matrix with parameter inflation.
    '''
    powerMat = np.copy(expandMat)
    for i in range(inflation - 1):
        powerMat = powerMat * expandMat
    inflateColumnSum = np.sum(powerMat, axis=0)
    inflateMat = powerMat / inflateColumnSum
    return inflateMat