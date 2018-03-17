"""Fichier d'installation de notre script salut.py."""

from setuptools import setup, find_packages
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# On appelle la fonction setup

setup(
    name = "Analyse dune fluviale",
    version = "1",
	author = "Kevin Ecalle",
    description = "Executable pour windows",
	packages=find_packages(),
    scripts=['Main.pyw']
)