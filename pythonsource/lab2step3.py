##############################################
#  Localization experiment lab2 step2
#  Nanjing University Dislab
#  Author: Shang Zeng
#  Date:  2023/1/11
############################################## 

import numpy as np
import scipy.sparse as sps
import scipy.linalg as linalg


def mds(n, edgelist):
    '''    
    calculate the mds relative location given the edgelist

    Input 
       -- n: number of nodes in the network
       -- edgelist: the list of edges, with only the tail and head node id
    Output
       -- mds_loc: the estimated relative locations using MDS method
    '''

    ## You should write your own version of this function
    mds_loc=np.zeros( (n,2)) 

    ## Calculate the shortest paths for all pair of nodes


    ## Calculate the matrix Y from shortest path distance


    ## SVD decomposition for the matrix Y


    ## Get the estimated svd location from matrix Y
    
    return mds_loc