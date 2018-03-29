# AnalyseDunesFluviales
Projet de Recherche et Développement sur l'analyse de dunes fluviales et déterminer leurs caractéristiques

Ce projet de PRD consiste à partir d'une image de relevé bathymétrique (effectué par un système echo-soundeur), de pouvoir relever la présence des dunes au fond du bassin, et ainsi d'en extraire les caractéristiques.
Cela dans le but d'étude de sédimentologie des fleuves.

Le dossier "Pour python 2.7 (+ArcGIS)" contient un petit programme Python (version 2.7) utilisant la librairie "arcpy" de ArcGIS (librairie installée avec ce dernier).
Son but premier est de générer des images 16 en noir/blanc sur 16 bits afin d'obtenir des images avec une plus grande variante de gris → une plus grande précision lors de la recherche des dunes.
Prenons par exemple l'image fournie avec ce dépôt
 - Tout d'abord son nom "Exemple_12,4_1,95" implique que l'altitude maximum répertorié est de 12,4m et le minimum 1,95m
 - C'est une image noir/blanc 8 bits → soit 256 niveau de gris possibles
 - 12,4-1,95 / 255 = 0,04098 m → soit environ 4,1cm
 - La détection de dunes étant dès que la hauteur mesurée de cette dernière dépasse 10cm, il suffit donc juste de 3 variance de gris pour la considiérer comme une dune (4,1 * 3 = 12,3 > 10)
 
Si par contre on exploite la même image mais utilisant une plage de gris sur 16 bits, nous arrivons à un maximum de 65 536 (2^16) teintes de gris différentes.
 - Pour la même image nous arrivons donc avec une précision maximum atteignable (si l'acquisition des données est assez précise pour bien évidemment) de 12,4 -1,95 / 65 535 = 0,000159 m → soit 0.16mm !
 
Problème : le programme génère bien des images .TIF en 16 bits (ou 8 bits si besoin au choix), mais les images obtenues ne sont pas compréhensibles par Pillow, bibliothèque pour afficher les images sur une interface en codée en Python.

Pour fonctionner le projet utilise Python 3.6 (développé avec la 3.6.4) et les librairies suivantes :
 - Matplotlib v2.2.2 (faire les graphiques de vue de profil) https://pypi.python.org/pypi/matplotlib
 - Numpy v1.14.2 (utilisé pour faire des opérations sur des matrices / calculs scientifique) https://pypi.python.org/pypi/numpy
 - Scipy v1.0.0 (idem que Numpy) https://pypi.python.org/pypi/scipy
 - Pillow v5.0.0 (permet de manipuler plus de formats d'image que celles supportées par Tkinter, dont les images TIF) https://pypi.python.org/pypi/Pillow/5.0.0

Commande pour mettre à jour une bibliothèque python
python -m pip install --upgrade "nom de la bibliothèque"

Le projet étant basé sur du code Python, l'édition de ses fichiers peut se faire depuis un simple éditeur de texte, mais aussi par un IDE comme PyCharm ou Eclipse (avec le plugin PyDev).

Les interfaces créées n'utilisent pas Qt (vu trop tard, librairie lourde pour n'apporter rien de plus) 
Néanmoins pour utiliser QT afin de créer les interfaces il faut les librairies pyqt5 et pyqt5_tools
Tutoriel comment obtenir les interfaces en python à partir du designer Qt https://www.codementor.io/deepaksingh04/design-simple-dialog-using-pyqt5-designer-tool-ajskrd09n
pour installer pyqt5, il faut passe par l'inviter de commande avec "pip install pyqt5"

Les installateurs à la racine de ce projet permettent d'installer python + les librairies en hors ligne, néanmoins comme les librairies sont lourdes, seules les scripts sont ici
Les fichiers des librairie (.whl) sont disponibles sur le site pypi, comme par exemple avec pillow
https://pypi.python.org/pypi

Les différents tests unitaires sont dans le dossier "Tests" de ce même dépôt, il contient 4 fichiers Python contenant une liste de tests qui vont tester la fiabilité des classes "Point", "Axe", "GestionAxes" et "ImageDune".

Bien évidemment, la classe "GestionAxes" utilisant la classe "Axe" qui elle même appelle les méthodes de "Point", il faut commencer par vérifier la classe "Point" puis "Axe" avant de lancer les tests sur "GestionAxes".

Les tests unitaires sont faits avec unittest, pour les exécuter il suffit par exemple d'ouvrir le projet sous son IDE, puis de demander l'exécution des fichiers "test_Point.py", "test_Axe.py", "test_GestionAxes.py" ou "test_ImageDune.py" pour effectuer les tests sur leur classe associée, l'ensemble des tests de la classe se lancerons, il suffira juste de déterminer lesquels sont faux pour ajuster ses classes pour qu'ils respectent les tests.

Par exemple avec l'IDE eclipse (+ plugin PyDev), il suffit de lancer les classes de tests en tant que "python uni-test".
Il est aussi possible depuis un invite de commande / terminal d'exécuter l'ensemble des fichier test d'un coup. Pour ce faire déplacer vous jusqu'au dossier "Tests" du projet, puis lancer la commande "python -m unittest discover".
