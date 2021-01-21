import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from flask import Flask,render_template,url_for,request,redirect,json

import load_data.load_compiled_graph2 as load_graph
import display_on_map.Display_geojson as display_geo





# Pour que ça fonctionne ne pas oublier de faire clic droit,
# "définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

graph = load_graph.load_graph()


default_time = 8*3600
default_origine = 0
default_destination = 1

def extract_index(gare_name):
    #extract station_index from gare_name : gare_name = "station_name / station_index"
    gare_name = gare_name.split("/")
    index = int(gare_name[-1][1:])
    return index

def time_to_sec(time):
    print(time,type(time))
    try :
        time=time.split(":")
        time = int(time[0])*3600 + int(time[1])*60
    except:
        time = default_time
    if time>=24*3600 or time<0 :
        time = default_time

    return time

def city_mapper_single_user(request):
    h_debut = time_to_sec(request.form['time'])
    origine = request.form['origine']
    destination = request.form['destination']

    try :
        i = extract_index(origine)
        j = extract_index(destination)
        path = graph.time_changement_path_finder(i,j,h_debut)
    except Exception as e:
        i = default_origine
        j = default_destination
        path = graph.time_changement_path_finder(default_origine,default_destination,default_time)
        print(e)

    print("==============================")
    print(i,j)
    print("From",load_graph.PandaV["station_name"][i],"to",load_graph.PandaV["station_name"][j])
    dep = display_geo.seconds_to_hours(graph[path[0]].time())
    arr = display_geo.seconds_to_hours(graph[path[-1]].time())
    print("Departure time =",dep,"| Arrival time =",arr)
    print("==============================")

    return path

def create_geojson_file(path):
    try :
        display_geo.create_geojson_file(VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph , file_path = currentdir + "/templates/geojson/geojson_singleuser.js")
    except :
        print("path not displayable")



# Affichage des résultats d'une recherche
@app.route('/affichagecarte/')
def affiche():
    return render_template("carte_accueil.html")

@app.route('/route_display_single_user/')
def route_display_single_user():
    return render_template("route_display.html", geojson_url = "/geojson_single_user")

@app.route('/route_description_single_user/')
def route_description_single_user():
    return render_template("route_info_display.html", geojson_url = "/geojson_single_user")

@app.route('/geojson_single_user/')
def render_geojson_single_user():
    return render_template("geojson/geojson_singleuser.js")



# Affichage des différents plans de réseaux (RER & métro ou Bus)
@app.route('/affichagereseauRER')
def affichagereseaRER():
    return render_template("reseauRER.html")



# Onglets de la barre de navigation
@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")

@app.route('/itineraire/')
def itineraire():
    return render_template("itineraire.html")

@app.route('/reseau/')
def reseau():
    return render_template("reseau.html")

@app.route('/carte/', methods=['GET', 'POST'])
def carte():
    if request.method == "GET":
        return render_template("carte.html",liste_stations = json.dumps(load_graph.station_names))
    if request.method == 'POST':
        path = city_mapper_single_user(request)
        create_geojson_file(path)
        return redirect(url_for ('itineraire'))


if __name__ == "__main__":
    app.run()
