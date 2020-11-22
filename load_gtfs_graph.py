import pandas
import numpy as np
import networkx as nx
import datetime

Adress="base_donnee/datas/graph_files/"

def convert_in_date_time(hhmmss,start_day):
    #hhmmss string format hh:mm:ss
    return start_day+datetime.timedelta(hours=int(hhmmss[0:2]),minutes=int(hhmmss[3:5]),seconds=int(hhmmss[6:8]))

def PandaE_time_limitation(date_debut,PandaE,hhmmss="03:00:00"):
    start_day=date_debut.replace(hour=0,minute=0,second=0)
    PandaE=PandaE[PandaE["departure_time"].map(lambda c:convert_in_date_time(c,start_day)>=date_debut)]
    PandaE=PandaE[PandaE["departure_time"].map(lambda c:convert_in_date_time(c,start_day)<=convert_in_date_time(hhmmss,date_debut))]
    return PandaE

def time_cost(departure_time,arrival_time,start_day):
    return (convert_in_date_time(arrival_time,start_day)-convert_in_date_time(departure_time,start_day)).total_seconds()


def load_graph(adress,date_debut,limitation_horaire):
    start_day=date_debut.replace(hour=0,minute=0,second=0)

    PandaE=pandas.read_pickle(adress+"gtfs_E.pkl")
    PandaV=pandas.read_pickle(adress+"gtfs_V.pkl")
    PandaDisp_edges=pandas.read_pickle(adress+"gtfs_PandaDispEdges.pkl")
    PandaDisp_edgesBus=pandas.read_pickle(adress+"gtfs_PandaDispEdgesBus.pkl")
    PandaC=pandas.read_pickle(adress+"gtfs_Color.pkl")
    transferts=pandas.read_pickle(adress+"gtfs_transferts.pkl")

    PandaE=PandaE_time_limitation(date_debut,PandaE,hhmmss=limitation_horaire)
    G = nx.MultiDiGraph()
    n=0
    for i in PandaE.index:
        cost = np.int(time_cost(PandaE["departure_time"][i],PandaE["arrival_time"][i],start_day))
        G.add_edge(PandaE['departure_stop_index'][i],PandaE['arrival_stop_index'][i],weight=cost,departure_time=PandaE["departure_time"][i],arrival_time=PandaE["arrival_time"][i],route_id=PandaE["route_id"][i],list_of_disp_edge_index=PandaE["list_of_disp_edge_index"][i],disp_edge_index_bus=PandaE["disp_edge_index_bus"][i],type="common")
    for i in transferts.index:
        cost = np.int(transferts["min_transfer_time"][i])
        G.add_edge(transferts['from_stop_id'][i],transferts['to_stop_id'][i],weight=cost,type="walk")

    return G,PandaV,PandaDisp_edges,PandaC,PandaDisp_edgesBus


if __name__ == '__main__':
    load_graph(Adress,datetime.datetime.now(),limitation_horaire="03:00:00")
