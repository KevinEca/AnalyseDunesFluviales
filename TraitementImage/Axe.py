from TraitementImage import Point

class Axe():
    
    def __init__(self, Xpoint1, Ypoint1):
        
        self.PointDepart = Point.Point(Xpoint1, Ypoint1)
        self.PointArrive = None
        
    def AjoutPointArrive(self, Xpoint2, Ypoint2):
        self.PointArrive = Point.Point(Xpoint2, Ypoint2)
            
    def getPointDepart(self):
        return self.PointDepart
    
    def getPointArrive(self):
        return self.PointArrive
    
    def getCoordonneAxe(self):
        return self.PointDepart.getCoordonnees(), self.PointArrive.getCoordonnees()
    
    def VecteurXaxe(self):
        return self.PointArrive.getXpoint() - self.PointDepart.getXpoint()

    def VecteurYaxe(self):
        return self.PointArrive.getYpoint() - self.PointDepart.getYpoint()
    
    def VecteurAxe(self):
        return self.VecteurXaxe(), self.VecteurYaxe()
        
        
        