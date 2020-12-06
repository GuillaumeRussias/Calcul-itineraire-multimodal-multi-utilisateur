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

j = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
i = np.random.randint(low=0, high=load_graph.PandaV["station_name"].size-1)
print("applying path finder")

path = graph.time_path_finder(i,j,heure_debut)

print("==============================")
print("From",load_graph.PandaV["station_name"][i],"to",load_graph.PandaV["station_name"][j])
dep = display.seconds_to_hours(graph[path[0]].time())
arr = display.seconds_to_hours(graph[path[-1]].time())
print("Departure time =",dep,"| Arrival time =",arr)
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
    app2.run(debug=False)
