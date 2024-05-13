function mds_loc=mds(n, edgelist)
% Function mds_loc=mds(edgelist)
% calculate the mds relative location given the edgelist
% Input 
%    -- n: number of nodes in the network
%    -- edgelist: the list of edges, with only the tail and head node id
% Output
%    -- mds_loc: the estimated relative locations using MDS method

%% You should write your own version of this function
mds_loc=zeros(n,2);


%% Calculate the shortest paths for all pair of nodes


%% Calculate the matrix Y from shortest path distance


%% SVD decomposition for the matrix Y


%% Get the estimated svd location from matrix Y


end