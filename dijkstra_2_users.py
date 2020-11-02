import numpy as np
from dijkstra_1_user_adapté import *

def cost_of_path(graph,path):
    """ Returns the cost of a path. A path is an ordered list
    of vertice.index. """
    cost = 0
    for i in range(len(path)-1):
        first_vertice = graph.list_of_vertices[path[i]]
        second_vertice = graph.list_of_vertices[path[i+1]]
        cost += first_vertice.cost_between(second_vertice)
    return cost

""" We have two users. Two origins start_1_index and start_2_index.
The destination is unknown (and for now without constraint)."""


""" Option 1 : the destination is such as the sum of the cost of each path is minimum."""


def all_path_finder(graph,start_1_index,start_2_index):
    list_of_path = [] #(end_index,cost_of_path)
    for index in range(graph.number_of_vertices):
        if index != start_1_index and index != start_2_index :
            possible_path = Homemade_path_finder(graph,start_1_index,index)
            list_of_path.append((index,cost_of_path(graph,possible_path)))
    return list_of_path

def chose_end_index(graph,start_1_index,start_2_index):
    user_1 = all_path_finder(graph,start_1_index,start_2_index)
    user_2 = all_path_finder(graph,start_2_index,start_1_index)
    sum = []
    for i in range (len(user_1)):
        sum.append((user_1[i][0],user_1[i][1]+user_2[i][1]))
    return min(sum, key = lambda t: t[1])[0]



