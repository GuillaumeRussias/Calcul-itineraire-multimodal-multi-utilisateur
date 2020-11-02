from queue import PriorityQueue as priorQ
import numpy as np

inf = np.inf

class vertice:
    def __init__(self, index):
        self._index = index#indice du sommet
        self._priority = inf #priorité par défaut
        self._visited = False #le sommet n'est pas visité par défaut
        self._distance = inf  #distance infinie par défaut
        self._antecedent =- inf #antécédent non défini avant l'utilisation de dijkstra

    """definition de la relation d'ordre pour la file de priorité """

    def __lt__(self, other): # implements <
        return self._priority < other._priority

    """ acces aux champs"""

    def index(self):
        return self._index
    def visited(self):
        return self._visited
    def distance(self):
        return self._distance
    def antecedent(self):
        return self._antecedent

    """ecriture dans les champs"""

    def set_priority(self,priority):
        self._priority = priority
    def set_visited(self, bool):
        self._visited = bool
    def set_distance(self, distance):
        self._distance = distance
    def set_antecedent(self, other):
        self._antecedent = other._index


    def __repr__(self):
        """help debug"""
        return f"Vertice : {str(self._index)} Antecedent : {str(self._antecedent)} Distance : {str(self._distance)} Visted : {str(self._visited)}"

    def is_linked(self, other, A):
        """return True if there is an edge between self and other"""
        return A[self._index][other._index] > 0
    def dist(self, other, A):
        """return the lenght of the edge"""
        return A[self._index][other._index]


def homemade_dijkstra(A, start_index, list_vertices):
    PQ = priorQ() # initialisation file de priorité
    list_vertices[start_index].set_priority(0)
    list_vertices[start_index].set_distance(0)
    list_vertices[start_index].set_visited(True)
    PQ.put(list_vertices[start_index])
    # vertice de départ : priorité 0, distance 0 et déja visité

    while PQ.empty() == False:
        top_vertice = PQ.get() # withdraw the upper element of the queue (lowest priority)
        for v in list_vertices:
            if v.visited() == False and top_vertice.is_linked(v, A): # verify if linked and not visited yet

                dist = top_vertice.distance() + top_vertice.dist(v, A) # on calcule le cout du voyage pour aller vers v en passant par top_vertice

                if dist < v.distance(): # on la compare avec l ancienne distance
                    v.set_distance(dist)
                    v.set_antecedent(top_vertice)

                list_vertices[top_vertice.index()].set_visited(True) # top vertice est maintenant visite
                v.set_priority(v.distance()) # on met v dans la file de priorite avec la priorite distance
                PQ.put(v)

def Homemade_path_finder(A, start_index, end_index, directed=True):
    """returns the list of vertices visited during the path from i to j"""
    list_vertices = [vertice(i) for i in range(len(A))]

    homemade_dijkstra(A, start_index, list_vertices)

    path = [end_index]
    while path[-1] != start_index:

        path.append(list_vertices[path[-1]].antecedent())
    path.reverse()
    return path


import numpy as np
s = np.sqrt(2)/2
A = [[0,1,0,1,s],[1,0,1,0,0],[0,1,0,1,s],[1,0,1,0,0],[s,0,s,0,0]]
t = Homemade_path_finder(A,0,2)














