import unittest
from TraitementImage import Point

class test_Point(unittest.TestCase):
    
    def testInitialisationPoint(self):
        Correct = False
        MonPoint = Point.Point(15, 25)
        CoordonneesPoint = MonPoint.getCoordonnees()
        if(CoordonneesPoint[0] == 15 and CoordonneesPoint[1] == 25):
            Correct = True
        self.assertEqual(Correct, True, "Echec Initialisation des coordonnées d'un point")

# Ceci lance le test si on exécute le script directement.
if __name__ == '__main__':
    unittest.main()