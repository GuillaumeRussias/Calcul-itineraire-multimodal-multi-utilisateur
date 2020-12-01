***New***
Exploitation du format gtfs . Nouveau module requis : networkx
Il est nécessaire de télécharger le gtfs


***Old***
Requirements:
python module : json,copy

Description:
3 fichiers python.
data_classes.py : definit des classes pour exploiter les bases de données
tree.py : définit une structure en arbre, utile a data_classes
exceptions : contient les differentes exceptions soulevable par les autres scripts

1 dossier data:
*referentiel-des-lignes.json : base de données IDFM-pas util pour l'instant
*transport_idf_open_streetmap.json : base de données OpenStreet Map-Point géographique des gares uniquement, ne communique pas avec la base idfm
*lignes gtfs: contient les liens entre arrêt pour chaques missions: pb : les arrêts n'ont pas d'identifiant pour faire le lien avec une autre base, chaque mission a la meme valeur: par exemeple, avec cette base la gare de l'est est desservie par la ligne E du RER au meme titre que Noisy champs avc le RER A, or la gare de l'est n'est desservie qu'en situation perturbee
*Referentiel Stops: format shape, impossible a lire pour l'instant
*referentiel gares: bien pour les gares, mais pas de liaison entre elles
*IDFM-gtfs:format txt pas explote pour l'instant mais prometteur
