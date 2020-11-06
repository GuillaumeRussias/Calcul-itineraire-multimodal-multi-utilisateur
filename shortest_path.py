#using SCIPY library
from scipy.sparse.csgraph import dijkstra

def Dj(A,directed=True,start_index=None,predecessor=False):
    """Arguments :
    (i) A=n*n matrix such like A_ij=distance(Vertice_i,Vertice_j) if there is and edge between V_i and V_j  otherwise =0
    (ii) directed is a boolean : True (by default) G is directed. False if G isn't.
    (iii) start_index= vertices from which we want to start path (default value=none) : therefore the programm computes path from every vertices) we assume for the rest of the doc that we gave p vertices as start.
    (iiii) predecessor : Boolean. If True : returns the p*n matrix of predecessor. (False by default)
    returns : dist_matrix,predecessor_matrix (https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.dijkstra.html)
    """
    return dijkstra(A,directed,start_index,predecessor)

def path_finder(A,start_index,end_index,directed=False):
    """returns the list of vertices visited during the path from i to j"""
    path=[]
    dist_matrix,predecessor_matrix=Dj(A,directed,start_index,True)
    path.append(predecessor_matrix[end_index])
    while path[-1]!=start_index and path[-1]>=0:
        path.append(predecessor_matrix[path[-1]])
    path.reverse()
    path.append(end_index)
    return path






#test:
#import numpy as np
#s=np.sqrt(2)/2
#A=[[0,1,0,1,s],[1,0,1,0,0],[0,1,0,1,s],[1,0,1,0,0],[s,0,s,0,0]]
#t=path_finder(A,2,2)
