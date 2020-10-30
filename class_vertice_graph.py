""" The goal of this file is to have all the information on a graph. """

import numpy as np
inf = np.inf

#Change this bool according to the situation
non_oriented = False

class Vertice:
    """" All the information of one vertice are contained here. """

    def __init__(self, index, coordinates):
        """ Entry : index of the vertice in list_of_vertices
        and the coordinates of the vertice. """
        self._index = index
        self._coordinates = coordinates
        self._neighbours_list = [] # no neighbour by default
        self._priority = inf # priority by default
        self._visited = False # vertice is by default not visited
        self._cost_dijkstra = inf  # cost is by default inf
        self._antecedent = -inf # antecedent not defined before using Dijkstra

    @property
    def index(self):
        """ Returns the index of the vertice. """
        return self._index

    @property
    def coordinates(self):
        """ Returns the coordinates of the vertice. """
        return self._coordinates

    @property
    def neighbours_list(self):
        """ Returns the list of neighbour. """
        return self._neighbours_list

    @property
    def priority(self):
        """ Returns the priority of the vertice. """
        return self._priority

    @property
    def visited(self):
        """ Indicates whether the vertice is visited or not. """
        return self._visited

    @property
    def cost_dijkstra(self):
        """ Returns the cost during Dijkstra algorithm. """
        return self._cost_dijkstra

    @property
    def antecedent(self):
        """ Returns the antecedent of the vertice. """
        return self._antecedent


    # We suppose that the index and the coordinates never change.
    # The other properties can.

    @neighbours_list.setter
    def neighbours_list(self,neighbours_list):
        """ An element of neighbours_list is a tuple
        (neighbour, cost between self and neighbours). """
        self._neighbours_list = neighbours_list

    @priority.setter
    def priority(self,priority):
        self._priority = priority

    @visited.setter
    def visited(self,bool):
        self._visited = bool

    @cost_dijkstra.setter
    def cost_dijkstra(self,d):
        self._cost_dijkstra = d

    @antecedent.setter
    def antecedent(self,vertice):
        self._antecedent = vertice

    def number_of_neighbours(self):
        return len(self._neighbours_list)

    def is_linked(self,other):
        """returns True if there is an edge between self and other"""
        for (neighbour,cost) in self._neighbours_list:
            if other == neighbour:
                return True
        return False

    def __repr__(self):
        return "Vertice "+str(self._index)

    def __lt__(self, other):
        return self._priority < other._priority


class Graph:
    """ All the information of a graph are contained here. """
    def __init__(self,list_of_vertices):
        """ Entry : the list of vertices. """
        self._list_of_vertices = list_of_vertices
        self._number_of_vertices = len(list_of_vertices)

    @property
    def list_of_vertices(self):
        """ Returns the list of vertices. """
        return self._list_of_vertices

    @property
    def number_of_vertices(self):
        """ Returns the number of vertices. """
        return self._number_of_vertices

    def laplace_matrix(self):
        """ Returns the laplace matrix. """
        n = self._number_of_vertices
        laplace_matrix = np.zeros((n, n))
        for i in range(n):
            laplace_matrix[i][i] = 1
            vertice = self._list_of_vertices[i]
            for (neighbour,cost) in vertice.neighbours_list:
                laplace_matrix[i][neighbour.index] = 1
        return laplace_matrix

    def pairs_of_vertices(self):
        """Returns the pairs of connected vertices.
        Beware ! There might be non-connected vertices in the graph. """
        pairs_of_vertices = []
        for vertice in self._list_of_vertices:
            for (neighbour,cost) in vertice.neighbours_list:
                if non_oriented:
                    if (vertice,neighbour) and (neighbour,vertice) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice,neighbour))
                if not non_oriented:
                    if (vertice,neighbour) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice,neighbour))
        return pairs_of_vertices

    def number_of_edges(self):
        return len(self.pairs_of_vertices())




#test
# vertice0 = Vertice(0,(0,0))
# vertice1 = Vertice(1,(0,0))
# vertice2 = Vertice(2,(0,0))
# vertice3 = Vertice(3,(0,0))
# vertice0.neighbours_list = [(vertice1,0),(vertice2,0),(vertice3,0)]
# vertice1.neighbours_list = [(vertice0,0),(vertice2,0)]
# vertice2.neighbours_list = [(vertice0,0),(vertice1,0)]
# vertice3.neighbours_list = [(vertice0,0)]
#
# graph_test = Graph([vertice0,vertice1,vertice2,vertice3])










