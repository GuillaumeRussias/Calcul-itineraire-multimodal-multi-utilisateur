import data_to_graph as buildGraph
import Display
import dijkstra_1_user_adapté as Dj #Beaucoup trop lent ou alors ne converge pas ?
import flask
import folium
import shortest_path as path #fonctionne tres bien (blibliotheque scipy.csgraph)
import homemade_shortest_path as hpath #Beaucoup trop lent ou alors ne converge pas ?
import class_vertice_graph as cvg

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
    G=buildGraph.graph_creator()
    i=find_gare(G,"NOISY-CHAMPS")
    j=266

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
    app2.run(debug=True)
