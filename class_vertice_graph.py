""" The goal of this file is to have all the information on a graph. """

import numpy as np
import matplotlib.pyplot as plt
import copy
import exceptions
inf = np.inf

#Change this bool according to the situation
non_oriented = False

class Vertice:
    """" All the information of one vertice are contained here. """

    def __init__(self, index, coordinates):
        """ Entry : index of the vertice in list_of_vertices
        and the coordinates of the vertice. """
        self.index = index
        self.coordinates = np.array([coordinates[0],coordinates[1]])
        self._edges_list = [] # no neighbour by default
        self.priority = inf # priority by default
        self.visited = False # vertice is by default not visited
        self.cost_dijkstra = inf  # cost is by default inf
        self.antecedent = -inf # antecedent not defined before using Dijkstra
        #implemente apres passage par panda
        self.index_edges_list = []#seulement implemente apres passage par panda


        #database
        self.id = None #identifiant idfm de la gare
        self.gare_name = None #nom de la gare
        self.color = None #couleur de la gare
        self.is_a_station= True # boolean True, si le noeud est veritablement une gare. False sinon

    def get_lines_connected(self):
        list_of_line = []
        for edge in self._edges_list:
            if edge.id not in list_of_line:
                list_of_line.append(edge.id)
        return list_of_line

    @property
    def edges_list(self):
        """ Returns the list of neighbour. """
        return self._edges_list

    # We suppose that the index and the coordinates never change.
    # The other properties can.

    @edges_list.setter
    def edges_list(self, edges_list):
        """ An element of edges_list is an edge """
        for e in edges_list:
            exceptions.check_pertinent_edge(self, e)
        self._edges_list = edges_list

    def neighbours_list(self, list_tuple, id=0):
        self._edges_list.clear()
        """interface with old constructor , tuple=(neighbour_vertice,cost) is an element of list_tuple """
        for tuple in list_tuple:
            E = Edge(self, tuple[0], id, tuple[1])
            self._edges_list.append(E)

    def number_of_neighbours(self):
        return len(self._edges_list)

    def is_linked(self, other):
        """returns True if there is an edge between self and other"""
        for edge in self._edges_list:
            if other.index == edge.linked[1].index:
                return True
        return False

    def push_edge(self, edge, coords_verif=False):
        if coords_verif:
            exceptions.check_pertinent_edge_coords_verif(self, edge)
        else:
            exceptions.check_pertinent_edge(self, edge)
        self._edges_list.append(edge)

    """
    def cost_between(self, other):
        for edge in self._edges_list:
            [vertice, vertice_voisin] = edge.linked
            if vertice_voisin == other:
                return edge.given_cost"""

    def __repr__(self):
        return f"Vertice {str(self.index)}"

    def __lt__(self, other):
        return self.priority < other.priority

class Edge:
    def __init__(self, vertice1, vertice2, id, given_cost=0):
        self.linked = [vertice1,vertice2]
        self.id = id #identifiant de la liaison. ici id=nom de la ligne a laqualle appartient la liaison
        self._given_cost = given_cost #cout de deplacement de la liason donne par l'utilisateur ou la base de donnee
        #data_base
        self.color=None #couleur de la liason
        self.connection_with_displayable=None #indice de la liason developpee( trace reel) dans la table de connection connection_table_edge_and_diplayable_edge de la classe graph
        self.index=None
    def set_given_cost(self,cost):
        self._given_cost=cost
    #ne pas mettre @property ici, on veut une methode pas un attribut
    def euclidian_cost(self):
        return np.sqrt(self.square_euclidian_cost())
    def square_euclidian_cost(self):
        return np.dot(np.transpose(self.linked[0].coordinates-self.linked[1].coordinates),(self.linked[0].coordinates-self.linked[1].coordinates))
    def customized_cost1(self):
        V_metro = 25.1 / 3.6 #vitesse moyenne en km/h /3.6 -> vitesse moyenne en m/s
        V_train = 49.6 / 3.6
        V_tram = 18 / 3.6
        V_pieton = 4 / 3.6
        if self.id in ["A","B","C","D","E","H","I","J","K","L","M","N","P","R","U","TER","GL"]:
            return self._given_cost/V_train
        if self.id in [str(i) for i in range(1,15)]+["ORL","CDG","3b","7b"]:
            return self._given_cost/V_metro
        if self.id in ["T"+str(i) for i in range(1,12)]+["T3A","T3B","FUN"]:
            return self._given_cost/V_tram
        if self.id in ["RER Walk"]:
            return self._given_cost/V_pieton
        raise ValueError(" Dans customized_cost1 " +self.id+" non pris en compte dans le calcul de distance")


    #ne pas mettre @property ici, on veut une methode pas un attribut
    def given_cost(self):
        return self._given_cost
    def __repr__(self):
        return f"Edge [{str(self.linked[0].index)}, {str(self.linked[1].index)}] !oriented!"



class Graph:
    """ All the information of a graph are contained here. """
    def __init__(self,list_of_vertices):
        """ Entry : the list of vertices. """
        self.list_of_vertices = list_of_vertices
        self.number_of_vertices = len(list_of_vertices)
        self.connection_table_edge_and_diplayable_edge=[]
        self.list_of_edges=[]
        self.number_of_edges=0

    def push_diplayable_edge(self,bidim_array):
        self.connection_table_edge_and_diplayable_edge.append(copy.deepcopy(bidim_array))
        self.number_of_edges+=1
    def push_edge(self,e):
        self.list_of_edges.append(e)


    def push_vertice(self,vertice):
        self.list_of_vertices.append(vertice)
        self.number_of_vertices += 1

    def push_vertice_without_doublons(self, vertice):
        bool,index = self.is_vertice_in_graph_based_on_xy(vertice)
        if bool == False:
            self.push_vertice(vertice)
        else:
            for edge in vertice.edges_list:
                if edge not in self.list_of_vertices[index].edges_list:
                    self.list_of_vertices[index].push_edge(edge,True)


    def is_vertice_in_graph_based_on_xy(self,vertice):
        for i in range(self.number_of_vertices):
            v = self.list_of_vertices[i]
            if v.coordinates[0] == vertice.coordinates[0] and v.coordinates[1] == vertice.coordinates[1]:
                return True,i
        return False,None

    def is_vertice_in_graph_based_on_xy_with_tolerance(self, vertice, epsilon):
        for i in range(self.number_of_vertices):
            v = self.list_of_vertices[i]
            if ((v.coordinates[0] - vertice.coordinates[0])**2) + ((v.coordinates[1] - vertice.coordinates[1])**2) < epsilon:
                return True, i
        return False, None


    def __getitem__(self, key):#implement instance[key]
        if key >= 0 and key < self.number_of_vertices:
            return self.list_of_vertices[key]
        else :
            raise IndexError

    def laplace_matrix(self):
        """ Returns the laplace matrix. """
        n = self.number_of_vertices
        laplace_matrix = np.zeros((n, n))
        for i in range(n):
            laplace_matrix[i][i] = 1
            vertice = self.list_of_vertices[i]
            for edge in vertice.edges_list:
                laplace_matrix[i][edge.linked[1].index] = 1
        return laplace_matrix

    def A_matrix(self,type_cost=Edge.given_cost):
        """ Returns the laplace matrix. """
        n = self.number_of_vertices
        A_matrix = np.zeros((n, n))
        for i in range(n):
            vertice = self.list_of_vertices[i]
            for edge in vertice.edges_list:
                cost = type_cost(edge)
                A_matrix[i][edge.linked[1].index] = cost
                A_matrix[edge.linked[1].index][i] = cost
        return A_matrix

    def pairs_of_vertices(self):
        """Returns the pairs of connected vertices.
        Beware ! There might be non-connected vertices in the graph. """
        pairs_of_vertices = []
        for vertice in self.list_of_vertices:
            for edge in vertice.edges_list:
                if non_oriented:
                    if (vertice, edge.linked[1]) and (edge.linked[1], vertice) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice, edge.linked[1]))
                if not non_oriented:
                    if (vertice, edge.linked[1]) not in pairs_of_vertices:
                        pairs_of_vertices.append((vertice, edge.linked[1]))
        return pairs_of_vertices

    def number_of_edges(self):
        return len(self.pairs_of_vertices())

    def search_index_by_coordinates(self,coord):
        """search the index of vertice at coordinates: """
        for i in range(len(self.list_of_vertices)):
            if self[i].coordinates[0]==coord[0] and self[i].coordinates[1]==coord[1]:
                return i

    def set_right_edges(self):
        """verify that the graph is coherent """
        for v in self:
            for e in v.edges_list:
                e.linked[0]=v
                e.linked[1]=self[self.search_index_by_coordinates(e.linked[1].coordinates)]
        for e in self.list_of_edges:
            e.linked[0]=self[self.search_index_by_coordinates(e.linked[0].coordinates)]
            e.linked[1]=self[self.search_index_by_coordinates(e.linked[1].coordinates)]


    def plot(self):
        plt.clf()
        for v in self._list_of_vertices:
            c = f"#{v.color}"
            plt.scatter(v.coordinates[0], v.coordinates[1], color=c)
            for e in v.edges_list:
                c = f"#{e.color}"
                x = e.linked[0].coordinates[0]
                y = e.linked[0].coordinates[1]
                dx = e.linked[1].coordinates[0] - x
                dy = e.linked[1].coordinates[1] - y
                plt.plot([x,x+dx], [y,y+dy], color=c)
                # plt.arrow(x,y,dx,dy)
        plt.axis = 'off'
        plt.show()

    def plot_dev(self):
        plt.clf()
        for v in self._list_of_vertices:
            c = f"#{v.color}"
            plt.scatter(v.coordinates[0], v.coordinates[1], color=c)
            for e in v.edges_list:
                c = f"#{e.color}"
                for i in range(len(self.connection_table_edge_and_diplayable_edge[e.connection_with_displayable])-1):
                    x = self.connection_table_edge_and_diplayable_edge[e.connection_with_displayable][i][0]
                    y = self.connection_table_edge_and_diplayable_edge[e.connection_with_displayable][i][1]
                    dx = self.connection_table_edge_and_diplayable_edge[e.connection_with_displayable][i+1][0]-x
                    dy = self.connection_table_edge_and_diplayable_edge[e.connection_with_displayable][i+1][1]-y
                    plt.plot([x,x+dx], [y,y+dy], color=c)
        plt.axis = 'off'
        plt.show()
