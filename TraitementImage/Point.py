class Point():
    
    def __init__(self, Xpoint, Ypoint):
        
        self.CoordonneX = Xpoint
        self.CoordonneY = Ypoint
            
    def getXpoint(self):
        return self.CoordonneX
    
    def getYpoint(self):
        return self.CoordonneY
            
    def getCoordonnees(self):
        return self.CoordonneX, self.CoordonneY
        
        