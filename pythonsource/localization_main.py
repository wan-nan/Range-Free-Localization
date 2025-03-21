##############################################
#  Localization experiment main script
#  Nanjing University Dislab
#  Author: Wei Wang, Shang Zeng, Hujia Yu
#  Date: 2015/3/17 modified 2023/1/11
############################################## 

import time
import numpy as np
from matplotlib import pyplot as plt
from util_loc import *
from lab2step2 import *
from lab2step3 import *


## Step 1: Generate the simulation data
n=500; #number of nodes
x_size=10 #the width of the rectangular
y_size=10 #the length of the rectangular
mrange=1   #communication range
anchor_num=5 # number of anchor nodes

def two_loalization_algorithms(iter, init_time):
    # generate random (x,y) locations for sensor nodes
    true_loc=generate_random_network(n,x_size,y_size)

    # generate edgelist and node adjacency matrix
    # the first two columns in edge list is the tail and head vertex id
    # the thrid column is the distance of the edge
    # adjacency matrix is a n*n sparse matrix
    edgelist,adjmatrix=getedges(true_loc,mrange)

    # get anchor nodes, there are anchor_num anchor nodes on each side of the
    # rectangular, but actual number of anchors may change.
    # the first column in anchor is the node id of the anchor, the next two
    # columns are x and y coordinates
    anchor=getanchor(true_loc,anchor_num)

    # Draw the position and generated graph of the network
    # print('Showing the true locations for sensors')
    # print('Paused, close the figure to continue or use Ctrl-C to stop')

    # drawconnection(true_loc,edgelist,anchor)

    ## Step 2: Graph Laplacian based Localization 
    # You should only use the first two columns of the edge list and the
    # anchor to find out est_loc

    # print('Starting Graph Laplacian based loalization')

    iterations = 5  # number of iterations
    edgeweight = np.ones((edgelist.shape[0], 1)) # initialize edge weights to 1

    start_time = time.time() - init_time
    print("iterations:", iter)
    # print("iterations:", iter, "\n\tLaplacian start     time:", start_time)

    for loops in range(iterations): #iteratively sove the balanced srping network problem
        # You should write your own program to balance the spring network using
        # graph laplacian, source code in lab2step2.py
        est_loc = balancenet(n, np.concatenate([edgelist[:, :2], edgeweight], -1), anchor)

        # You should write your own program to adjust the weight (stiffness) of
        # edges, source code in lab2step2.py    
        edgeweight = adjustweight(est_loc, np.concatenate([edgelist[:, :2], edgeweight], -1), mrange)

        # print('Iteration'+str(loops) )
        # print('Paused, close the figure to continue or use Ctrl-C to stop\n')
        # drawconnection(est_loc, edgelist, anchor)
        
    # show the final result
    # print('Final localization error for laplacian based method. ')
    # print('Paused, close the figure to continue  or use Ctrl-C to stop')
    # compareresults(true_loc,est_loc,anchor);
    execution_time_laplacian = time.time() - init_time - start_time
    print("\tLaplacian Execution Time:", execution_time_laplacian)
    errors_laplacian = np.linalg.norm(true_loc - est_loc, axis=1)
    avg_error_laplacian = np.mean(errors_laplacian)
    print("\tLaplacian Average   Error:", avg_error_laplacian)

    # _________________________________________________________
    start_time = time.time() - init_time
    # print("\tMDS       start     time:", start_time)
    # You need to write your own code to calculate the average localization error
    # the CDF of error distribution.

    ## Step 3 MDS based localization
    # You should only use the first two columns of the edge list and the
    # anchor to find out est_loc

    #use the edge list to get the relative position of sensors
    #you need to write your own code for mds function.

    mds_loc = mds(n, edgelist[:, :2])

    # print('Relative locations for MDS')
    # print('Paused, close the figure to continue or use Ctrl-C to stop')
    # drawconnection(mds_loc, edgelist)

    # Do the scaling and rotation through linear regression
    # put the estimated anchor location as the training data
    training_data = np.concatenate([mds_loc[anchor[:, 0].astype(int), :], np.ones((anchor.shape[0], 1))], -1)
    # the output must be the ture location of the anchors
    true_val = anchor[:, 1:]

    theta = gradientdescent(training_data, true_val, 0.01, 1000)
    est_loc = np.concatenate([mds_loc, np.ones((n, 1))], -1)@theta

    # drawconnection(est_loc, edgelist)
    # print('Absolute locations for MDS')
    # print('Paused, close the figure to continue or use Ctrl-C to stop')

    # compareresults(true_loc, est_loc, anchor)
    # print('Final localization error for MDS method.')
    # print('Paused, close the figure to continue or use Ctrl-C to stop')

    execution_time_MDS = time.time() - init_time - start_time
    print("\tMDS       Execution Time:", execution_time_MDS)
    errors_MDS = np.linalg.norm(true_loc - est_loc, axis=1)
    avg_error_MDS = np.mean(errors_MDS)
    print("\tMDS       Average   Error:", avg_error_MDS)

    return errors_laplacian, errors_MDS, \
            execution_time_laplacian, execution_time_MDS, \
             avg_error_laplacian, avg_error_MDS

if __name__ == "__main__":
    iterations = 100
    errors_laplacian = []  # array to store all errors for laplacian
    errors_mds = []  # array to store all errors for mds
    execution_times_laplacian = []  # array to store all execution times for laplacian
    execution_times_mds = []  # array to store all execution times for mds
    avg_errors_laplacian = []  # array to store all average errors for laplacian
    avg_errors_mds = []  # array to store all average errors for mds
    i = 0
    while i < iterations:
        try:
            # Run the localization algorithms
            a, b, c, d, e, f = two_loalization_algorithms(i, time.time())

            errors_laplacian.extend(a)
            errors_mds.extend(b)
            execution_times_laplacian.append(c)
            execution_times_mds.append(d)
            avg_errors_laplacian.append(e)
            avg_errors_mds.append(f)
        except np.linalg.LinAlgError:
            print("Singular matrix encountered, skipping iteration", i)
            continue
        i += 1
    print("avg time of laplacian:", np.mean(execution_times_laplacian))
    print("avg time of mds:", np.mean(execution_times_mds))
    print("avg error of laplacian:", np.mean(avg_errors_laplacian))
    print("avg error of mds:", np.mean(avg_errors_mds))
    # Plot CDF of errors_laplacian
    plt.figure()
    plt.hist(errors_laplacian, cumulative=True, density=True, bins=100)
    plt.xlabel('Localization Error')
    plt.ylabel('CDF')
    plt.title('CDF of Errors (Laplacian)')
    plt.savefig('figures/errors_laplacian_cdf.png')

    # Plot CDF of errors_mds
    plt.figure()
    plt.hist(errors_mds, cumulative=True, density=True, bins=100)
    plt.xlabel('Localization Error')
    plt.ylabel('CDF')
    plt.title('CDF of Errors (MDS)')
    plt.savefig('figures/errors_mds_cdf.png')