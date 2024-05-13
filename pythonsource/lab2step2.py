##############################################
#  Localization experiment lab2 step2
#  Nanjing University Dislab
#  Author: Shang Zeng
#  Date:  2023/1/11
############################################## 

import numpy as np
import scipy.sparse as sps
import scipy.linalg as linalg


def adjustweight(est_loc, edgelist, mrange):
    '''
    Adjust the weight (stiffness) of each edge

    Input 
      -- est_loc: estimated location
      -- edgelist: edge list with original edge weights
      -- range: transmission range
    Output
      -- newweight: the adjusted weight
    '''

    ## You should write your own version of this function

    newweight = edgelist[:, 2]
    
    newweight = newweight.reshape(-1, 1)
    return newweight

def balancenet(n, edgelist, anchor):
    '''
    find out the balanced locations for all nodes 

    Input:
       -- n: number of nodes
       -- edgelist: edge list with the third column to be the weights
       -- anchor: anchor list: first column is the node id, second and third are corrdinates for the anchors.
    Output:
       -- loc: estimated locations
    '''
    ## You should write your own version of this function
    loc=np.zeros((n,2))

    ## Generate the adjacency matrix from edgelist, if you are not sure, you can
    #  look at the getedges.m sample



    ## Generate the Laplacian matrix from the adjacency matrix




    ## Handle special cases for all anchor nodes



    ## Inverse the modified Laplacian matrix 


    ## Use the inverse matrix to calculate estimated positions
    return loc