from TraitementImage import Axe

class GestionAxes():
    
    def __init__(self):
        self.ListAxes = []
            
    def getListAxes(self):
        return self.ListAxes
    
    # retourne un objet Axe suivant sa position dans la liste des axes
    def InfosAxe(self, NumeroAxe):
        return self.ListAxes[NumeroAxe]
            
    def AjouterPoint(self, Xpoint, Ypoint):
        # Si aucun axe n'est créé ou que le dernier axe créé est complet (possède son point d'arrivé), alors on créé un nouvel axe et on lui met son point de départ
        if(self.NombreAxes() < 1  or self.ListAxes[self.NombreAxes() - 1].getPointArrive() != None):
            self.ListAxes.append(Axe.Axe(Xpoint, Ypoint))
        else: # Sinon, c'est que le point que l'on va rajouter va correspondre au point d'arrivé du dernier axe de la liste (celui qui n'est pas complété)
            self.ListAxes[self.NombreAxes() - 1].AjoutPointArrive(Xpoint, Ypoint)
        
    # cette méthode est utilisé pour connaître les coordonnees du dernier point que l'utilisateur a placé pour effectuer une duplication d'axe (donc forcement un axe qui ne possède pas de point d'arrivée)
    def PositionDernierPointDepart(self):
        return self.ListAxes[self.NombreAxes() - 1].getPointDepart().getCoordonnees();
        
    def NombreAxes(self):
        return len(self.ListAxes)
    
    # méthode permettant de savoir si le derier axe dans la liste est complet (un point de départ ET surtout d'arrivé sont défini)
    def DernierAxeComplet(self):
        EstIlComplet = True
        # Si le point d'arrivé du dernier axe n'existe pas, c'est qu'il n'est pas complet
        if (self.NombreAxes() < 1 or self.ListAxes[self.NombreAxes() - 1].getPointArrive() == None):
            EstIlComplet = False
        
        return EstIlComplet
    
    # retourne les coordonnees de l'axe choisi sous la forme
    # XDepart, YDepart, XArrive, YArrive
    def CoordonneesAxe(self, NumeroAxe):
        return self.ListAxes[NumeroAxe].getCoordonneAxe()
            
    def CoordonneesDernierAxe(self):
        return self.CoordonneesAxe(self.NombreAxes() - 1)
    
    def VecteurAxe(self, NumeroAxe):
        return self.ListAxes[NumeroAxe].VecteurAxe();
    
    # Attention ici on met un -2 !
    # le décalage de 1 (la numérotation commence à 0) + le faite d'un axe non terminé (un seul des point est placé) est considéré tout de même comme un axe
    # Hors le vecteur ne peux se déterminer que sur un axe complet → -2
    def VecteurDernierAxe(self):
        return self.VecteurAxe(self.NombreAxes() - 2)
    
    def SupprimerAxes(self, NumeroAxe):
        del self.ListAxes[NumeroAxe]
        
    def SupprimerDernierAxe(self):
        self.SupprimerAxes(self.NombreAxes() - 1)
        
    def SupprimerTousAxes(self):
        del self.ListAxes[:]
        