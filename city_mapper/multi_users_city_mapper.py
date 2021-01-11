import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import load_data.load_compiled_graph2 as load_graph
#import load_data.load_compiled_graph as load_graph
import display_on_map.Display_compiled as display
import folium
import flask
import numpy as np


print("importing")
heure_debut = 3600 *16 #10h


def find_index_station_name(name,PandaV=load_graph.PandaV):
    research=PandaV[PandaV["station_name"].map(lambda c:c==name)]
    return research.index[0]


print("building graph")
graph = load_graph.load_graph()

#N utilisateurs

N = 2

start_indexes = np.zeros((N,), dtype=int)
for i in range (N):
    start_indexes[i] = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
    print(start_indexes[i])


print("applying path finder")

best_end_index = graph.multi_users_dijkstra(start_indexes,heure_debut)

print(best_end_index)

print(graph.time_path_finder(15189,6120,heure_debut))

"""path = np.zeros(N)
for i in range(N):
    path[i] = graph.time_path_finder(start_indexes[i],best_end_index,heure_debut)

print("==============================")
for i in range (N):
    print("From",load_graph.PandaV["station_name"][i],"to",load_graph.PandaV["station_name"][best_end_index])
    dep = display.seconds_to_hours(graph[path[i][0]].time())
    arr = display.seconds_to_hours(graph[path[i][-1]].time())
    print("Departure time =",dep,"| Arrival time =",arr)
    print("------")
print("==============================")

map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=11)


#map = display.plot_traject(FoliumMap = map , VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , DisplayFer = load_graph.PandaDisp_edges , DisplayBus = load_graph.PandaDisp_edgesBus , LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )
map = display.plot_traject2(FoliumMap = map , VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )

app2 = flask.Flask(__name__)
if __name__ == '__main__':
    @app2.route('/')
    def plot_on_web():
        return map._repr_html_()
    app2.run(debug=False)"""
