import folium
import flask
import data_to_graph as buildGraph

#Utilise Flask et Folium pour afficher sur navigateur une carte d'idf avec son reseau ferre


G=buildGraph.create_half_graph_trace_ligne()
buildGraph.link_with_station_data(G)
buildGraph.link_with_color(G)

Line_to_display=["A","B","C","D","E"]#pas encore implemente


map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)

def change_convention(G):
    for dev_edge in G.connection_table_edge_and_diplayable_edge:
        for h in range(len(dev_edge)):
            a=dev_edge[h][0]
            dev_edge[h][0]=dev_edge[h][1]
            dev_edge[h][1]=a

def plot_part_of_graph(map,Line_to_display,G):
    change_convention(G)
    rad=40
    for v in G:
        c = f"#{v.color}"
        x = v.coordinates[1]
        y = v.coordinates[0]
        folium.Circle(radius=rad,location=[x,y],popup=v.gare_name,color=c,fill_color=c,fill_opacity=0.8,fill=True).add_to(map)
        for e in v.edges_list:
            c = f"#{e.color}"
            folium.PolyLine(G.connection_table_edge_and_diplayable_edge[e.connection_with_displayable],color=c,opacity=0.6).add_to(map)

plot_part_of_graph(map,Line_to_display,G)

app = flask.Flask(__name__)

@app.route('/')
def plot_on_web():
 return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
