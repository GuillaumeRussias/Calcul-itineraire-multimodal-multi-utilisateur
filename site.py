from flask import Flask,render_template,url_for,request,redirect,json

from data_to_graph import *
from shortest_path import * #fonctionne tres bien (blibliotheque scipy.csgraph)
from class_vertice_graph import *

import Display
import folium

map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)


#Pour que ça fonctionne ne pas oublier de faire clic droit,
#"définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"

app = Flask(__name__)

def find_gare(G,gare):
    for v in G :
        if v.is_a_station and v.gare_name==gare:
            return v.index


@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")


@app.route('/affichagecarte/')
def affiche():
    return render_template("macarte.html")

@app.route('/affichagecarteactualisee/')
def afficheactualisee():
    return render_template("macarteactualisee.html")


@app.route('/itineraire/')
def itineraire():
    return render_template("itineraire.html")


@app.route('/carte/', methods=['GET', 'POST'])
def carte():

    #On initialise la carte
    map = folium.Map(
    #lat lon folium inversee avec idfm
        location=(48.852186, 2.339754),
        tiles='Stamen Toner',
        zoom_start=10)
    map.save('templates/macarte.html')

    if request.method == "GET":
        liste_stations = [station for station in load_station_names()]
        return render_template("carte.html",liste_stations = json.dumps(liste_stations))

    if request.method == 'POST':
        origine = request.form['origine']
        destination = request.form['destination']

        G = load()
        i = find_gare(G,origine)
        j = find_gare(G,destination)

        print("finding traject",G[i].gare_name , "to", G[j].gare_name)
        A = G.A_matrix(type_cost=Edge.customized_cost1)
        path = path_finder(A, i, j)

        for i in path:
            print(G[i].gare_name)

        Display.plot_a_course(map,path,G)

        map.save('templates/macarteactualisee.html')

        return redirect(url_for ('itineraire'))



if __name__ == "__main__":
    app.run()
