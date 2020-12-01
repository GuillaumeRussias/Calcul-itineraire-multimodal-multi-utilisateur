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
G.build_scheduled_edges(departs,arrivees,departs,arrivees,id)

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
G1.build_free_edges(numpy.array([0,1,2,3]),numpy.array([1,2,3,0]),numpy.array([1,1,1,1]),numpy.array([0,1,2,3]))
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


graph="""
==========TEST3=============
   0 <---> 1 <---> 4 <---> 5
   ^       ^               ^
   |       |               |
   v       v               |
   3 <---> 2<-------------/
cout unitaire ,  A compute (4,2) , B(5,3), C(0,2), D (1,3), E (5,0)
"""
print(graph)
G3=fast_graph.graph(6)
G3.build_free_edges(numpy.array([0,0,1,1,1,2,2,2,3,3,4,4,5,5]),numpy.array([1,3,0,2,4,3,1,5,0,2,1,5,4,2]),numpy.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1]),numpy.array([0,0,1,1,1,2,2,2,3,3,4,4,5,5]))
path = G3.basic_path_finder(4,2)
print("=======A=======")
print(path)
print_path(G3,path)
path = G3.basic_path_finder(5,3)
print("=======B=======")
print(path)
print_path(G3,path)
path = G3.basic_path_finder(0,2)
print("=======C=======")
print(path)
print_path(G3,path)
path = G3.basic_path_finder(1,3)
print("=======D=======")
print(path)
print_path(G3,path)
path = G3.basic_path_finder(5,0)
print("=======E=======")
print(path)
print_path(G3,path)


graph="""
==========TEST4============= MIXED graph
   0 ----> 1
   ^       |
   |       |
   |       v
   3 <---- 2
 depart_index|arrivee_index |horaire_depart|horaire_arrivee
      0      |     1        |     0        |      1
      0      |     1        |     0        |      2
      1      |     2        |     0        |      1
      1      |     2        |     2        |      3
      2      |     3        |     0        |      1
      2      |     3        |     3        |      4
      3      |     0        |     4        |      5
      3      |     0        |     2        |      3
	+ cout liaison libre pour chaque noeud egal à 1
on affiche successivement les voisins de chaque noeud

+compute(0->3)
"""
G4 = fast_graph.graph(4)
departure = numpy.array([0,0,0,0,0,2,3,2])
arrival =numpy.array([1,1,1,5,2,3,4,3])
G4.build_scheduled_edges(numpy.array([0,1,2,3,0,1,2,3]),numpy.array([1,2,3,0,1,2,3,0]),departure,arrival,numpy.array([0,1,2,3,0,1,2,3]))
G4.build_free_edges(numpy.array([0,1,2,3]),numpy.array([1,2,3,0]),numpy.array([1,1,1,1]),numpy.array([0,1,2,3]))
print(graph)
def print_voisin(G,i):
	print("----noeud",i,"----")
	print(G[i].neighbours())

for i in range(4):
	print_voisin(G4,i)
path=G4.time_path_finder(0,3,0)
print(path)
print_path(G4,path)


print("========TEST5================BIG GRAPH=============")
n = 500
departs = []
arrivees = []
for i in range(n-1):
	for j in range(n-1):
		departs.append(j+n*i)
		departs.append(j+n*i)
		arrivees.append(j+n*(i+1))
		arrivees.append(j+1+n*i)

GG=fast_graph.graph((n+1)**2)
d = numpy.array(departs)
a = numpy.array(arrivees)
GG.build_free_edges(d,a,numpy.ones(d.size -1),numpy.ones(d.size -1))
path=GG.time_path_finder(0,2000,0)
print(path)
