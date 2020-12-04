import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


import load_data.load_compiled_graph as load_graph
import display_on_map.Display_compiled as display
import folium
import flask


print("importing")
heure_debut = 3600 *19 #19h


def find_index_station_name(name,PandaV=load_graph.PandaV):
    research=PandaV[PandaV["station_name"].map(lambda c:c==name)]
    return research.index[0]

i = find_index_station_name("Beauplan")
#i = 5884
j = find_index_station_name("GARE DE NOISY CHAMPS")

#i = 10000
#j = 20000 #resultats bizarres


print("building graph")
graph = load_graph.load_graph()
print("applying path finder")
path = graph.time_path_finder(i,j,heure_debut)
print("")
print("displaying traject")


map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)


map = display.plot_traject(FoliumMap = map , VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , DisplayFer = load_graph.PandaDisp_edges , DisplayBus = load_graph.PandaDisp_edgesBus , LineData = load_graph.PandaC, Path = path , CompiledGraph = graph )


app2 = flask.Flask(__name__)
if __name__ == '__main__':
    @app2.route('/')
    def plot_on_web():
     return map._repr_html_()
    app2.run(debug=False)
