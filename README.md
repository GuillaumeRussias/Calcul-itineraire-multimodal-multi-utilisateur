# Projet MOPSI 2020

##### Objectif
Ce projet a pour but de développer une application web capable de calculer des itinéraires multimodaux afin de faciliter les déplacements impliquant plusieurs utilisateurs.

##### Instructions de lancement
Le site en question est pour le moment développé en interne, afin de le lancer il faut installer les packages nécessaires en exécutant la commande `pip install -r requirements.txt` à la racine du projet et ensuite se placer dans le dossier `test_site` et entrer `python3 -m flask run`.

##### Technologies utilisées
Le back-end est écrit en `flask` (utilisation du moteur de templates `jinja`). Le front-end utilise des outils `bootstrap`.

#### Consignes pour le gtfs :
La base gtfs n'est pas encore interfacée avec le site, vous pouvez faire un test en lançant gtfs_city_mapper.py .
il faut au préalable télécharger le module networkx : les commandes conda/pip install fonctionnent. 
Enfin si vous parvenez à lire les pkl, vous pouvez vous épargnez de lancer la précompilation avec data_to_graph_gtfs.py
sinon il faut lancer data_to_graph_gtfs.py, ce programme va télécharger le gtfs si la base est manquante et la compiler en fichiers pickle. prévoir un temps d'éxecution conséquent

