##############################################
#  Localization experiment utility script
#  Nanjing University Dislab
#  Author: Shang Zeng
#  Date:  2023/1/11
############################################## 

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.sparse import csr_matrix

def generate_random_network(n, xlimit, ylimit):
    '''
    random network with uniformly distributed nodes in a rectangular

    Input: 
      n: Number of nodes
      xlimit: the sidelength x for the rectangular
      ylimit: the sidelength y for the rectangular  
    Output:
      nodexy: the x and y coordinates for all 
    '''
    nodexy = np.random.rand(n, 2)
    nodexy[:, 0] *= xlimit
    nodexy[:, 1] *= ylimit
    return nodexy

def getedges(nodexy, range_):
    '''
    list and a node-node adjancency matrix for a given network and communication range

    Input: 
      nodexy: the coordinates for the nodes
      range: communication range of the network

    Output:
      edgelist: the list of edges that appears in the network
      adjmatrix: the sparse node-node adjancency matrix'''

    n = nodexy.shape[0]
    dismatrix = squareform(pdist(nodexy))
    dismatrix[dismatrix > range_] = 0
    edgelist = np.where(dismatrix)
    edgelist = np.stack([*edgelist, dismatrix[edgelist]], -1)
    adjmatrix = csr_matrix(
        (edgelist[:, 2], (edgelist[:, 0], edgelist[:, 1])), (n, n))
    return edgelist, adjmatrix

def getanchor(nodes, m):
    '''
    pick anchors along the edges of the network

    Input
       -- nodes: the (x,y) coordinates of the nodes
       -- m: number of anchors per side, there are 4m anchors in total
    Output
       -- anchor: the picked anchor, the first column is the node id, the
       following columns are the x and y corrdinates for the anchor
    '''
    anchor = []
    mx = np.ceil(np.max(nodes[:, 0])).astype(int)
    my = np.ceil(np.max(nodes[:, 1])).astype(int)
    for low in np.arange(0, mx, mx/m):
        high = low+mx/m
        nodeids, = np.where((nodes[:, 0] <= high) & (nodes[:, 0] >= low))
        if nodeids.shape[0]:
            nodestrip = nodes[nodeids, 1]
            id2 = np.argmax(nodestrip)
            anchor.append(nodeids[id2])
            id2 = np.argmin(nodestrip)
            anchor.append(nodeids[id2])

    for low in np.arange(0, my, my/m):
        high = low+my/m
        nodeids, = np.where((nodes[:, 1] <= high) & (nodes[:, 1] >= low))
        if nodeids.shape[0]:
            nodestrip = nodes[nodeids, 0]
            id2 = np.argmax(nodestrip)
            anchor.append(nodeids[id2])
            id2 = np.argmin(nodestrip)
            anchor.append(nodeids[id2])

    anchor = np.stack(anchor)
    anchor = np.unique(anchor)
    anchor = np.concatenate([anchor.reshape(-1, 1), nodes[anchor, :]], -1)
    return anchor

def drawconnection(nodes, edges, anchor=None):
    '''
    Draw the location of nodes and edges between the nodes

    Input:
     -- nodes: the (x,y) coordinates of the nodes
     -- edges: the edgelist
     -- anchor: the position of anchor nodes
    '''
    plt.cla()
    edges = edges[edges[:, 0] > edges[:, 1], :2].astype(int)
    plt.plot([nodes[edges[:, 0], 0], nodes[edges[:, 1], 0]], [
             nodes[edges[:, 0], 1], nodes[edges[:, 1], 1]], color=[0.4, 0.4, 0.4], lw=0.3, zorder=0)
    plt.scatter(nodes[:, 0], nodes[:, 1], 10, 'g', zorder=1)
    if anchor is not None:
        plt.scatter(anchor[:, 1], anchor[:, 2], 10, 'r', zorder=1)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


def compareresults(true_loc, est_loc, anchor=None):
    '''
    draw both the true location and the estimated locations to 
    compare estimation errors

    Input
    -- true_loc: True locations of sensors
    -- est_loc: Estimated locations of sensors
    -- anchor: anchornodes
    '''
    plt.cla()
    n = true_loc.shape[0]
    for j in range(n):
        plt.plot([true_loc[j, 0], est_loc[j, 0]], [true_loc[j, 1],
                                                   est_loc[j, 1]], color=[0.5, 0.5, 0.5], lw=0.3, zorder=0)

    plt.scatter(est_loc[:, 0], est_loc[:, 1], 10, 'k', zorder=1)
    plt.scatter(true_loc[:, 0], true_loc[:, 1], 10, 'g', zorder=1)
    if anchor is not None:
        plt.scatter(anchor[:, 1], anchor[:, 2], 10, 'r', zorder=1)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def gradientdescent(X, y, alpha, num_iters):
    '''
    Gradient descent function to solve the linear regression problem

    Input:
      -- X: the training data
      -- y: the expected output for each training sample
      -- alpha: descent speed
    num_iters: number of iterations for the gradient descent
    Output:
     -- theta: the set of theta values that has been trained'''
    num_samples = y.shape[0]
    theta = np.zeros((X.shape[1], y.shape[1]))
    for iter in range(num_iters):
        newtheta = np.zeros_like(theta)
        for i in range(X.shape[1]):
            for j in range(y.shape[1]):
                newtheta[i, j] = theta[i, j]-alpha/num_samples * \
                    np.sum((X@theta[:, j]-y[:, j])*X[:, i])
        theta = newtheta
    return theta