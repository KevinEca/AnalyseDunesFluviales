from PIL import Image
from TraitementImage import ImageDune
import unittest

NiveauDeGrisDifferent = 256
NomImage1 = "Exemple_1,95_12,4.tif"
NomImage2 = "Exemple2_5,548_11,20.tif"
NomImageEchec = "Echec test.tif"
NomImageIncomplet = "Exemple2_5,548.tif"
NomImageExistePas = "Exemple3_5,548_11,20.tif"

class test_ImageDune(unittest.TestCase):
    
    # L'image existe
    def testImageDuneValide1(self):
        MonImage = ImageDune.ImageDune()
        ImageValide = MonImage.AttribuerImage(NomImage1)
        self.assertEqual(ImageValide, True, "Echec Test image 1")
    
    # L'image existe, autre exemple
    def testImageDuneValide2(self):
        MonImage = ImageDune.ImageDune()
        ImageValide = MonImage.AttribuerImage(NomImage2)
        self.assertEqual(ImageValide, True, "Echec Test image 2")
    
    # L'image existe mais n'est pas sous le bon format de nom
    def testImageDuneValide3(self):
        MonImage = ImageDune.ImageDune()
        ImageValide = MonImage.AttribuerImage(NomImageEchec)
        self.assertEqual(ImageValide, False, "Echec Test image 3")
    
    # L'image existe mais n'est pas sous le format complet du nom à prendre
    def testImageDuneValide4(self):
        MonImage = ImageDune.ImageDune()
        ImageValide = MonImage.AttribuerImage(NomImageIncomplet)
        self.assertEqual(ImageValide, False, "Echec Test image 4")
        
    # L'image n'existe pas
    def testImageDuneValide5(self):
        MonImage = ImageDune.ImageDune()
        ImageValide = MonImage.AttribuerImage(NomImageExistePas)
        self.assertEqual(ImageValide, False, "Echec Test image 5")
        
    # Tester comment est déterminé la hauteur de l'image
    def testHauteurImage(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        Hauteur = Image.open(NomImage1).size[1]
        self.assertEqual(MonImage.getHauteurImage(), Hauteur, "Echec récupération de l'hauteur de l'image")
    
    # Tester comment est déterminé la largeur de l'image 
    def testLargeurImage(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        Largeur = Image.open(NomImage1).size[0]
        self.assertEqual(MonImage.getLargeurImage(), Largeur, "Echec récupération de de largeur de l'image")
    
    # Tester comment est déterminé le chemin menant à l'image
    def testCheminImage(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        self.assertEqual(MonImage.getCheminImage(), NomImage1, "Echec du nom de l'image")
    
    # Tester comment est déterminé le nom du fichier de l'image
    def testNomImage(self):
        CheminImage = NomImage1
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(CheminImage)
        NomImage = (CheminImage.split("/"))[-1]
        self.assertEqual(MonImage.getNomImage(), NomImage, "Echec de la récupération du chemin de l'image")

    # Premier test pour déterminer L'altitude minimum d'une image
    def testAltitudeMinimumImage1(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        self.assertEqual(MonImage.getAltitudeMin(), 1.95, "Echec récupération altitude minimum 1")
        
    # Deuxième test pour déterminer L'altitude minimum d'une image
    def testAltitudeMinimumImage2(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage2)
        self.assertEqual(MonImage.getAltitudeMin(), 5.548, "Echec récupération altitude minimum 2")
    
    # Premier Test pour vérifier la résolution d'une image
    def testResolutionImage1(self):
        CheminImage = NomImage1
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(CheminImage)
        self.assertEqual(MonImage.getResolutionAltitude(), self.CalculResolutionImage(CheminImage, MonImage), "Echec déterminé résolution 1")
    
    # Premier Test pour vérifier la résolution d'une image 
    def testResolutionImage2(self):
        CheminImage = NomImage2
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(CheminImage)
        
        self.assertEqual(MonImage.getResolutionAltitude(), self.CalculResolutionImage(CheminImage, MonImage), "Echec déterminé résolution 2")
        
    # Méthode qui calcul et retourne la résolution d'une image envoyé e paramètre
    def CalculResolutionImage(self, CheminImage, MonImage):
        AltitudeMinimum = MonImage.getAltitudeMin()
        
        NomImage = (CheminImage.split("/"))[-1]
        DecoupeNomImage = NomImage.split("_")
        #AltitudeMin = float(DecoupeNomImage[-2].replace(',', '.'))
        AltitudeMaximum = float((DecoupeNomImage[-1].split("."))[0].replace(',', '.'))
        
        ResolutionAltitude = round((AltitudeMaximum - AltitudeMinimum) / (NiveauDeGrisDifferent - 1), 5)
        return ResolutionAltitude
    
    def testCourant1(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        self.assertEqual(MonImage.getSensCourantGauche(), True, "Echec - par défaut le sens du courant est vers la gauche")
        
    def testCourant2(self):
        MonImage = ImageDune.ImageDune()
        MonImage.AttribuerImage(NomImage1)
        MonImage.setSensCourantGauche(False)
        self.assertEqual(MonImage.getSensCourantGauche(), False, "Echec - le sens du courant doit être modifié (vers la droite)")

# Ceci lance le test si on exécute le script directement.
if __name__ == '__main__':
    unittest.main()