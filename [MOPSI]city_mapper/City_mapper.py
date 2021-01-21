
#DEPRECIATED - not used by final programm

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)




import load_data.data_to_graph as buildGraph
import display_on_map.Display as Display
import python_graph.dijkstra_1_user_adapté as Dj #Beaucoup trop lent ou alors ne converge pas ?
import flask
import folium
import python_graph.shortest_path as path #fonctionne tres bien (blibliotheque scipy.csgraph)
import python_graph.homemade_shortest_path as hpath #Beaucoup trop lent ou alors ne converge pas ?
import python_graph.class_vertice_graph as cvg

map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)


app2 = flask.Flask(__name__)
def find_gare(G,gare):
    for v in G :
        if v.is_a_station and v.gare_name==gare:
            return v.index

if __name__ == '__main__':
    G=buildGraph.load()
    i=find_gare(G,"La Défense - Grande Arche")
    j=find_gare(G,"Louise Michel")
    #find_gare(G,"Mairie de Saint-Ouen: Not a station but a vertex near it")

    print("finding traject",G[i].gare_name , "to", G[j].gare_name)
    A=G.A_matrix(type_cost=cvg.Edge.customized_cost1)
    path=path.path_finder(A, i, j)
    #path=hpath.Homemade_path_finder(A, i, j)
    #path=Dj.Homemade_path_finder(G, i, j)

    for i in path:
        print(G[i].gare_name)

    Display.plot_a_course(map,path,G)


    @app2.route('/')
    def plot_on_web():
     return map._repr_html_()
    app2.run(debug=False)
