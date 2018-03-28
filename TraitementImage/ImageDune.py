from PIL import Image
from tkinter import messagebox
from os.path import isfile

class ImageDune():
    
    def __init__(self):
        
        self.CheminImage = "" # chemin indiquant où se trouve l'image sélectionnée
        self.NomImage = "" # contient le nom de l'image (qui sera reprit comme indication pour les exports TXT d'informations des dunes trouvées)
        self.Image = Image # variable pour stocker en mémoire le tableau original de l'image (après passage en noir et blanc 8 bits)
        self.AltitudeMin = 0 # L'altitude minimum de l'image
        self.ResolutionAltitude = 0 # La résolution de l'altitude de l'image → diffèrence d'altitude (cm) entre 2 niveaux de gris
        self.CourantVersLaGauche = True
            
    def AttribuerImage(self, Chemin):
        # par défaut on suppose que l'image ne correspond pas aux contraintes nécessaires pour effectuer un traitement de l'image
        ImageValide = False
    
        #print(isfile(Chemin))
        #print(self.VerifierImage())
        # On vérfie que l'image respecte la convention de nommage et qu'elle existe à l'emplacement indiqué
        if self.VerifierImage(Chemin) and isfile(Chemin):
            # On modifie le chemin indiquant où se trouve l'image sélectionnée
            self.CheminImage = Chemin 
            # On Convertie l'image en noir et blanc 8 bits et on la sauvegarde en mémoire
            self.Image = Image.open(self.CheminImage).convert('L')
            # On signale que la nouvelle image choisie est valide
            ImageValide = True        
        
        return ImageValide
            
    def getCheminImage(self):
        return self.CheminImage
    
    def getNomImage(self):
        return self.NomImage
    
    def CheminValide(self):
        return len(self.CheminImage) > 0
            
    def getImage(self):
        return self.Image
    
    def getHauteurImage(self):
        return self.Image.size[1]
    
    def getLargeurImage(self):
        return self.Image.size[0]
    
    def getAltitudeMin(self):
        return self.AltitudeMin
    
    def getResolutionAltitude(self):
        return self.ResolutionAltitude
    
    def setSensCourantGauche(self, CourantVersGauche):
        self.CourantVersLaGauche = CourantVersGauche
    
    def getSensCourantGauche(self):
        return self.CourantVersLaGauche
    
    def VerifierImage(self, Chemin):
        # par défaut on suppose que l'image ne correspond pas aux contraintes nécessaires pour effectuer un traitement de l'image
        ImageValide = False
    
        try:
            # Tout d'abord on comme du chemin complet d'accès comple vers le fichier, par exemple C:/Exemple_8,508_5,029.tif
            # On découpe donc suivant le caractère '/' et on récupère le dernier morceau pour obtenir le nom de l'image
            # On obtient ainsi Exemple_8,508_5,029.tif
            # On le redécoupe donc par le caractère "_"
            # Altitude maximum : on en prend l'avant dernier morceau et on remplace la ',' par un '.' → conversion en float
            # Altitude minimum : on prend le dernier morceau, 
            #                    on le coupe par le caractère '.' pour enlever le '.tiff'
            #                    on en prend le premier morceau "5,029" et on remplace la ',' par un '.' → conversion en float

            self.NomImage = (Chemin.split("/"))[-1]
            DecoupeNomImage = self.NomImage.split("_")
            self.AltitudeMin = float(DecoupeNomImage[-2].replace(',', '.'))
            AltitudeMaximum = float((DecoupeNomImage[-1].split("."))[0].replace(',', '.'))
            # la résolution de l'altitude 
            # nombre de mètre correspond Ã  la différence d'altitude entre 2 niveaux de gris successif
            # 256 niveaux de gris → on divise par 255 la différence entre le min et le max (la 256ème valeur étant le min + 0 * ResolutionAltitude)
            self.ResolutionAltitude = round((AltitudeMaximum - self.AltitudeMin) / 255, 5)
            
            #print("Altitude Max = " + str(AltitudeMaximum))
            #print("Altitude Min = " + str(self.AltitudeMin))
            #print("Resolution image = " + str(self.ResolutionAltitude))

            # Si nous somme arrivé jusque ici, c'est que l'image est valide
            ImageValide = True
                
        except (ValueError, IndexError) :
            ImageValide = False
            
        return ImageValide
    
    