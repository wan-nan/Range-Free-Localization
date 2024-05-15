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
    for edge in edgelist:
        x_loc = est_loc[(int)(edge[0])]
        y_loc = est_loc[(int)(edge[1])]
        distance = np.linalg.norm(x_loc - y_loc)
        factor = distance / mrange
        edge[2] = factor

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
    # loc=np.zeros((n,2))

    ## Generate the adjacency matrix from edgelist, if you are not sure, you can
    #  look at the getedges.m sample

    # 获取节点数
    size = n
    # size = len(edgelist)
    # 初始化邻接矩阵
    adjacency = [[0]*size for _ in range(size)]
    # 填充邻接矩阵
    for edge in edgelist:
        adjacency[(int)(edge[0])][(int)(edge[1])] = edge[2]

    ## Generate the Laplacian matrix from the adjacency matrix

    # 计算对角矩阵D，对角线元素为A每行元素之和
    A = np.array(adjacency)
    D = np.diag(np.sum(A, axis=1))
    # 计算矩阵L，L = D - A
    L = D - A

    ## Handle special cases for all anchor nodes
    rightMatrix = np.zeros((size, 2))
    # 遍历锚点列表，将矩阵L中包含锚点的行的对角线元素设置为1，其余元素设为0
    for ac in anchor:
        node_id = ac[0]
        if node_id < len(L):
            L[(int)(node_id)].fill(0)
            L[(int)(node_id)][(int)(node_id)] = 1
        rightMatrix[(int)(node_id)] = ac[1:]

    ## Inverse the modified Laplacian matrix 
    # 计算矩阵L的逆矩阵
    L_inv = np.linalg.inv(L)

    ## Use the inverse matrix to calculate estimated positions
    estimatedLoc = np.matmul(L_inv, rightMatrix)

    return estimatedLoc