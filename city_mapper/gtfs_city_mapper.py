import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)




import load_data.load_gtfs_graph as load_gtfs_graph
import display_on_map.Display_gtfs as Display_gtfs
import folium
import flask
import networkx as nx
import datetime

print("importing")
date_debut=datetime.datetime.now()
date_debut=date_debut.replace(hour=15,minute=0,second=0)
Graph,PandaV,PandaDisp_edges,PandaC,PandaDisp_edgesBus=load_gtfs_graph.load_graph(adress=parentdir+"/base_donnee/datas/graph_files/",date_debut=date_debut,limitation_horaire="03:00:00")

def find_index_station_name(name,PandaV=PandaV,):
    research=PandaV[PandaV["station_name"].map(lambda c:c==name)]
    return research.index[0]

i = find_index_station_name("LYCEE MONOD")
j = find_index_station_name("Gare de Versailles Chantiers Gare Routière")
h = find_index_station_name("Hauts de Chevreuse")


path=nx.shortest_path(Graph,source=h,target=j,weight="weight")


map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)

#map = Display_gtfs.plot_traject_folium(map,path,PandaV,PandaDisp_edges,PandaC,Graph)
map = Display_gtfs.plot_traject_folium2(map,path,PandaV,PandaDisp_edges,PandaC,Graph,PandaDisp_edgesBus,date_debut)


app2 = flask.Flask(__name__)
if __name__ == '__main__':
    @app2.route('/')
    def plot_on_web():
     return map._repr_html_()
    app2.run(debug=False)
