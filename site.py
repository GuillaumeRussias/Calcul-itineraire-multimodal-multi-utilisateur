import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from flask import Flask,render_template,url_for,request,redirect,json

from load_data.data_to_graph import *
from python_graph.shortest_path import * # fonctionne tres bien (blibliotheque scipy.csgraph)
from python_graph.class_vertice_graph import *

import display_on_map.Display as Display
import folium

map = folium.Map(
#lat lon folium inversee avec idfm
    location=(48.852186, 2.339754),
    tiles='Stamen Toner',
    zoom_start=10)


# Pour que ça fonctionne ne pas oublier de faire clic droit,
# "définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"

app = Flask(__name__)

def find_gare(G,gare):
    for v in G :
        if v.is_a_station and v.gare_name==gare:
            return v.index

liste_gares_itineraire = []

# Affichage des résultats d'une recherche
@app.route('/affichagecarte/')
def affiche():
    return render_template("macarte.html")

@app.route('/affichagecarteactualisee/')
def afficheactualisee():
    return render_template("macarteactualisee.html")

# Affichage des différents plans de réseaux (RER & métro ou Bus)
@app.route('/affichagereseauRER')
def affichagereseaRER():
    return render_template("reseauRER.html")

@app.route('/affichagereseauBus')
def affichagereseauBus():
    return render_template("reseauBus.html")


# Onglets de la barre de navigation
@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")

@app.route('/itineraire/')
def itineraire():
    return render_template("itineraire.html", feuille_route = liste_gares_itineraire)

@app.route('/reseau/')
def reseau():
    return render_template("reseau.html")

@app.route('/carte/', methods=['GET', 'POST'])
def carte():

    # On initialise la carte
    map = folium.Map(
    # lat lon folium inversee avec idfm
        location=(48.852186, 2.339754),
        tiles='Stamen Toner',
        zoom_start=10)
    map.save('templates/macarte.html')

    if request.method == "GET":
        liste_stations = [station for station in load_station_names()]
        return render_template("carte.html",liste_stations = json.dumps(liste_stations))

    if request.method == 'POST':

        # On initialise la liste des gares parcourues
        # liste_gares_itineraire = []

        origine = request.form['origine']
        destination = request.form['destination']

        G = load()
        i = find_gare(G,origine)
        j = find_gare(G,destination)

        print("finding traject",G[i].gare_name , "to", G[j].gare_name)
        A = G.A_matrix(type_cost=Edge.customized_cost1)
        path = path_finder(A, i, j)

        for i in path:
            liste_gares_itineraire.append(G[i].gare_name)

        Display.plot_a_course(map,path,G)

        map.save('templates/macarteactualisee.html')

        return redirect(url_for ('itineraire'))






if __name__ == "__main__":
    app.run()
