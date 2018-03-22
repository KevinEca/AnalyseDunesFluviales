@echo off

SET PIP_INSTALL=python -m pip install
SET PACKAGE_PATH=./
SET NUMPY_PATH=%PACKAGE_PATH%numpy-1.14.2-cp36-none-win_amd64.whl
SET SCIPY_PATH=%PACKAGE_PATH%scipy-1.0.0-cp36-none-win_amd64.whl
SET MATPLOTLIB_PATH=%PACKAGE_PATH%matplotlib-2.2.2-cp36-cp36m-win_amd64.whl
SET PILLOW_PATH=%PACKAGE_PATH%Pillow-5.0.0-cp36-cp36m-win_amd64.whl
:: %~dp0 fait référence au dossier courant
:: si on trouve pas l'installateur de python, on le signale à l'utilisateur et on quitte le programme
SET PYTHON_INSTALL=%PACKAGE_PATH%python-3.6.4-amd64.exe
:: Ainsi on ne défini pas la variable
SET MANQUE_WHEEL = 

:Demarrage
:: On regarde si Python 3.6.X a été installé
IF EXIST "C:\Python36\python.exe" GOTO :Install_Package

echo pour installer Python il faut que le ficier python-3.6.4-amd64.exe (executable installer) soit dans le meme repertoire que cet installateur
echo Python 3.6 n'est pas encore installe, faisons le maintenant

echo %PYTHON_INSTALL%

IF NOT EXIST %PYTHON_INSTALL% (
	echo Le fichier d'installation n'est pas trouve, il peut-etre telecharge sur https://www.python.org/ - version 3.6.4
	GOTO :Sortie
)

echo Le repertoire d'installation doit etre "C:\Python36"
python-3.6.4-amd64.exe
GOTO :Install_Package

:Install_Package
echo Version de python installe
python --version
echo ------ Installons maintenant les packages -------
echo Les packages sont numpy 1.14.2, scipy 1.0.0, matplotlib 2.2.2 et Pillow 5.0.0

set /p ChoixInstallation="Voulez-vous faire une installation en ligne (n'utilise pas les packages wheel telecharges au prealable) ? (o/n)"

IF %ChoixInstallation% == o (GOTO :Install_Package_Online) ELSE (GOTO :Install_Package_Offline)

:Install_Package_Online
echo Installation en ligne
echo 1. Mise a jour pip (web)
%PIP_INSTALL% --upgrade pip
echo 2. Installation Numpy (web)
%PIP_INSTALL% numpy==1.14.2
echo 3. Installation Scipy (web)
%PIP_INSTALL% scipy==1.0.0
echo 4. Installation Matplotlib (web)
%PIP_INSTALL% matplotlib==2.2.2
echo 5. Installation Pillow (web)
%PIP_INSTALL% pillow==5.0.0
GOTO :Fin_Install
	
:Install_Package_Offline
echo Installation hors-ligne
IF NOT EXIST %SCIPY_PATH% (
	echo Il manque le fichier wheel de scipy disponible sur https://pypi.python.org/pypi/scipy - version 1.0.0
	SET MANQUE_WHEEL=1
)
IF NOT EXIST %NUMPY_PATH% (
	echo Il manque le fichier wheel de numpy disponible sur https://pypi.python.org/pypi/numpy - version 1.14.2
	SET MANQUE_WHEEL=1
)
IF NOT EXIST %MATPLOTLIB_PATH% (
	echo Il manque le fichier wheel de matplotlib disponible sur https://pypi.python.org/pypi/matplotlib - version 2.2.2
	SET MANQUE_WHEEL=1
)
IF NOT EXIST %PILLOW_PATH% (
	echo Il manque le fichier wheel de pillow disponible sur https://pypi.python.org/pypi/pillow - version 5.0.0
	SET MANQUE_WHEEL=1
)
IF DEFINED %MANQUE_WHEEL% (
	echo Il manque au moins une librairie au format wheel (whl)
	GOTO :Sortie
)
	
::echo 0. Mise a jour pip (web)
::%PIP_INSTALL% --upgrade pip
echo 1. Installation Numpy (wheel)
%PIP_INSTALL% %NUMPY_PATH%
echo 2. Installation Scipy (wheel)
%PIP_INSTALL% %SCIPY_PATH%
echo 3. Installation Matplotlib (wheel)
%PIP_INSTALL% %MATPLOTLIB_PATH%
echo 4. Installation Pillow (wheel)
%PIP_INSTALL% %PILLOW_PATH%
GOTO :Fin_Install

:Fin_Install
echo ------ Tous les packages sont installes -------
echo *********Le programme d'analyse de dunes peux maintenant s'executer*********

:: EXIT est un nom système de la commande de sortie
:Sortie
set /p DUMMY=Press ENTRER pour quitter...
