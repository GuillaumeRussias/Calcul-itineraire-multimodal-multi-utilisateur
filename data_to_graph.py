import class_vertice_graph as cvg
import base_donnee.datas_classes as data
epsilon=10**(-3)
print("epsilon",epsilon)

def put_edge(index_gare,mission,Graph,name,color):
    gare=mission[index_gare]
    garep=mission[index_gare+1]
    v=cvg.Vertice(0,(gare[0],gare[1]))
    vp=cvg.Vertice(0,(garep[0],garep[1]))
    e=cvg.Edge(v,vp,name)
    ep=cvg.Edge(vp,v,name)
    e.color=color
    ep.color=color
    v.color=color
    vp.color=color
    v.push_edge(e)
    vp.push_edge(ep)
    Graph.push_vertice_without_doublons(v)
    Graph.push_vertice_without_doublons(vp)

def create_half_graph_gtfs(adress_gtfs="base_donnee/datas/lignes-gtfs.json"):
    lignes_gtfs=data.lignes_gtfs(adress_gtfs)
    coords,line_names,line_colors,line_types=lignes_gtfs.get_important_data()
    #Coord_gares[i][1]=Ensemble des missions de la ligne i
    #Ensemble de missions[j]= Enemble des coordonnees gares deservies dans l ordre par la mission j
    Graph=cvg.Graph([])
    for index_ligne in range(len(line_names)):
        ligne=coords[index_ligne][1]
        name=line_names[index_ligne][1]
        color=line_colors[index_ligne][1]
        for mission in ligne:
            for index_gare in range(0,len(mission)-1):
                put_edge(index_gare,mission,Graph,name,color)
    return Graph

def get_index_of_optimal_station(vertice,coords,type_cost=cvg.Edge.square_euclidian_cost):
    v=cvg.Vertice(0,(coords[0][1][0],coords[0][1][1]))
    e=cvg.Edge(v,vertice,0)
    min=type_cost(e)
    i_min=0
    for index in range(1,len(coords)):
        v=cvg.Vertice(0,(coords[index][1][0],coords[index][1][1]))
        e=cvg.Edge(v,vertice,0)
        d=type_cost(e)
        if min>d:
            min=d
            i_min=index
    return i_min,min

def link_with_station_data(half_Graph,adress_station="base_donnee/datas/Referenciel_gares/emplacement-des-gares-idf.json"):
    referentiel_gares=data.emplacement_gares(adress_station)
    coords,id,names=referentiel_gares.get_important_data()
    for i in range(half_Graph.number_of_vertices):
        i_min,min=get_index_of_optimal_station(half_Graph[i],coords)
        half_Graph[i].gare_name=names[i_min][1]
        half_Graph[i].id=id[i_min][1]
        half_Graph[i].index=i
        if min>epsilon:
            print(half_Graph[i].gare_name,half_Graph[i].get_lines_connected(),half_Graph[i].coordinates)



G=create_half_graph_gtfs()
link_with_station_data(G)
G.plot()
