function loc=balancenet(n,edgelist,anchor)
%Function loc=balancenet(n,edgelist,anchor)
% find out the balanced locations for all nodes 
% Input:
%    -- n: number of nodes
%    -- edgelist: edge list with the third column to be the weights
%    -- anchor: anchor list: first column is the node id, second and third
%               are corrdinates for the anchors.
% Output:
%    -- loc: estimated locations

%% You should write your own version of this function
loc=zeros(n,2);



%% Generate the adjacency matrix from edgelist, if you are not sure, you can
%  look at the getedges.m sample



%% Generate the Laplacian matrix from the adjacency matrix




%% Handle special cases for all anchor nodes



%% Inverse the modified Laplacian matrix 


%% Use the inverse matrix to calculate estimated positions


end