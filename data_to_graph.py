import class_vertice_graph as cvg
import base_donnee.datas_classes as data
epsilon = 10**(-3)
print("epsilon", epsilon)

def put_edge(index_gare, mission, Graph, name, color):
    """Fonction appelee par create_half_graph_gtfs, on les separe pour plus de lisibilite mais elles forment un tout """
    gare = mission[index_gare]
    garep = mission[index_gare+1]
    v = cvg.Vertice(0,(gare[0],gare[1]))
    vp = cvg.Vertice(0,(garep[0],garep[1]))
    e = cvg.Edge(v,vp,name)
    ep = cvg.Edge(vp,v,name)
    e.color = color
    ep.color = color
    v.color = color
    vp.color = color
    v.push_edge(e)
    vp.push_edge(ep)
    Graph.push_vertice_without_doublons(v)
    Graph.push_vertice_without_doublons(vp)

def create_half_graph_gtfs(adress_gtfs="base_donnee/datas/lignes-gtfs.json"):
    """Utilise la base de donnee gtfs pour cree un graph de vertices anonymes relies entre eux selon les donnees de la base """
    lignes_gtfs = data.lignes_gtfs(adress_gtfs)
    coords, line_names, line_colors, line_types = lignes_gtfs.get_important_data()
    #Coord_gares[i][1]=Ensemble des missions de la ligne i
    #Ensemble de missions[j]= Enemble des coordonnees gares deservies dans l ordre par la mission j
    Graph = cvg.Graph([])
    for index_ligne in range(len(line_names)):
        ligne = coords[index_ligne][1]
        name = line_names[index_ligne][1]
        color = line_colors[index_ligne][1]
        for mission in ligne:
            for index_gare in range(0, len(mission)-1):
                put_edge(index_gare, mission, Graph, name, color)
    return Graph

def get_index_of_optimal_station(vertice,coords,type_cost=cvg.Edge.square_euclidian_cost):
    """Pour enlenver l'anonymat de vertice, on cherche parmis coords le point le plus proche selon type_cost, et on retourn l'indice et la valeur de l'optimum """
    v = cvg.Vertice(0, (coords[0][1][0], coords[0][1][1]))
    e = cvg.Edge(v,vertice,0)
    min = type_cost(e)
    i_min = 0
    for index in range(1, len(coords)):
        v = cvg.Vertice(0,(coords[index][1][0], coords[index][1][1]))
        e = cvg.Edge(v,vertice,0)
        d = type_cost(e)
        if min > d:
            min = d
            i_min = index
    return i_min, min

def link_with_station_data(anonymous_Graph, adress_station="base_donnee/datas/Referenciel_gares/emplacement-des-gares-idf.json"):
    """on déshanonymise le graph en interpollant les id et noms de station avec une base de donnee idfm"""
    referentiel_gares = data.emplacement_gares(adress_station)
    coords, id, names = referentiel_gares.get_important_data()
    for i in range(anonymous_Graph.number_of_vertices):
        i_min,min = get_index_of_optimal_station(anonymous_Graph[i], coords)
        anonymous_Graph[i].gare_name = names[i_min][1]
        anonymous_Graph[i].id = id[i_min][1]
        anonymous_Graph[i].index = i
        if min > epsilon: #tolerance du minimum
            print(anonymous_Graph[i].gare_name, anonymous_Graph[i].get_lines_connected(), anonymous_Graph[i].coordinates)



G = create_half_graph_gtfs()
link_with_station_data(G)
G.plot()
