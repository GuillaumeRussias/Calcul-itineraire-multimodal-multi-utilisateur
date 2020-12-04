import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import exceptions




try :
    import fast_graph as fg
except :
    print("compiled graph library is not installed : please install it with pip install ./compiled_graph")
    exit(2)

exceptions.check_compiled_graph_version("0.0.2")


import pandas
import numpy as np
import datetime

try :
    print("reading pickle files")
    adress=parentdir+"/base_donnee/datas/graph_files/"
    PandaE=pandas.read_pickle(adress+"gtfs_E.pkl")
    PandaV=pandas.read_pickle(adress+"gtfs_V.pkl")
    PandaDisp_edges=pandas.read_pickle(adress+"gtfs_PandaDispEdges.pkl")
    PandaDisp_edgesBus=pandas.read_pickle(adress+"gtfs_PandaDispEdgesBus.pkl")
    PandaC=pandas.read_pickle(adress+"gtfs_Color.pkl")
    transferts=pandas.read_pickle(adress+"gtfs_transferts.pkl")
except :
    print("can't read pickle files, do you want to re-create it ? (15min approx) [y]/n")
    if input()=="y":
        import load_data.data_to_graph_gtfs
        print("reading pickle files")
        adress=parentdir+"/base_donnee/datas/graph_files/"
        PandaE=pandas.read_pickle(adress+"gtfs_E.pkl")
        PandaV=pandas.read_pickle(adress+"gtfs_V.pkl")
        PandaDisp_edges=pandas.read_pickle(adress+"gtfs_PandaDispEdges.pkl")
        PandaDisp_edgesBus=pandas.read_pickle(adress+"gtfs_PandaDispEdgesBus.pkl")
        PandaC=pandas.read_pickle(adress+"gtfs_Color.pkl")
        transferts=pandas.read_pickle(adress+"gtfs_transferts.pkl")
    else :
        exit(2)

"""
print("convert in seconds")
PandaE["departure_time"]=PandaE["departure_time"].map(lambda hhmmss : 3600*int(hhmmss[0:2])+60*int(hhmmss[3:5])+int(hhmmss[6:8]))
PandaE["arrival_time"]=PandaE["arrival_time"].map(lambda hhmmss : 3600*int(hhmmss[0:2])+60*int(hhmmss[3:5])+int(hhmmss[6:8]))
"""

def load_graph(scheduled_edges = PandaE ,free_edges = transferts , size = 0) :
    Graph = fg.graph(size)
    Graph.build_scheduled_edges_string(scheduled_edges['departure_stop_index'].to_numpy(),scheduled_edges['arrival_stop_index'].to_numpy(),scheduled_edges["departure_time"].to_numpy(),scheduled_edges["arrival_time"].to_numpy(),scheduled_edges.index.to_numpy())
    Graph.build_free_edges(free_edges['from_stop_id'].to_numpy(),free_edges['to_stop_id'].to_numpy(),free_edges["min_transfer_time"].to_numpy())
    return Graph
