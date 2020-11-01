""" The goal of this file is to have all the information on a graph. """

import numpy as np
import matplotlib.pyplot as plt
inf = np.inf

#Change this bool according to the situation
non_oriented = False

class Vertice:
    """" All the information of one vertice are contained here. """

    def __init__(self, index, coordinates):
        """ Entry : index of the vertice in list_of_vertices
        and the coordinates of the vertice. """
        self._index = index
        self._coordinates = np.array([coordinates[0],coordinates[1]])
        self._edges_list = [] # no neighbour by default
        self._priority = inf # priority by default
        self._visited = False # vertice is by default not visited
        self._cost_dijkstra = inf  # cost is by default inf
        self._antecedent = -inf # antecedent not defined before using Dijkstra

        #database
        self._id=None
        self.gare_name=None
        self.color=None


    def get_lines_connected(self):
        list_of_line=[]
        for edge in self._edges_list:
            if edge.id not in list_of_line:
                list_of_line.append(edge.id)
        return list_of_line

    @property
    def index(self):
        """ Returns the index of the vertice. """
        return self._index

    @property
    def coordinates(self):
        """ Returns the coordinates of the vertice. """
        return self._coordinates

    @property
    def edges_list(self):
        """ Returns the list of neighbour. """
        return self._edges_list

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

    @property
    def id(self):
        """"returns the id"""
        return self._id


    # We suppose that the index and the coordinates never change.
    # The other properties can.

    @edges_list.setter
    def edges_list(self,edges_list):
        """ An element of edges_list is an edge """
        self._edges_list = edges_list

    def neighbours_list(self,list_tuple,id=0):
        self._edges_list.clear()
        """interface with old constructor , tuple=(neighbour_vertice,cost) is an element of list_tuple """
        for tuple in list_tuple:
            E=Edge(self,tuple[0],id,tuple[1])
            self._edges_list.append(E)

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

    @id.setter
    def id(self,id):
        self._id=id

    def number_of_neighbours(self):
        return len(self._edges_list)

    def is_linked(self,other):
        """returns True if there is an edge between self and other"""
        for edge in self._edges_list:
            if other == edge.linked[1]:
                return True
        return False

    def push_edge(self,edge):
        self._edges_list.append(edge)

    def __repr__(self):
        return "Vertice "+str(self._index)

    def __lt__(self, other):
        return self._priority < other._priority

class Edge:
    def __init__(self,vertice1,vertice2,id,given_cost=0):
        self._linked=[vertice1,vertice2]
        self._id=id
        self._given_cost=given_cost
        #data_base
        self.color=None


    #ne pas mettre @property ici, on veut une methode pas un attribut
    def euclidian_cost(self):
        return np.sqrt(self.square_euclidian_cost())
    def square_euclidian_cost(self):
        return np.dot(np.transpose(self._linked[0].coordinates-self._linked[1].coordinates),(self._linked[0].coordinates-self._linked[1].coordinates))
    #ne pas mettre @property ici, on veut une methode pas un attribut
    def given_cost(self):
        return self._given_cost

    @property
    def linked(self):
        return self._linked
    @property
    def id(self):
        return self._id

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

    def push_vertice(self,vertice):
        self._list_of_vertices.append(vertice)
        self._number_of_vertices+=1

    def push_vertice_without_doublons(self,vertice):
        bool,index=self.is_vertice_in_graph_based_on_xy(vertice)
        if bool==False:
            self.push_vertice(vertice)
        else:
            for edge in vertice.edges_list:
                if edge not in self._list_of_vertices[index].edges_list:
                    self._list_of_vertices[index].push_edge(edge)


    def is_vertice_in_graph_based_on_xy(self,vertice):
        for i in range(self._number_of_vertices):
            v=self._list_of_vertices[i]
            if v.coordinates[0]==vertice.coordinates[0] and v.coordinates[1]==vertice.coordinates[1]:
                return True,i
        return False,None

    def is_vertice_in_graph_based_on_xy_with_tolerance(self,vertice,epsilon):
        for i in range(self._number_of_vertices):
            v=self._list_of_vertices[i]
            if ((v.coordinates[0]-vertice.coordinates[0])**2)+((v.coordinates[1]-vertice.coordinates[1])**2)<epsilon:
                return True,i
        return False,None


    def __getitem__(self, key):#implement instance[key]
        if key>=0 and key<self._number_of_vertices:
            return self._list_of_vertices[key]
        else :
            raise IndexError

    def laplace_matrix(self):
        """ Returns the laplace matrix. """
        n = self._number_of_vertices
        laplace_matrix = np.zeros((n, n))
        for i in range(n):
            laplace_matrix[i][i] = 1
            vertice = self._list_of_vertices[i]
            for edge in vertice.edges_list:
                laplace_matrix[i][edge.linked[1].index] = 1
        return laplace_matrix

    def pairs_of_vertices(self):
        """Returns the pairs of connected vertices.
        Beware ! There might be non-connected vertices in the graph. """
        pairs_of_vertices = []
        for vertice in self._list_of_vertices:
            for edge in vertice.edges_list:
                if non_oriented:
                    if (vertice,edge.linked[1]) and (edge.linked[1],vertice) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice,edge.linked[1]))
                if not non_oriented:
                    if (vertice,edge.linked[1]) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice,edge.linked[1]))
        return pairs_of_vertices

    def number_of_edges(self):
        return len(self.pairs_of_vertices())
    def plot(self):
        plt.clf()
        for v in self._list_of_vertices:
            c="#"+v.color
            plt.scatter(v.coordinates[0],v.coordinates[1],color=c)
            for e in v.edges_list:
                c="#"+e.color
                x=e.linked[0].coordinates[0]
                y=e.linked[0].coordinates[1]
                dx=e.linked[1].coordinates[0]-x
                dy=e.linked[1].coordinates[1]-y
                plt.plot([x,x+dx],[y,y+dy],color=c)
                #plt.arrow(x,y,dx,dy)
        plt.show()





#test
vertice0 = Vertice(0,(0,0))
vertice1 = Vertice(1,(0,0))
vertice2 = Vertice(2,(0,0))
vertice3 = Vertice(3,(0,0))
vertice0.neighbours_list([(vertice1,0),(vertice2,0),(vertice3,0)])
vertice1.neighbours_list([(vertice0,0),(vertice2,0)])
vertice2.neighbours_list([(vertice0,0),(vertice1,0)])
vertice3.neighbours_list([(vertice0,0)])

graph_test = Graph([vertice0,vertice1,vertice2,vertice3])
