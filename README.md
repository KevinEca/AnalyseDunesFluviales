# AnalyseDunesFluviales
Projet de Recherche et Développement sur l'analyse de dunes fluviales et déterminer leurs caractéristiques

Ce projet de PRD consiste à partir d'une image de relevé bathymétrique (effectué par un système echo-soundeur), de pouvoir relever la préscence des dunes au fond du bassin, et ainsi d'en extraire les caractéristiques.
Cela dans le but d'étude de sédimentologie des fleuves.

Le dossier "Pour python 2.7 (+ArcGIS)" contient un petit programme Python (version 2.7) utilisant la librairie "arcpy" de ArcGIS (librairie installée avec ce dernier).
Son but premier est de générer des images 16 en noir/blanc sur 16 bits afin d'obtenir des images avec une plus grande variante de gris → une plus grande précision lors de la recherche des dunes.
Prenons par exemple l'image fourni avec ce dépôt
 - Tout d'abord son nom "Exemple_12,4_1,95" implique que l'altitude maximum répertorié est de 12,4m et le minimum 1,95m
 - C'est une image noir/blanc 8 bits → soit 256 niveau de gris possibles
 - 12,4-1,95 / 255 = 0,04098 m → soit environ 4,1cm
 - La détection de dunes étant dès que la hauteur mesuré de cette dernière dépasse 10cm, il suffit donc juste de 3 variance de gris pour la considiérer comme une dune (4,1 * 3 = 12,3 > 10)
 
Si par contre on exploite la même image mais utilisant une plage de gris sur 16 bits, nous arrivons à un maximum de 65 536 (2^16) teintes de gris différentes.
 - Pour la même image nous arrivons donc avec une précision maximum atteignable (si l'acquisition des données est assez précise pour bien évidemment) de 12,4 -1,95 / 65 535 = 0,000159 m → soit 0.16mm !
 
Problème : Le programme génère bien des images .TIF en 16 bits (ou 8 bits si besoin au choix), mais les images obtenues ne sont pas compréhensibles par Pillow, bibliothèque pour afficher les images sur une interface en codée en Python.

Pour fonctionner le projet utilise Python 3.6 (développé avec la 3.6.4) et les librairies suivantes :
Matplotlib v2.2.0 (faire les graphiques de vue de profil)
Numpy v1.14.2 (utilisé pour faire des opérations sur des matrices / calculs scientifique)
Scipy v1.0.0 (idem que Numpy)
Pillow v5.0.0 (permet de manipuler plus de formats d'image que celle supporté par Tkinter, dont les images TIF)

Commande pour mettre à jour une bibliothèque python
python -m pip install --upgrade "nom de la bibliothèque"

Les interfaces créées n'utilise pas Qt (vu trop tard, librairie lourde pour n'apporter rien de plus) 
Néanmoins pour utiliser QT afin de créer les interfaces il faut les librairies pyqt5 et pyqt5_tools
Tutoriel comment obtenir les interfaces en python à partir du designer Qt https://www.codementor.io/deepaksingh04/design-simple-dialog-using-pyqt5-designer-tool-ajskrd09n
pour installer pyqt5, il faut passe par l'inviter de commande avec "pip install pyqt5"

Les installateurs à la racine de ce projet permettent d'installer python + les librairies en hors ligne, néanmoins comme les librairies sont lourdes, seules les scripts sont ici
Les fichiers des librairie (.whl) sont disponible sur le site pypi, comme par exemple avec pillow
https://pypi.python.org/pypi/Pillow/5.0.0