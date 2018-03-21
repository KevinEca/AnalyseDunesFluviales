@echo off

SET PIP_INSTALL=python -m pip install
SET PACKAGE_PATH=./
SET NUMPY_PATH=%PACKAGE_PATH%numpy-1.14.2-cp36-none-win_amd64.whl
SET SCIPY_PATH=%PACKAGE_PATH%scipy-1.0.0-cp36-cp36m-win_amd64.whl
SET MATPLOTLIB_PATH=%PACKAGE_PATH%matplotlib-2.2.2-cp36-cp36m-win_amd64.whl
SET PILLOW_PATH=%PACKAGE_PATH%Pillow-5.0.0-cp36-cp36m-win_amd64.whl

:START_POINT
IF EXIST "C:\Python36\python.exe" GOTO :Install_Package

echo Python 3.6 n'est pas encore installe, faisons le maintenant
echo repertoire d'installation "C:\Python36"
python-3.6.4-amd64.exe
GOTO :START_POINT

:Install_Package
echo Version de python installe
python --version
echo ------ Installons maintenant les packages -------
echo Les packages sont numpy 1.14.2, scipy 1.0.0, matplotlib 2.2.2 et Pillow 5.0.0
echo Ils peuvent etre telecharges sur https://pypi.python.org/pypi et doivent etre dans le meme repertoire que cette installateur
echo 1. Mise a jour pip (web)
%PIP_INSTALL% --upgrade pip
echo 2. Installation Numpy (wheel)
%PIP_INSTALL% %NUMPY_PATH%
echo 3. Installation Scipy (wheel)
%PIP_INSTALL% %SCIPY_PATH%
echo 4. Installation Matplotlib (wheel)
%PIP_INSTALL% %MATPLOTLIB_PATH%
echo 5. Installation Pillow (wheel)
%PIP_INSTALL% %PILLOW_PATH%

echo ------ Tous les packages sont installes -------
echo *********Le programme d'analyse de dunes peux maintenant s'executer*********
set /p DUMMY=Press ENTRER pour quitter...
