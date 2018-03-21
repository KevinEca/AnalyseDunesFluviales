#!/bin/bash

echo "Installation Python 3.6 + librairies associees"

echo "Mise a jour (apt-get update)"
sudo apt-get update

echo "Installation de Python 3.6"
sudo apt-get install python3.6

echo "1. Mise a jour pip (web)"
sudo pip install pip --upgraded

echo "2. Installation Numpy"
pip install numpy-1.14.2-cp36-cp36m-manylinux1_x86_64.whl
echo "3. Installation Scipy"
pip install scipy-1.0.0-cp36-cp36m-manylinux1_x86_64.whl
echo "4. Installation Matplotlib"
pip install matplotlib-2.2.2-cp36-cp36m-manylinux1_x86_64.whl
echo "5. Installation Pillow"
pip install Pillow-5.0.0-cp36-cp36m-manylinux1_x86_64.whl

echo "Installation termine (appuyer sur une touche pour fermer)"
read