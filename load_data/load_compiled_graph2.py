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

exceptions.check_compiled_graph_version("0.0.4")


import pandas
import numpy as np
import datetime

if os.path.exists(parentdir+"/base_donnee/datas/graph_files")==False:
    os.makedirs(parentdir+"/base_donnee/datas/graph_files")

if input("Do you want to update graph (15min approx)? y/n ") == "y" :
    import load_data.data_to_graph_gtfs_2

try :
    print("reading pickle files")
    PandaE=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_E.pkl")
    PandaV=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_V.pkl")
    PandaDisp=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_PandaDisp.pkl")
    PandaC=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Color.pkl")
    PandaEf=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Ef.pkl")
    station_names=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/station_name.pkl").to_list()
except :
    if input("can't read pickle files, do you want to re-create graph ? (15min approx) y/n" )=="y":
        import load_data.data_to_graph_gtfs_2
        print("reading pickle files")
        PandaE=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_E.pkl")
        PandaV=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_V.pkl")
        PandaDisp=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_PandaDisp.pkl")
        PandaC=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Color.pkl")
        PandaEf=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/2gtfs_Ef.pkl")
        station_names=pandas.read_pickle(parentdir+"/base_donnee/datas/graph_files/station_name.pkl").to_list()
    else :
        exit(2)



def load_graph(scheduled_edges = PandaE ,free_edges = PandaEf , size = PandaV["station_name"].size) :
    Graph = fg.graph(size)
    Graph.build_scheduled_edges_string(scheduled_edges['departure_stop_index'].to_numpy(),scheduled_edges['arrival_stop_index'].to_numpy(),scheduled_edges["departure_time"].to_numpy(),scheduled_edges["arrival_time"].to_numpy(),scheduled_edges.index.to_numpy())
    Graph.build_free_edges(free_edges['departure_stop_index'].to_numpy(),free_edges['arrival_stop_index'].to_numpy(),free_edges["min_transfer_time"].to_numpy())
    return Graph
