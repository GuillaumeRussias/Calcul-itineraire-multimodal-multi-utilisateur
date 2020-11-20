import load_gtfs_graph
import Display_gtfs
import folium
import flask
import networkx as nx
import datetime


Graph,PandaV,PandaDisp_edges,PandaC=load_gtfs_graph.load_graph(adress="base_donnee/datas/graph_files/",date_debut=datetime.datetime.now(),limitation_horaire="03:00:00")

def find_index_station_name(name,PandaV=PandaV,):
    research=PandaV[PandaV["station_name"].map(lambda c:c==name)]
    return research.index[0]

i = find_index_station_name("GARE DE ST REMY LES CHEVREUSE")
j = find_index_station_name("GARE DE NOISY CHAMPS")

path=nx.shortest_path(Graph,source=i,target=j)

map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)

map = Display_gtfs.plot_traject_folium(map,path,PandaV,PandaDisp_edges,PandaC,Graph)

app2 = flask.Flask(__name__)
if __name__ == '__main__':
    @app2.route('/')
    def plot_on_web():
     return map._repr_html_()
    app2.run(debug=False)
