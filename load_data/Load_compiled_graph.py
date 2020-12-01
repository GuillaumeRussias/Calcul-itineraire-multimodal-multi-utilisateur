import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)



try :
    import fast_graph as fg
except :
    print("compiled graph library is not installed")

import pandas
import numpy as np
import datetime


print("read_pickle")
adress=parentdir+"/base_donnee/datas/graph_files/"
PandaE=pandas.read_pickle(adress+"gtfs_E.pkl")
PandaV=pandas.read_pickle(adress+"gtfs_V.pkl")
PandaDisp_edges=pandas.read_pickle(adress+"gtfs_PandaDispEdges.pkl")
PandaDisp_edgesBus=pandas.read_pickle(adress+"gtfs_PandaDispEdgesBus.pkl")
PandaC=pandas.read_pickle(adress+"gtfs_Color.pkl")
transferts=pandas.read_pickle(adress+"gtfs_transferts.pkl")


print("convert seconds")
PandaE["departure_time"]=PandaE["departure_time"].map(lambda hhmmss : 3600*int(hhmmss[0:2])+60*int(hhmmss[3:5])+int(hhmmss[6:8]))
PandaE["arrival_time"]=PandaE["arrival_time"].map(lambda hhmmss : 3600*int(hhmmss[0:2])+60*int(hhmmss[3:5])+int(hhmmss[6:8]))

print("graph creation")
G=fg.graph(PandaV["gtfs_id"].size)
print("scheduled")
G.build_scheduled_edges(PandaE['departure_stop_index'].to_numpy(),PandaE['arrival_stop_index'].to_numpy(),PandaE["departure_time"].to_numpy(),PandaE["arrival_time"].to_numpy(),PandaE.index.to_numpy())
print("free")
G.build_free_edges(transferts['from_stop_id'].to_numpy(),transferts['to_stop_id'].to_numpy(),transferts["min_transfer_time"].to_numpy(),transferts.index.to_numpy())
print("path_finder")
path=G.time_path_finder(0,300,3600*15)
print(path)
