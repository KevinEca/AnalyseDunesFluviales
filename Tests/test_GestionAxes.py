import unittest
from TraitementImage import GestionAxes

class test_GestionAxes(unittest.TestCase):
    
    # L'image existe
    def testListeVide(self):
        MesAxes = GestionAxes.GestionAxes()
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 0, "Echec liste d'axes non initialisé vide")
        
    def testListe1Element(self):
        MesAxes = GestionAxes.GestionAxes()
        MesAxes.AjouterPoint(25, 25)
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 1, "Echec liste d'axes non incrémenté")

    def testListe1AxeTaille0(self):
        MesAxes = GestionAxes.GestionAxes()
        MesAxes.AjouterPoint(25, 25)
        AxeCree = MesAxes.AjouterPoint(25, 25)
        self.assertEqual(AxeCree, False, "Echec - il est impossible de créer un axe de taille null (coordonnées départ = coordonnées arrivée)")
        
    def testListe1AxeAjoute(self):
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 1)
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 1, "Echec liste d'axes non incrémenté (ne passe pas à 1)")
        
    def testListe3AxesAjoute(self):
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 3)
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 3, "Echec liste d'axes non incrémenté (test pour 3 axes créés)")
            
    def AjouterAxes(self, MesAxes, NombreAxesAjoutes):
        for i in range(0,NombreAxesAjoutes):
            MesAxes.AjouterPoint(25, 25)
            MesAxes.AjouterPoint(20, 20)
            
    def testSuppression1Axe(self):
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 3)
        # On supprime le premier axe de la liste
        MesAxes.SupprimerAxe(0)
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 2, "Echec la suppression d'un axe ne sait pas passé correctement (passage de 3 à 2)")
          
    def testSuppressionTousAxes(self):
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 5)
        MesAxes.SupprimerTousAxes()
        NombreAxes = MesAxes.NombreAxes()
        self.assertEqual(NombreAxes, 0, "Echec la suppression de tous les axes ne sait pas fait correctement")
          
          
    def testLecturePrecisAxe(self):
        Correct = False
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 3)
        MesAxes.AjouterPoint(10, 10)
        MesAxes.AjouterPoint(30, 30)
        self.AjouterAxes(MesAxes, 2)
        Coordonnees = MesAxes.CoordonneesAxe(3)
        # On teste chacune des coordonnées récupérées
        if(Coordonnees[0][0] == 10 and Coordonnees[0][1] == 10 and Coordonnees[1][0] == 30 and Coordonnees[1][1] == 30):
            Correct = True
        self.assertEqual(Correct, True, "Echec lecture de données d'un d'axe dans la liste")
            
    def testDernierElementIncomplet(self):
        MesAxes = GestionAxes.GestionAxes()
        MesAxes.AjouterPoint(25, 25)
        EstComplet = MesAxes.DernierAxeComplet()
        self.assertEqual(EstComplet, False, "Echec le dernier element doit-être incomplet")
        
    def testDernierElementComplet(self):
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 1)
        EstComplet = MesAxes.DernierAxeComplet()
        self.assertEqual(EstComplet, True, "Echec le dernier element doit-être complet")
        
    def testVecteurPrecisAxe(self):
        Correct = False
        MesAxes = GestionAxes.GestionAxes()
        self.AjouterAxes(MesAxes, 3)
        MesAxes.AjouterPoint(10, 10)
        MesAxes.AjouterPoint(30, 30)
        self.AjouterAxes(MesAxes, 2)
        Vecteur = MesAxes.VecteurAxe(3)
        if(Vecteur[0] == 20 and Vecteur[1] == 20):
            Correct = True
        self.assertEqual(Correct, True, "Echec le calcul du vecteur 'est pas correct")

# Ceci lance le test si on exécute le script directement.
if __name__ == '__main__':
    unittest.main()
        