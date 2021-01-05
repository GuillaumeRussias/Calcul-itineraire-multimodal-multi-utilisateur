# Documentation de la bibliothèque compilée.

# Installation:
- (1)
    - **Sur windows** : télécharger au préalable le compilateur msvc : https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/ (laisser toutes les instructions par défaut).
    - **Sur mac et linux** : aller directement étape (3).

- (2)
    - **Avec anaconda** : AnacondaPrompt -> activer un environnement -> aller dans le répertoire du projet -> `pip install ./compiled_graph`  ou  `python -m pip install ./compiled_graph`.

# Tester :
1. Vérifier que l'environnement dans lequel vous avez installé la bibliothèque possède numpy. sinon : `conda install numpy` ou `pip install numpy` .

2. Exécuter `compiled_graph/test_compiled_graph.py` . S'il n'y a pas d'erreur , l'installation fonctionne.

# Documentation :
## Introduction :
La bibliothèque est composée de 3 classes : **graph**, **vertex** et **edge** dont un certain nombre de méthode sont intérfacées et utilisables depuis python sous réserve de l'installation et de l'import de la bibliothèque avec la commande `import fast_graph`. 

## Méthodes utilisables sous python (et C++):
1- **Classe graph**
- Constructeur : `G = graph (n)` , construit un graph sans aucune liaison (*edge*) avec n sommets (*vertex*). L'éxécution est interrompue si n n'est pas entier.
- build_scheduled_edges : `G.build_scheduled_edges(departure_index, arrival_index, departure_time, arrival_time , edge_id)` , construit les liaisons du graph G à partir de 5 arrays numpy d'entiers unidimensionnels.
- - build_scheduled_edges_string : `G.build_scheduled_edges(departure_index, arrival_index, departure_time, arrival_time , edge_id)` , construit les liaisons du graph G à partir de 3 arrays numpy d'entiers unidimensionnels. Enfin les arguments  `departure_time, arrival_time` sont





# Credits :
setup.py : Sylvain Corlay
