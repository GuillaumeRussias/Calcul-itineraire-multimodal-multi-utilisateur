from flask import Flask,render_template,url_for,request, redirect, json

import folium

from data_to_graph import *

#Pour que ça fonctionne ne pas oublier de faire clic droit,
#"définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"

app = Flask(__name__)


@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")


@app.route('/carte/', methods=['GET', 'POST'])
def carte():
    if request.method == "GET":
        liste_stations = load_station_names()
        liste_serializable = [station for station in liste_stations]

        return render_template("carte.html",liste_stations = json.dumps(liste_serializable))

    if request.method == 'POST':
        coords = (request.form['latitude'],request.form['longitude'])
        folium_map = folium.Map(location=coords, zoom_start=14)
        return folium_map._repr_html_()


if __name__ == "__main__":
    app.run()
