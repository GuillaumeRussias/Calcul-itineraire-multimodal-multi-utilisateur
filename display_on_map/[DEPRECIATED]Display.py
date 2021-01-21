

#DEPRECIATED - not used by final programm

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)



import folium
import flask
import load_data.data_to_graph as buildGraph

#Utilise Flask et Folium pour afficher sur navigateur une carte d'idf avec son reseau ferre
app = flask.Flask(__name__)




map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)

def change_convention(G):#(x,y)=(y,x)
    for dev_edge in G.connection_table_edge_and_diplayable_edge:
        for h in range(len(dev_edge)):
            dev_edge[h][0],dev_edge[h][1] = dev_edge[h][1],dev_edge[h][0]

def condition_station_display(vertex,Line_to_display,Skip=True):
    """return a boolean which tells if the station should be displayed or no """
    if Skip:
        return vertex.is_a_station
    for nom_de_ligne in vertex.get_lines_connected():
        if nom_de_ligne in Line_to_display:
            return vertex.is_a_station
    return False

def condition_edge_display(edge,Line_to_display,Skip=True):
    """return a boolean which tells if the station should be displayed or no """
    if Skip:
        return True
    return edge.id in Line_to_display

def plot_part_of_graph(map,Line_to_display,G,Skip=True):
    change_convention(G)
    rad=40
    w=5
    for v in G:
        for e in v.edges_list:
            if condition_edge_display(e,Line_to_display,Skip):
                c = f"#{e.color}"
                line = G.connection_table_edge_and_diplayable_edge[e.connection_with_displayable]
                folium.PolyLine(line,color=c,weight=w,popup=e.id,opacity=0.6).add_to(map)
        if condition_station_display(v,Line_to_display,Skip):
            c = f"#{v.color}"
            x = v.coordinates[1]
            y = v.coordinates[0]
            nom=v.gare_name+" "+str(v.index)
            folium.Circle(radius=rad,location=[x,y],popup=nom,color=c,fill_color=c,fill_opacity=0.8,fill=True).add_to(map)



def get_edge_bewteen_vertices(v1,v2,id_prec):
    for e in v1.edges_list:
        if e.linked[1].index==v2.index and e.id==id_prec:
            return e
    for e in v1.edges_list:
        if e.linked[1].index==v2.index:
            return e
    print("pas de lien trouve entre v1 et v2")
    #raise(ValueError("pas de lien trouve entre v1 et v2"))


def plot_a_course(map,index_of_vertice_in_right_order,G):
    rad=20
    w=5
    id_prec=0
    change_convention(G)
    for i in range(len(index_of_vertice_in_right_order)-1):
        index = index_of_vertice_in_right_order[i]
        indexp = index_of_vertice_in_right_order[i+1]
        edge = get_edge_bewteen_vertices(G[index],G[indexp],id_prec)
        id_prec = edge.id
        developped_edge = G.connection_table_edge_and_diplayable_edge[edge.connection_with_displayable]
        c = f"#{edge.color}"
        x = G[index].coordinates[1]
        y = G[index].coordinates[0]
        xp = G[indexp].coordinates[1]
        yp = G[indexp].coordinates[0]
        nom = G[index].gare_name
        nomp = G[indexp].gare_name
        folium.PolyLine(developped_edge,color=c,weight=w,popup=edge.id,opacity=1).add_to(map)
        if G[index].is_a_station:
            folium.Circle(radius=rad,location=[x,y],popup=nom,color=c,fill_color=c,fill_opacity=0.8,fill=True).add_to(map)
            folium.Circle(radius=rad-7,location=[x,y],popup=nom,color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(map)
        if G[indexp].is_a_station:
            folium.Circle(radius=rad,location=[xp,yp],popup=nomp,color=c,fill_color=c,fill_opacity=0.8,fill=True).add_to(map)
            folium.Circle(radius=rad-7,location=[xp,yp],popup=nomp,color="WHITE",fill_color="WHITE",fill_opacity=0.9,fill=True).add_to(map)







@app.route('/')
def plot_on_web():
 return map._repr_html_()

if __name__ == '__main__':
    G=buildGraph.load()
    Line_to_display=["A","B","C","D","E"]#useless if skip=True
    plot_part_of_graph(map,Line_to_display,G,Skip=True)
    app.run(debug=True)
