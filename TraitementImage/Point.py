class Point():
    
    def __init__(self, Xpoint, Ypoint):
        
        self.CoordonneeX = Xpoint
        self.CoordonneeY = Ypoint
            
    def getXpoint(self):
        return self.CoordonneeX
    
    def getYpoint(self):
        return self.CoordonneeY
    
    def getCoordonnees(self):
        return self.CoordonneeX, self.CoordonneeY
    
    # Modifier les coordonn�es n'est pas autoris�, on supprime le point et on en cr�� un autre
