import unittest
from TraitementImage import Axe

class test_Axe(unittest.TestCase):
    
    def testInitialisationAxe(self):
        Correct = False
        MonAxe = Axe.Axe(15, 25)
        PointDepart = MonAxe.getCoordonneesPointDepart()
        #PointDepart = MonAxe.getPointDepart().getCoordonnees()
        if(PointDepart[0] == 15 and PointDepart[1] == 25):
            Correct = True
        self.assertEqual(Correct, True, "Echec Initialisation d'un axe")
        
    def testPointArriveAxe(self):
        Correct = False
        MonAxe = Axe.Axe(15, 25)
        MonAxe.AjoutPointArrive(50, 100)
        PointArrive = MonAxe.getCoordonneesPointArrive()
        #PointArrive = MonAxe.getPointArrive().getCoordonnees()
        if(PointArrive[0] == 50 and PointArrive[1] == 100):
            Correct = True
        self.assertEqual(Correct, True, "Echec placement du deuxième point de l'axe")
        
    def testVecteurAxe(self):
        Correct = False
        MonAxe = Axe.Axe(15, 25)
        MonAxe.AjoutPointArrive(50, 100)
        Vecteur = MonAxe.VecteurAxe()
        if(Vecteur[0] == 35 and Vecteur[1] == 75):
            Correct = True
        self.assertEqual(Correct, True, "Echec la valeur du vecteur associé à l'axe est fausse")
        
# Ceci lance le test si on exécute le script directement.
if __name__ == '__main__':
    unittest.main()