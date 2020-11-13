import class_vertice_graph as cvg
import base_donnee.datas_classes as data
import numpy as np
import base_donnee.File_management as File_management
epsilon = 10**(-8)

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
    """on désanonymise le graphe en interpollant les id et noms de station avec une base de donnee idfm"""
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
        e.index = len(Graph.list_of_edges)
        ep = cvg.Edge(vp,v,ligne_liaison[i][1],cout_liaison[i][1])
        ep.connection_with_displayable = i
        ep.index = len(Graph.list_of_edges)+1
        v.push_edge(e)
        vp.push_edge(ep)
        Graph.push_vertice_without_doublons(v)
        Graph.push_vertice_without_doublons(vp)
        Graph.push_diplayable_edge(liaisons_developpes[i][1])
        Graph.push_edge(e)
        Graph.push_edge(ep)
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

def link_Montmartre_condition(vi,vj):
    if vi.gare_name=="Funiculaire Montmarte Station Basse" and vj.gare_name=="Anvers":
        return True
    if vj.gare_name=="Funiculaire Montmarte Station Basse" and vi.gare_name=="Anvers":
        return True
    return False

def link_neighboured_stations(Graph,radius):
    print("...Creating walking transfers between stations")
    s=0
    n=len(Graph.connection_table_edge_and_diplayable_edge)
    for i in range(Graph.number_of_vertices):
        for j in range(i+2,Graph.number_of_vertices):
            vi,vj=Graph[i],Graph[j]
            d=distance_metre(vi,vj)
            if (d<radius and vi.is_a_station and vj.is_a_station) or link_Montmartre_condition(vi,vj):
                ei  = cvg.Edge(vi,vj,"RER Walk",d)
                ei.connection_with_displayable = s+n
                ei.index = len(Graph.list_of_edges)
                ej = cvg.Edge(vj,vi,"RER Walk",d)
                ej.connection_with_displayable = s+n
                ej.index = len(Graph.list_of_edges)+1
                Graph[i].push_edge(ei)
                Graph[j].push_edge(ej)
                Graph.push_diplayable_edge([[vi.coordinates[0],vi.coordinates[1]],[vj.coordinates[0],vj.coordinates[1]]])
                Graph.push_edge(ei)
                Graph.push_edge(ej)
                s+=1

def load(adress="base_donnee/"):
    """Load the graph in pickle format generate by function file_management.save(G,adress)"""
    PandaV = File_management.pandas.read_pickle(adress+'datas/PandaV.pkl')
    PandaE = File_management.pandas.read_pickle(adress+'datas/PandaE.pkl')
    PandadevE = File_management.pandas.read_pickle(adress+'datas/PandadevE.pkl')
    G=cvg.Graph([])
    for i in range(PandaV['index'].count()):
        v = cvg.Vertice(index=PandaV['index'][i],coordinates=PandaV['coordinates'][i])
        v.gare_name = PandaV['gare_name'][i]
        v.color = PandaV['color'][i]
        v.is_a_station = PandaV['is_a_station'][i]
        v.id = PandaV['id'][i]
        v.index_edges_list = PandaV['index_edges_list'][i]
        G.push_vertice(v)

    for i in range(PandaE['index'].count()):
        e = cvg.Edge(vertice1=G[PandaE['index_linked[0]'][i]], vertice2=G[PandaE['index_linked[1]'][i]], id=PandaE['id'][i], given_cost=PandaE['given_cost'][i])
        e.color = PandaE['color'][i]
        e.index = PandaE['index'][i]
        e.connection_with_displayable = PandaE['connection_with_displayable'][i]
        G[PandaE['index_linked[0]'][i]].push_edge(e)
        G.push_edge(e)

    for i in range(PandadevE['connection_with_displayable'].count()):
        G.push_diplayable_edge(PandadevE['connection_table_edge_and_diplayable_edge'][i])

    return G

def load_station_names(adress="base_donnee/"):
    """returns a Panda serie of every station names """
    PandaV = File_management.pandas.read_pickle(adress+'datas/PandaV.pkl')
    return PandaV[PandaV['is_a_station']]['gare_name']#on enleve les vertices qui ne sont pas des stations

def graph_creator():
    """Function to call in order to get a graph """
    print("[loading] graph from IDFM data base...")
    G=create_half_graph_trace_ligne()
    link_with_station_data(G)
    link_neighboured_stations(G,200)
    link_with_color(G)
    print("[loading completed] : Number of vertices : " +str(G.number_of_vertices)+" Number of edges : "+str(G.number_of_edges))
    print('Exporting Graph')
    File_management.save(G,'base_donnee/')
    print('Export finished')
    return G

if __name__ == '__main__':
    G=graph_creator()
    #G=load()
    #L=load_station_names()
