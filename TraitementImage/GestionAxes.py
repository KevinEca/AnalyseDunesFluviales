from TraitementImage import Axe

class GestionAxes():
    
    def __init__(self):
        self.ListeAxes = []
            
    def getListeAxes(self):
        return self.ListeAxes
    
    # retourne un objet Axe suivant sa position dans la liste des axes
    def InfosAxe(self, NumeroAxe):
        return self.ListeAxes[NumeroAxe]
            
    def AjouterPoint(self, Xpoint, Ypoint):
        PointAjoute = True
        # Si aucun axe n'est créé ou que le dernier axe créé est complet (possède son point d'arrivé), alors on créé un nouvel axe et on lui met son point de départ
        if(self.NombreAxes() < 1  or self.ListeAxes[self.NombreAxes() - 1].getPointArrive() != None):
            self.ListeAxes.append(Axe.Axe(Xpoint, Ypoint))
        else: # Sinon, c'est que le point que l'on va rajouter va correspondre au point d'arrivé du dernier axe de la liste (celui qui n'est pas complété)
            PointDepartAxe = self.PositionDernierPointDepart()
            # Si le point que l'on s'apprête a ajouter est le deuxième d'un axe, et qu'il se trouve au même endroit que le premier
            # Alors on empêche la création de ce point
            if PointDepartAxe[0] == Xpoint and PointDepartAxe[1] == Ypoint:
                PointAjoute = False
            else:
                self.ListeAxes[self.NombreAxes() - 1].AjoutPointArrive(Xpoint, Ypoint)
        return PointAjoute
    
    # cette méthode est utilisé pour connaître les coordonnees du dernier point que l'utilisateur a placé pour effectuer une duplication d'axe (donc forcement un axe qui ne possède pas de point d'arrivée)
    def PositionDernierPointDepart(self):
        return self.ListeAxes[self.NombreAxes() - 1].getCoordonneesPointDepart();
        
    def NombreAxes(self):
        return len(self.ListeAxes)
    
    # méthode permettant de savoir si le dernier axe dans la liste est complet (les points de départ ET surtout d'arrivés sont définis)
    def DernierAxeComplet(self):
        EstIlComplet = True
        # Si le point d'arrivé du dernier axe n'existe pas, c'est qu'il n'est pas complet
        if (self.NombreAxes() < 1 or self.ListeAxes[self.NombreAxes() - 1].getPointArrive() == None):
            EstIlComplet = False
        
        return EstIlComplet
    
    # retourne les coordonnees de l'axe choisi sous la forme
    # XDepart, YDepart, XArrive, YArrive
    # Si le numéro d'axe indiqué ne correspond pas à la liste, le dernier élément de la liste sera prit
    def CoordonneesAxe(self, NumeroAxe):
        if not NumeroAxe > self.NombreAxes() and NumeroAxe >= 0:
            return self.ListeAxes[NumeroAxe].getCoordonneesAxe()
        else:
            return self.CoordonneesDernierAxe()
            
    def CoordonneesDernierAxe(self):
        return self.CoordonneesAxe(self.NombreAxes() - 1)
    
    def VecteurAxe(self, NumeroAxe):
        return self.ListeAxes[NumeroAxe].VecteurAxe();
    
    def VecteurDernierAxe(self):
        if(self.DernierAxeComplet()):
            return self.VecteurAxe(self.NombreAxes() - 1)
        else:
            # Attention ici on met un -2 !
            # le décalage de 1 (la numérotation commence à 0) + le faite d'un axe non terminé (un seul des point est placé) est considéré tout de même comme un axe (dans le nombre d'axes)
            # Hors le vecteur ne peux se déterminer que sur un axe complet → -2
            return self.VecteurAxe(self.NombreAxes() - 2)
    
    def SupprimerAxe(self, NumeroAxe):
        del self.ListeAxes[NumeroAxe]
        
    def SupprimerDernierAxe(self):
        self.SupprimerAxe(self.NombreAxes() - 1)
        
    def SupprimerTousAxes(self):
        del self.ListeAxes[:]
        