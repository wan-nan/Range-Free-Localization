##############################################
#  Localization experiment lab2 step2
#  Nanjing University Dislab
#  Author: Shang Zeng
#  Date:  2023/1/11
############################################## 

import numpy as np
import scipy.sparse as sps
import scipy.linalg as linalg
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


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
   # 初始化邻接矩阵
   adjacency = [[0]*n for _ in range(n)]
   # 填充邻接矩阵
   for edge in edgelist:
      adjacency[(int)(edge[0])][(int)(edge[1])] = 1
   # 将邻接矩阵转换为稀疏矩阵
   graph_sparse = csr_matrix(adjacency)
   # 计算最短路径距离矩阵
   dist_matrix = shortest_path(csgraph=graph_sparse, directed=False, unweighted=True)

   ## Calculate the matrix Y from shortest path distance
   # 假设dist_matrix已经定义好，是一个NxN的numpy数组
   n = dist_matrix.shape[0]
   D_squared = np.square(dist_matrix)

   # 对行和列求和
   row_sum = D_squared.sum(axis=1).reshape(n, 1) / n
   col_sum = D_squared.sum(axis=0).reshape(1, n) / n
   total_sum = D_squared.sum() / (n**2)

   # 根据公式计算Y矩阵
   Y = -0.5 * (D_squared - row_sum - col_sum + total_sum)

   ## SVD decomposition for the matrix Y
   # The matrix Y is a symmetric positive semidefinite matrix.
   U, S, Vh = np.linalg.svd(Y)

   ## Get the estimated svd location from matrix Y
   # 取出大于0的奇异值对应的奇异向量
   positive_singular_values = np.sqrt(S[S > 0])
   X = U[:, S > 0] * positive_singular_values
   X = X[:, :2]
   
   return X