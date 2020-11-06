import class_vertice_graph as cvg
import base_donnee.datas_classes as data
import numpy as np
epsilon = 10**(-8)

#old
"""
def put_edge(index_gare, mission, Graph, name, color,index):
    Fonction appelee par create_half_graph_gtfs, on les separe pour plus de lisibilite mais elles forment un tout
    gare = mission[index_gare]
    garep = mission[index_gare+1]
    v = cvg.Vertice(index,(gare[0],gare[1]))
    vp = cvg.Vertice(index,(garep[0],garep[1]))
    e = cvg.Edge(v,vp,name)
    ep = cvg.Edge(vp,v,name)
    e.color = color
    ep.color = color
    v.color = color
    vp.color = color
    v.push_edge(e)
    vp.push_edge(ep)
    if Graph.push_vertice_without_doublons(v): #il y'a eu push ,on incrémente index
        index+=1
    Graph[-1].index=len(Graph)-1
    if Graph.push_vertice_without_doublons(vp): #il y'a eu push ,on incrémente index
        index+=1
    Graph[-1].index=len(Graph)-1
    return index
#old
def create_half_graph_gtfs(adress_gtfs="base_donnee/datas/lignes-gtfs.json"):
    Utilise la base de donnee gtfs pour cree un graph de vertices anonymes relies entre eux selon les donnees de la base
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
                put_edge(index_gare, mission, Graph, name, color,0)
    return Graph
"""
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
    print("...naming annonymous edges and vertices with safe interpolation on coords (epsilon = " +str(epsilon)+")")
    referentiel_gares = data.emplacement_gares(adress_station)
    coords, id, names = referentiel_gares.get_important_data()
    for i in range(anonymous_Graph.number_of_vertices):
        i_min,min = get_index_of_optimal_station(anonymous_Graph[i], coords)
        anonymous_Graph[i].gare_name = names[i_min][1]
        anonymous_Graph[i].id = id[i_min][1]
        anonymous_Graph[i].index = i
        if min > epsilon: #tolerance du minimum
            anonymous_Graph[i].is_a_station = False
            anonymous_Graph[i].gare_name = anonymous_Graph[i].gare_name + ": Not a station but a vertex near it"
            #print("Fourche detectee",anonymous_Graph[i].gare_name, anonymous_Graph[i].get_lines_connected(), anonymous_Graph[i].coordinates, min)
    anonymous_Graph.set_right_edges()

def create_half_graph_trace_ligne(adress_ligne="base_donnee/datas/traces-du-reseau-ferre-idf.json"):
    print("...Extracting annonymous edges and vertices")
    lignes=data.trace_lignes_idf(adress_ligne)
    liaisons_developpes,cout_liaison,ligne_liaison=lignes.get_important_data()
    Graph = cvg.Graph([])
    for i in range (len(liaisons_developpes)):
        v  = cvg.Vertice(0,liaisons_developpes[i][1][0])
        vp = cvg.Vertice(0,liaisons_developpes[i][1][-1])
        e  = cvg.Edge(v,vp,ligne_liaison[i][1],cout_liaison[i][1])
        e.connection_with_displayable = i
        ep = cvg.Edge(vp,v,ligne_liaison[i][1],cout_liaison[i][1])
        ep.connection_with_displayable = i
        v.push_edge(e)
        vp.push_edge(ep)
        Graph.push_vertice_without_doublons(v)
        Graph.push_vertice_without_doublons(vp)
        Graph.push_diplayable_edge(liaisons_developpes[i][1])
    #Graph.plot_dev()
    return Graph

def distance_metre(v1,v2):
    #conversion
    x1 , x2 = v1.coordinates[0]*73340 , v2.coordinates[0]*73340
    y1 , y2 = v1.coordinates[1]*111300 , v2.coordinates[1]*111300
    d = (x1-x2)**2 + (y1-y2)**2
    return np.sqrt(d)

def link_with_color(Graph,adress_color="base_donnee/datas/referentiel-des-lignes.json"):
    print("...Coloring stations and lines")
    donnees= data.referenciel_lignes(adress_color)
    dict_nom_color=donnees.get_color_and_name()
    dict_nom_color["RER Walk"]='708090'
    for v in Graph:
        nom=v.get_lines_connected()[0]
        v.color=dict_nom_color[nom]
        for e in v.edges_list:
            nom=e.id
            e.color=dict_nom_color[nom]




def link_neighboured_stations(Graph,radius):
    print("...Creating walking transfers between stations")
    s=0
    n=len(Graph.connection_table_edge_and_diplayable_edge)
    assert(n==Graph.number_of_edges)
    for i in range(Graph.number_of_vertices):
        for j in range(i+2,Graph.number_of_vertices):
            vi,vj=Graph[i],Graph[j]
            d=distance_metre(vi,vj)
            if d<radius and vi.is_a_station and vj.is_a_station:
                ei  = cvg.Edge(vi,vj,"RER Walk",d*4)
                ei.connection_with_displayable = s+n
                ej = cvg.Edge(vj,vi,"RER Walk",d*4)
                ej.connection_with_displayable = s+n
                Graph[i].push_edge(ei)
                Graph[j].push_edge(ej)
                Graph.push_diplayable_edge([[vi.coordinates[0],vi.coordinates[1]],[vj.coordinates[0],vj.coordinates[1]]])
                s+=1




def graph_creator():
    """Function to call in order to get a graph """
    print("[loading] graph from IDFM data base...")
    G=create_half_graph_trace_ligne()
    link_with_station_data(G)
    link_neighboured_stations(G,200)
    link_with_color(G)
    print("[loading completed] : Number of vertices : " +str(G.number_of_vertices)+" Number of edges : "+str(G.number_of_edges))
    return G
