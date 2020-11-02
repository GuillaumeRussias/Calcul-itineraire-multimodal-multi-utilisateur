import numpy as np
from class_vertice_graph import *
#Pour que ça fonctionne ne pas oublier de faire clic droit,
#"définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"
from queue import PriorityQueue as priorQ

def homemade_dijkstra(graph,start_index,type_cost=Edge.given_cost):
    PQ = priorQ()#initialisation file de priorité
    start_vertice = graph.list_of_vertices[start_index]
    start_vertice.priority = 0
    start_vertice.cost_dijkstra = 0
    start_vertice.visited = True
    PQ.put(start_vertice)
    #vertice de départ : priorité 0, coût 0 et déja visité

    while PQ.empty() == False:
        top_vertice = PQ.get()
        #withdraws the upper element of the queue (lowest priority)
        for edge in top_vertice.edges_list :
            v=edge.linked[1]
            cost_between=type_cost(edge)
            if v.visited == False : #verifies if not visited yet

                new_cost = top_vertice.cost_dijkstra + cost_between
                #on calcule le coût du voyage pour aller vers v
                #en passant par top_vertice

                if new_cost < v.cost_dijkstra:
                #on la compare avec l'ancien coût
                    v.cost_dijkstra = new_cost
                    v.antecedent = top_vertice

                graph.list_of_vertices[top_vertice.index].visited = True
                #top vertice est maintenant visité
                v.priority = v.cost_dijkstra
                #on met v dans la file de priorite avec la priorite cost
                PQ.put(v)

def Homemade_path_finder(graph,start_index,end_index,type_cost=Edge.given_cost):
    """ Returns the list of vertices visited during the path from i to j. """

    homemade_dijkstra(graph,start_index,type_cost)
    path = [end_index]
    while path[-1] != start_index:
        path.append(graph.list_of_vertices[path[-1]].antecedent.index)
    path.reverse()
    return path

#test
vertice0 = Vertice(0,(0,0))
vertice1 = Vertice(1,(0,0))
vertice2 = Vertice(2,(0,0))
vertice3 = Vertice(3,(0,0))
vertice4 = Vertice(4,(0,0))
vertice5 = Vertice(5,(0,0))
edge1 = Edge(vertice0,vertice1,1,1)
edge2 = Edge(vertice0,vertice2,2,2)
edge3 = Edge(vertice1,vertice3,3,1)
edge4 = Edge(vertice2,vertice4,4,3)
edge5 = Edge(vertice3,vertice5,5,4)
edge6 = Edge(vertice4,vertice5,6,1)
edge7 = Edge(vertice3,vertice4,7,1)
vertice0.edges_list = [edge1,edge2]
vertice1.edges_list = [edge1,edge3]
vertice2.edges_list = [edge2,edge4]
vertice3.edges_list = [edge5,edge3,edge7]
vertice4.edges_list = [edge6,edge4,edge7]
vertice5.edges_list = [edge5,edge6]


graph_test = Graph([vertice0,vertice1,vertice2,vertice3,vertice4,vertice5])





