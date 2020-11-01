import class_vertice_graph as cvg
import base_donnee.datas_classes as data






def create_half_graph_gtfs(adress_gtfs="base_donnee/datas/lignes-gtfs.json"):
    lignes_gtfs=data.lignes_gtfs(adress_gtfs)
    coords,line_names,line_colors,line_types=lignes_gtfs.get_important_data()
    #Coord_gares[i][1]=Enemble de missions de la ligne i
    #Ensemble de missions[j]= Enemble des coordonnees gares deservies dans l ordre par la mission j
    Graphique=cvg.Graph([])
    for index_ligne in range(len(line_names)):
        ligne=coords[index_ligne][1]
        name=line_names[index_ligne][1]
        color=line_colors[index_ligne][1]
        for mission in ligne:
            for index_gare in range(0,len(mission)-1):
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
                Graphique.push_vertice_without_doublons(v)
                Graphique.push_vertice_without_doublons(vp)

    Graphique.plot()

create_half_graph_gtfs()
