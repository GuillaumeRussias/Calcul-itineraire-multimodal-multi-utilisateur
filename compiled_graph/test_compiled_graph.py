import fast_graph
import numpy

nbV = 4

def print_path(G,path):
	for i in range(len(path)-1):
		edge = G[path[i]][path[i+1]]
		print("----------")
		print("liason",path[i],"to",path[i+1])
		print("type",edge.type())
		print("selected mission",edge.selected_mission())
		print("transfers_cost",edge.transfers_cost())
		print("----------")



departs=numpy.array([0,1,2,3,2,1],dtype=int)
arrivees=numpy.array([3,2,1,0,0,2],dtype=int)
id = numpy.array([1,2,3,4,5,6])

assert(numpy.max(departs)<nbV)
assert(numpy.max(arrivees)<nbV)
assert(numpy.min(departs)>=0)
assert(numpy.max(arrivees)>=0)
assert (departs.size==arrivees.size)


G=fast_graph.graph(nbV)
G.build_scheduled_edges(departs,arrivees,departs,departs,id)

vertex_0=G[0]
print(vertex_0)

try :
	vertex_4=G[4]
except ValueError:
	print("l'erreur de valeur (ie 4 n'est pas un vertex) a bien ete captee")


edge_0_3=G[0][3]#edge entre 0 et 3
print(edge_0_3)

try :
	vertex_4=G[0][2]
except ValueError:
	print("l'erreur de valeur (ie 0 et 2 ne sont pas liees) a bien ete captee")

#def nouveau graph:

graph="""
   0 ----> 1
   ^       |
   |       |
   |       v
   3 <---- 2
==========TEST1============= (compute 0 to 3)
tdep=0
cost = unitaire : solution attendue (0,1,2,3) arrival_time=3
==========TEST2============= (compute 0 to 3)
tdep = 0
depart_index|arrivee_index |horaire_depart|horaire_arrivee
     0      |     1        |     0        |      1
     0      |     1        |     0        |      2
     1      |     2        |     0        |      1
     1      |     2        |     2        |      3
     2      |     3        |     0        |      1
     2      |     3        |     3        |      4
     3      |     0        |     4        |      5
     3      |     0        |     2        |      3
solution attendue (0,1,2,3) arrival_time= 4
"""
print(graph)

G1=fast_graph.graph(4)
G2=fast_graph.graph(4)
G1.build_free_edges(numpy.array([0,1,2,3]),numpy.array([1,2,3,0]),numpy.array([1,1,1,1]))
departure = numpy.array([0,0,0,2,0,3,4,2])
arrival =numpy.array([1,2,1,3,1,4,5,3])

G2.build_scheduled_edges(numpy.array([0,0,1,1,2,2,3,3]),numpy.array([1,1,2,2,3,3,0,0]),departure,arrival,numpy.array([0,0,1,1,2,2,3,3]))

print("====test 1======")
path = G1.basic_path_finder(0,3)
print(path)
print_path(G1,path)
print("====test 2======")
path = G2.time_path_finder(0,3,0)
print_path(G2,path)
print(path)


