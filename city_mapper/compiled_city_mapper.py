import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import load_data.load_compiled_graph2 as load_graph
#import load_data.load_compiled_graph as load_graph
import display_on_map.Display_compiled as display
import display_on_map.Display_geojson as geo
import folium
import numpy as np
import geojson
import time



print("importing")
#heure_debut = 3600 *23 #10h


def find_index_station_name(name,PandaV=load_graph.PandaV):
    research=PandaV[PandaV["station_name"].map(lambda c:c==name)]
    return research.index[0]



print("building graph")
graph = load_graph.load_graph()
n=0

# cout moyen DJ sur instance complète, le code C++ lourd (if et assert en trop) = 0.02 s , ordinateur sur batterie.
T = time.time()
while n<1000 :
    j = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
    i = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
    h = np.random.randint(low=0, high=3600*24)
    #i = 32608
    #j = 27509
    #h= 8*3600

    #i = find_index_station_name("Olympiades")
    #j = find_index_station_name("Mairie de Saint-Ouen")

    #i = 29733
    #j = 1582

    #24926 arret ponts et chausées à ... Versailles

    print("applying path finder")
    print("==============================")
    print(i,j)
    print("From",load_graph.PandaV["station_name"][i],"to",load_graph.PandaV["station_name"][j])
    T = time.time()
    try :
        path = graph.complete_time_changement_path_finder(i,j,h)
        TT = time.time()
        dep = display.seconds_to_hours(graph[path[0]].time())
        arr = display.seconds_to_hours(graph[path[-1]].time())
        print("Departure time =",dep,"| Arrival time =",arr)
        print("temps d'execution :", TT-T,"(s)")
        print("==============================")
        T = time.time()
        path2 = graph.complete_time_path_finder(i,j,h)
        TT = time.time()
        dep = display.seconds_to_hours(graph[path[0]].time())
        arr = display.seconds_to_hours(graph[path[-1]].time())
        print("Departure time =",dep,"| Arrival time =",arr)
        print("temps d'execution :", TT-T,"(s)")
        print("==============================")
        """for i in range(len(path)-1):
            graph[path[i]][path[i+1]].print_missions()
            print(graph[path[i]][path[i+1]].get_selected_trip_id())
            print("===============")"""
    except :
        TT = time.time()
        print("path not found")
        print("temps d'execution :", TT-T,"(s)")






"""j = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
i = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)"""

i = 15189
j = 6100

print("applying path finder")


path = graph.time_path_finder(i,j,heure_debut)

    #map = folium.Map(
    #lat lon folium inversee avec idfm
        #location=(48.852186, 2.339754),
        #tiles='CartoDB positron',
        #zoom_start=11)


    #map = display.plot_traject(FoliumMap = map , VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , DisplayFer = load_graph.PandaDisp_edges , DisplayBus = load_graph.PandaDisp_edgesBus , LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )
    #map = display.plot_traject2(FoliumMap = map , VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )
    try :
        geo_features = geo.geojson_traject(VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )
        a=geojson.dumps(geo_features)
        file = open("result_city_mapper.js","w")
        file.write("var traject = ")
        file.write(a)
        file.close()
    except:
        "no path found"
    n+=1
    input()



#map = geo.map_from_geojson(geo_features, map)
