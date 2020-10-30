from flask import Flask,render_template,url_for,request, redirect

import folium

app = Flask(__name__)


@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")


@app.route('/carte/', methods=['GET', 'POST'])
def carte():
    if request.method == "GET":
        return render_template("carte.html")

    if request.method == 'POST':
        coords = (request.form['latitude'],request.form['longitude'])
        folium_map = folium.Map(location=coords, zoom_start=14)
        return folium_map._repr_html_()


if __name__ == "__main__":
    app.run()

