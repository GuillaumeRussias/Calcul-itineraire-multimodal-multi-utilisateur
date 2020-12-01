# Installation du code compilé:
- (1)
    - **Sur windows** : télécharger au préalable le compilateur msvc : https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/ (laisser toutes les instructions par défaut).
    - **Sur mac et linux** : aller directement étape (3). (testé sur linux , supposé pour mac).

- (2)
    - **Avec anaconda** : AnacondaPrompt -> activer un environnement -> aller dans le répertoire du projet -> `pip install ./compiled_graph`  ou  `python -m pip install ./compiled_graph`.

# Tester :
1. Vérifier que l'environnement dans lequel vous avez installé la bibliothèque possède numpy. sinon : `conda install numpy` ou `pip install numpy` .

2. Exécuter `compiled_graph/test_compiled_graph.py` . S'il n'y a pas d'erreur , l'installation fonctionne.


# Credits :
setup.py : Sylvain Corlay
