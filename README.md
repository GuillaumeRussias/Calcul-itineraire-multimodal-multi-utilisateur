# Projet MOPSI-TDLOG 2020

Projet réalisé par Emma BEUZE, Guillaume RUSSIAS, Aubin TCHOI
encadré par Guillaume DALLE

##### Objectif
Ce projet a pour but de développer une application web capable de calculer des itinéraires multimodaux afin de faciliter les déplacements impliquant plusieurs utilisateurs.

##### Instructions d'installation
Le site en question est pour le moment développé en interne.
Dans un environnement contenant `3.8.0 <= python < 3.9.0` en version 64bits, installer les packages nécessaires avec la commande `pip install -r requirements.txt` à la racine du projet. Il est aussi nécessaire de **compiler le code en C++ :**
- (1)
    - **Sur windows** : télécharger au préalable le compilateur msvc : [lien de téléchargement](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/)  (laisser toutes les instructions par défaut).
    - **Sur mac et linux** : aller directement étape (2).

- (2)
    - **Commande** : exécuter la commande `pip install ./compiled_graph`  ou  `python -m pip install ./compiled_graph` à la racine du projet.
#### Gestion des données
Lors du premier lancement du projet, il est nécessaire de télécharger les bases de données et d'effectuer une étape de précompilation assez longue (20 min). Celà ne nécessite pas de manipulation supplémentaire particulière.

#### Lancement du site
Exécuter le fichier `site.py` . A chaque lancement , une instruction demande si vous voulez mettre à jour la base de données . Si vous acceptez le programme effectue de nouveau le téléchargement et la précompilation.

##### Technologies utilisées
- **front** : `html`, `javascript`, `css`, `bootstrap`, `leaflet`
- **back** :  `python`, `flask` (utilisation du moteur de templates `jinja`), `pandas`

Pour des soucis de rapidité , le back est composé d'une dernière couche codée en `C++` et interfacée avec `python` avec la bilbiothèque `pybind11`.


