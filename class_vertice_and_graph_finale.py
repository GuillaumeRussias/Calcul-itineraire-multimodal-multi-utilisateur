""" The goal of this file is to have all the information on a graph. """

#Change this bool according to the situation
non_oriented = True

class Vertice:
    """" All the information of one vertice are contained here. """

    def __init__(self,index,neighbours_list,coordinates):
        """ Entry : index of the vertice in list_vertices
        and a list of neighbours represented by a tuple :
        (index of neighbour in list_vertices, distance between both)
        and the coordinates of the vertice. """
        self._index = index
        self._neighbours_list = neighbours_list
        self._number_of_neighbours = len(self._neighbours_list)
        self._coordinates = coordinates
        self._priority = 0
        self._attendance = 0

    @property
    def index(self):
        """ Returns the index of the vertice. """
        return self._index

    @property
    def neighbours_list(self):
        """ Returns the list of neighbour. """
        return self._neighbours_list

    @property
    def number_of_neighbours(self):
        """ Returns the number of neighbour. """
        return self._number_of_neighbours

    @property
    def coordinates(self):
        """ Returns the coordinates of the vertice. """
        return self._coordinates

    @property
    def priority(self):
        """ Returns the priority of the vertice. """
        return self._priority

    @property
    def attendance(self):
        """ Returns the attendance of the vertice. """
        return self._attendance

    # We suppose that the index, the list of neighbours and the coordinates never change.
    # The other properties can.

    @priority.setter
    def priority(self,priority):
        self._priority = priority

    @attendance.setter
    def attendance(self,vertice_attendance):
        self._attendance = vertice_attendance

    def is_linked(self,other):
        """returns True if there is an edge between self and other"""
        for (neighbour,distance) in self._neighbours_list:
            if other.index == neighbour:
                return True
        return False




class Graph:
    """ All the information of a graph are contained here. """
    def __init__(self,list_of_vertices):
        """ Entry : the list of vertices. """
        self._list_of_vertices = list_of_vertices
        self._number_of_vertices = len(list_of_vertices)

    def laplace_matrix(self):
        """ Returns the laplace matrix. """
        n = self._number_of_vertices
        laplace_matrix = np.zeros((n, n))
        for i in range(n):
            laplace_matrix[i][i] = 1
            vertice = self._list_of_vertices[i]
            for (neighbour,distance) in vertice.neighbours_list:
                laplace_matrix[i][neighbour] = 1
        return laplace_matrix

    def pairs_of_vertices(self):
        """Returns the pairs of connected vertices.
        Beware ! There might be non-connected vertices in the graph. """
        n = self._number_of_vertices
        pairs_of_vertices = []
        for i in range(n):
            vertice = self._list_of_vertices[i]
            for (neighbour,distance) in vertice.neighbours_list:
                if non_oriented:
                    if (i,neighbour) and (neighbour,i) not in pairs_of_vertices:
                        pairs_of_vertices.append((i,neighbour))
                if not non_oriented:
                    if (i,neighbour) not in pairs_of_vertices:
                        pairs_of_vertices.append((i,neighbour))
        return pairs_of_vertices

    def number_of_edges(self):
        return len(self.pairs_of_vertices())




#test
vertice0 = Vertice(0,[(1,0),(2,0),(3,0)],(0,0))
vertice1 = Vertice(1,[(0,0),(2,0)],(0,0))
vertice2 = Vertice(2,[(0,0),(1,0)],(0,0))
vertice3 = Vertice(3,[(0,0)],(0,0))
graph_test = Graph([vertice0,vertice1,vertice2,vertice3])










