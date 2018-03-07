from math import sqrt, ceil
from numpy import asmatrix
from TraitementImage import ImageDune, GestionAxes

def TableauAltitudeDistance(NumeroAxe, MonImage = None, LesAxes = None, ImageAffichage = [0]):
    # On prepare les listes des coordonnées X et Y (distance par rapport au point de départ et altitude respectivement)
    ListeDistance = []
    ListeAltitude = []
        
    ImageOrigine = asmatrix(MonImage.getImage())
    AltitudeMinimum = MonImage.AltitudeMin
    ResolutionImage = float(MonImage.getResolutionAltitude())
        
    # On prélève les deux points définissant le tracé de l'axe
    PointA = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    PointB = LesAxes.InfosAxe(NumeroAxe).getPointArrive().getCoordonnees()
    
    # Si le courant va de droite à gauche (vers la gauche), le point A est celui le plus à droite des 2 (à verticalité égale, il est le plus en bas)
    if(MonImage.getSensCourant() == True):
        if(PointA[0] < PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    else:
        # Sinon (courant de gauche à droite) on fait en sorte que le point A à gauche de B
        # (il est le plus haut placé des 2. Et si ils sont à la même hauteur, c'est celui le plus à gauche)     
        if(PointA[0] > PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
        
    # Nous avons maintenant les points de départ et d'arrivée (sur la miniature)
    # transposons les coordonnées des points de la miniature affichée sur l'image en taille réelle
    # le ratio de l'image étant conservé, on n'a pas besoin de regarder le nombre de lignes et colonne de l'image d'origine et sa miniature
    # seuls les nombres de lignes OU de colonnes suffisent (pour les 2 images bien évidemment)
    PointDepart = []
    PointArrive = []
    PointDepart.append(int(PointA[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointDepart.append(int(PointA[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
        
    #print("Départ : " + str(PointDepart))
    #print("Arrivé : " + str(PointArrive))
        
    # Regardons le nombre de pixels à l'horizontal/vertical pour passer du point de départ à l'arrivée
    DistanceX = abs(PointArrive[0] - PointDepart[0])
    DistanceY = abs(PointArrive[1] - PointDepart[1])
    
    # Suivant la direction du courant la boucle utilisé sera légèrement différente, d'où l'existence de ce if
    if(MonImage.getSensCourant() == True):
        # Suivant quelle distance Horizontale ou verticale du vecteur est la plus grande, on détermine sur quelle dimension on parcours le vecteur par cran de 1
        if(DistanceX >= DistanceY):
            # Notre point de référence (ici vertical) correspond à l'initialisation à la position verticale du point de départ
            PositionYReference = PointDepart[1]
            # C'est deux variables sont pour définir le premier et dernier pixels horizontales pour la boucle (initialisation et condition de sortie)
            PositionXDepart = PointDepart[0]
            PositionXArrive = PointArrive[0]
            # Cette variable indique de combien devrait-on se déplacer sur la vertical si l'on se déplace de 1 en horizontal
            # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
            # il sera utilisé avec la position verticale de référence pour déterminer le niveau vertical du pixel le plus adapté à prendre
            IncrementVertical = DistanceY / DistanceX
        
            # Si le point de départ est verticalement plus faible (positionné plus haut dans l'image) que le point d'arrivé
            if(PointDepart[1] < PointArrive[1]):
                # Pour chacun des pixels parcourus horizontalement (car DistanceX > DistanceY)
                # Comme ici nous allons de droite vers la gauche, nous nous déplacons en réduisant la valeur des coordonnées (d'où le -1)              
                for X in range (PositionXDepart, PositionXArrive, -1):
                    # On caste donc en int pour avoir une coordonnées vertiale du tableau de l'image
                    # c'est la coordonnée choisie de base pour détermniter sur quelle ligne (verticalité) prendre le pixel sur la colonne X de l'image
                    PositionPixelVertiChoisi = int(PositionYReference)
                    # Comme PointDepart[1] < PointArrive[1]
                    # notre position de référence est donc augmenté de la valeur incrémentale
                    # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                    PositionYReference += IncrementVertical
                       
                    # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau vertical précédemment ou non
                    if PositionYReference > (PositionPixelVertiChoisi + 1 + (IncrementVertical/2)):
                            PositionPixelVertiChoisi += 1
                            
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2))
            else:                
                for X in range (PositionXDepart, PositionXArrive, -1):
                    PositionPixelVertiChoisi = int(PositionYReference)
                    # Comme PointDepart[1] > PointArrive[1]
                    # notre position de référence est donc diminuée de la valeur incrémentale
                    # Ainsi nous diminuons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                    PositionYReference -= IncrementVertical
                    if PositionYReference < (PositionPixelVertiChoisi - 1 - (IncrementVertical/2)):
                            PositionPixelVertiChoisi -= 1
                            
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2))
        else:
            # Ici c'est que le nombre de pixels à parcourir sur la verticale est plus grand que le nombre pour l'horizontal
            # Notre point de référence (ici horizontal) correspond donc à l'initialisation à la position horizontale du point de départ
            PositionXReference = PointDepart[0]
            # C'est deux variables sont pour définir le premier et dernier pixels verticales pour la boucle (initialisation et condition de sortie)
            PositionYDepart = PointDepart[1]
            PositionYArrive = PointArrive[1]
            # Cette variable indique de combien devrait-on se déplacer à l'horizontal si l'on se déplace de 1 en vertical
            # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
            # il sera utilisé avec la position de référence pour déterminer le niveau horizontal du pixel le plus adapté
            IncrementHorinzontal = DistanceX / DistanceY
            
            if(PointDepart[1] < PointArrive[1]):
                # Pour chacun des pixels parcourus verticalement (car DistanceY > DistanceX)                
                for Y in range (PositionYDepart, PositionYArrive, +1):
                    # On caste donc en int pour avoir une coordonnées horzontale du tableau de l'image
                    # c'est la coordonnée choisie de base pour détermniter sur quelle colonne (horizontalité) prendre le pixel sur la ligne Y de l'image
                    PositionPixelHoriChoisi = int(PositionXReference)
                    # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                    # notre position de référence est donc réduite de la valeur incrémentale
                    # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                    PositionXReference -= IncrementHorinzontal
                    
                    # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                    if PositionXReference < (PositionPixelHoriChoisi - 1 - (IncrementHorinzontal/2)):
                            PositionPixelHoriChoisi -= 1
                    
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
            else:                
                for Y in range (PositionYDepart, PositionYArrive, -1):
                    # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                    # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                    PositionPixelHoriChoisi = int(PositionXReference)
                    PositionXReference -= IncrementHorinzontal
                    
                    # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                    if PositionXReference < (PositionPixelHoriChoisi - 1 - (IncrementHorinzontal/2)):
                            PositionPixelHoriChoisi -= 1
                    
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
    else:
        if(DistanceX >= DistanceY):            
            # Notre point de référence (ici vertical) correspond donc au départ à la position verticale du point de départ
            PositionYReference = PointDepart[1]
            # C'est deux variables sont pour définir le premier et dernier pixels horizontales pour la boucle (initialisation et condition de sortie)
            PositionXDepart = PointDepart[0]
            PositionXArrive = PointArrive[0]
            # Cette variable indique de combien devrait-on se déplacer sur la vertical si l'on se déplace de 1 en horizontal
            # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
            # il sera utilisé avec la position verticale de référence pour déterminer le niveau vertical du pixel le plus adapté à prendre
            IncrementVertical = DistanceY / DistanceX
        
            if(PointDepart[1] < PointArrive[1]):                
                for X in range (PositionXDepart, PositionXArrive, +1):
                    # On caste donc en int pour avoir une coordonnées vertiale du tableau de l'image, c'est la coordonnée choisi de base (qui peux être décrémenté par la suite)
                    PositionPixelVertiChoisi = int(PositionYReference)
                    PositionYReference += IncrementVertical
                        
                    if PositionYReference > (PositionPixelVertiChoisi + 1 + (IncrementVertical/2)):
                            PositionPixelVertiChoisi += 1
                            
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2 ))
            else:                
                for X in range (PositionXDepart, PositionXArrive, +1):
                    # On caste donc en int pour avoir une coordonnées vertiale du tableau de l'image, c'est la coordonnée choisi de base (qui peux être décrémenté par la suite)
                    PositionPixelVertiChoisi = int(PositionYReference)
                    PositionYReference -= IncrementVertical
                        
                    if PositionYReference < (PositionPixelVertiChoisi - 1 - (IncrementVertical/2)):
                            PositionPixelVertiChoisi -= 1
                            
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2 ))
        else:
            PositionXReference = PointDepart[0]
            # C'est deux variables sont pour définir le début et la fin des pixels vertical (d'où le 1) à parcourir
            PositionYDepart = PointDepart[1]
            PositionYArrive = PointArrive[1]
            # Cette variable indique de combien devrait-on se déplacer à l'horizontal si l'on se déplace de 1 en vertical
            # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
            # il sera utilisé avec la position de référence pour déterminer le niveau horizontal du pixel le plus adapté
            IncrementHorinzontal = DistanceX / DistanceY
            
            if(PointDepart[1] < PointArrive[1]):
                for Y in range (PositionYDepart, PositionYArrive, +1):
                    # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                    # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                    PositionPixelHoriChoisi = int(PositionXReference)
                    # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                    # notre position de référence est donc réduite de la valeur incrémentale
                    # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                    PositionXReference += IncrementHorinzontal
                    
                    # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                    if PositionXReference > (PositionPixelHoriChoisi + 1 + (IncrementHorinzontal/2)):
                            PositionPixelHoriChoisi += 1
                    
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
            else:                
                for Y in range (PositionYDepart, PositionYArrive, -1):
                    # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                    # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                    PositionPixelHoriChoisi = int(PositionXReference)
                    # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                    # notre position de référence est donc réduite de la valeur incrémentale
                    # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                    PositionXReference += IncrementHorinzontal
                    
                    # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                    if PositionXReference > (PositionPixelHoriChoisi + 1 + (IncrementHorinzontal/2)):
                            PositionPixelHoriChoisi += 1
                    
                    # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                    ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                    # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                    ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
    
    # On retourne les deux listes de données
    return ListeDistance, ListeAltitude
    

def TableauAltitudeDistance3(NumeroAxe, MonImage = None, LesAxes = None, ImageAffichage = [0]):
    # On prepare les listes des coordonnées X et Y (distance par rapport au point de départ et altitude respectivement)
    ListeDistance = []
    ListeAltitude = []
        
    ImageOrigine = asmatrix(MonImage.getImage())
    AltitudeMinimum = MonImage.AltitudeMin
    ResolutionImage = float(MonImage.getResolutionAltitude())
        
    # On prélève les deux points définissant le tracé de l'axe
    PointA = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    PointB = LesAxes.InfosAxe(NumeroAxe).getPointArrive().getCoordonnees()

    # Si le courant va de droite à gauche (vers la gauche), le point A est celui le plus à droite des 2 (à verticalité égale, il est le plus en bas)
    if(MonImage.getSensCourant() == True):
        if(PointA[0] < PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    else:
        # Sinon (courant de gauche à droite) on fait en sorte que le point A à gauche de B
        # (il est le plus haut placé des 2. Et si ils sont à la même hauteur, c'est celui le plus à gauche)     
        if(PointA[0] > PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
        
    # Nous avons maintenant les points de départ et d'arrivée (sur la miniature)
    # transposons les coordonnées des points de la miniature affichée sur l'image en taille réelle
    # le ratio de l'image étant conservé, on n'a pas besoin de regarder le nombre de lignes et colonne de l'image d'origine et sa miniature
    # seuls les nombres de lignes OU de colonnes suffisent (pour les 2 images bien évidemment)
    PointDepart = []
    PointArrive = []
    PointDepart.append(int(PointA[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointDepart.append(int(PointA[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
        
    #print("Départ : " + str(PointDepart))
    #print("Arrivé : " + str(PointArrive))
        
    # Regardons le nombre de pixel à l'horizontal/vertical pour passer du point de départ à l'arrivée
    DistanceX = PointArrive[0] - PointDepart[0]
    DistanceY = PointArrive[1] - PointDepart[1]
    
    if(MonImage.getSensCourant() == False):
        
        # Suivant laquelle des 2 valeurs est la plus grande, nous allons parcourir le l'image avec l'horizontalité ou la verticalité comme référence
        if (DistanceX > DistanceY):
            # Si la distance horizontale est la plus grande,
            # alors c'est que l'on va l'incrémenter de 1 à chaque fois (boucle for) et regarder si sur la verticale on doit utiliser la ligne suivante ou non (celle en dessous)
                
            # On initialise la position y au niveau de la ligne du pixel de départ
            PositionY = PointDepart[1]
            # Cette variable indique de combien devrait-on se déplacer sur la vertical si l'on augmente de 1 en horizontal
            # comme il y a de forte chance que ce nombre n'est pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple,
            # on l'utilisera pour savoir le pixel le plus adapté
            IncrementVertical = DistanceY / DistanceX
                
            # pour chaque niveau horizontal (colonne de l'image entre le point de départ et celui d'arrivée) 
            for X in range (PointDepart[0], PointArrive[0]):
                # On regarde si l'on doit prendre le pixel de la ligne suivante ou non 
                # Exemples : 
                # PositionY = 8,1 et IncrementVertical = 0.3 → on obtient 8,4, ce nombre est plus proche de 8 que de 9 donc on va prendre le pixel sur la 8ème colonne
                # PositionY = 8,4 et IncrementVertical = 0.4 → on obtient 8,8, ce qui est plus proche de 9, d'oà¹ le faite que l'on prend le pixel sur la 9ème colonne
                PixelVerticalChoisi = int(PositionY)
                if(PositionY + IncrementVertical) > (PixelVerticalChoisi + 0.5):
                    PixelVerticalChoisi += 1
                    
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PixelVerticalChoisi, X])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PixelVerticalChoisi - PointDepart[1]) ** 2 ))
                        
                # Pour chaque passage à la colonne suivante, on incrémente la position verticale de sa valeur préalablement calculée 
                PositionY += IncrementVertical
        else:
            # Si la distance verticale est la plus grande,
            # alors c'est que l'on va l'incrémenter de 1 à chaque fois (boucle for) et regarder si sur l'horizontale on doit utiliser la colonne suivante ou non(à droite)
                
            # On initialise la position x au niveau de la colonne du pixel de départ
            PositionX = PointDepart[0]
            # Cette variable indique de combien devrait-on se déplacer sur l'horizontal si l'on augmente de 1 en verticale (passage à la ligne en dessous)
            # comme il y a de forte chance que ce nombre n'est pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple,
            # on l'utilisera pour savoir le pixel le plus adapté
            IncrementHorizontal = DistanceX / DistanceY
                
            # pour chaque niveau vertical (ligne de l'image entre le point de départ et celui d'arrivée) 
            for Y in range (PointDepart[1], PointArrive[1]):
                PixelHorizontalChoisi = int(PositionX)
                if(PositionX + IncrementHorizontal) > (PixelHorizontalChoisi + 0.5):
                    PixelHorizontalChoisi += 1
                        
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PixelHorizontalChoisi])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((PixelHorizontalChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
                    
                # Pour chaque passage à la ligne suivante, on incrémente la position horizontale de sa valeur préalablement calculée 
                PositionX += IncrementHorizontal
            
    else:
        # Suivant laquelle des 2 valeurs est la plus grande, nous allons parcourir le l'image avec l'horizontalité ou la verticalité comme référence
        if (DistanceX > DistanceY):
            # Si la distance horizontale est la plus grande,
            # alors c'est que l'on va l'incrémenter de 1 à chaque fois (boucle for) et regarder si sur la verticale on doit utiliser la ligne suivante ou non (celle en dessous)
                
            # On initialise la position y au niveau de la ligne du pixel de départ
            PositionY = PointDepart[1]
            # Cette variable indique de combien devrait-on se déplacer sur la vertical si l'on augmente de 1 en horizontal
            # comme il y a de forte chance que ce nombre n'est pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple,
            # on l'utilisera pour savoir le pixel le plus adapté
            IncrementVertical = DistanceY / DistanceX
                
            # pour chaque niveau horizontal (colonne de l'image entre le point de départ et celui d'arrivée) 
            for X in range (PointDepart[0], PointArrive[0]):
                # On regarde si l'on doit prendre le pixel de la ligne suivante ou non 
                # Exemples : 
                # PositionY = 8,1 et IncrementVertical = 0.3 → on obtient 8,4, ce nombre est plus proche de 8 que de 9 donc on va prendre le pixel sur la 8ème colonne
                # PositionY = 8,4 et IncrementVertical = 0.4 → on obtient 8,8, ce qui est plus proche de 9, d'oà¹ le faite que l'on prend le pixel sur la 9ème colonne
                PixelVerticalChoisi = int(PositionY)
                if(PositionY + IncrementVertical) > (PixelVerticalChoisi + 0.5):
                    PixelVerticalChoisi += 1
                    
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PixelVerticalChoisi, X])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PixelVerticalChoisi - PointDepart[1]) ** 2 ))
                        
                # Pour chaque passage à la colonne suivante, on incrémente la position verticale de sa valeur préalablement calculée 
                PositionY += IncrementVertical
        else:
            # Si la distance verticale est la plus grande,
            # alors c'est que l'on va l'incrémenter de 1 à chaque fois (boucle for) et regarder si sur l'horizontale on doit utiliser la colonne suivante ou non(à droite)
                
            # On initialise la position x au niveau de la colonne du pixel de départ
            PositionX = PointDepart[0]
            # Cette variable indique de combien devrait-on se déplacer sur l'horizontal si l'on augmente de 1 en verticale (passage à la ligne en dessous)
            # comme il y a de forte chance que ce nombre n'est pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple,
            # on l'utilisera pour savoir le pixel le plus adapté
            IncrementHorizontal = DistanceX / DistanceY
                
            # pour chaque niveau vertical (ligne de l'image entre le point de départ et celui d'arrivée) 
            for Y in range (PointDepart[1], PointArrive[1]):
                PixelHorizontalChoisi = int(PositionX)
                if(PositionX + IncrementHorizontal) > (PixelHorizontalChoisi + 0.5):
                    PixelHorizontalChoisi += 1
                        
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PixelHorizontalChoisi])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((PixelHorizontalChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
                    
                # Pour chaque passage à la ligne suivante, on incrémente la position horizontale de sa valeur préalablement calculée 
                PositionX += IncrementHorizontal
        
        
    # On retourne les deux listes de données
    return ListeDistance, ListeAltitude
    

def TableauAltitudeDistance2(NumeroAxe, MonImage = None, LesAxes = None, ImageAffichage = [0]):
    # On prepare les listes des coordonnées X et Y (distance par rapport au point de départ et altitude respectivement)
    ListeDistance = []
    ListeAltitude = []
        
    ImageOrigine = asmatrix(MonImage.getImage())
    AltitudeMinimum = MonImage.AltitudeMin
    ResolutionImage = float(MonImage.getResolutionAltitude())
        
    # On prélève les deux points définissant le tracé de l'axe
    PointA = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    PointB = LesAxes.InfosAxe(NumeroAxe).getPointArrive().getCoordonnees()
    
    # Si le courant va de droite à gauche (vers la gauche), le point A est celui le plus à droite des 2 (à verticalité égale, il est le plus en bas)
    if(MonImage.getSensCourant() == True):
        if(PointA[0] < PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
    else:
        # Sinon (courant de gauche à droite) on fait en sorte que le point A à gauche de B
        # (il est le plus haut placé des 2. Et si ils sont à la même hauteur, c'est celui le plus à gauche)     
        if(PointA[0] > PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = LesAxes.InfosAxe(NumeroAxe).getPointDepart().getCoordonnees()
        
    # Nous avons maintenant les points de départ et d'arrivée (sur la miniature)
    # transposons les coordonnées des points de la miniature affichée sur l'image en taille réelle
    # le ratio de l'image étant conservé, on n'a pas besoin de regarder le nombre de lignes et colonne de l'image d'origine et sa miniature
    # seuls les nombres de lignes OU de colonnes suffisent (pour les 2 images bien évidemment)
    PointDepart = []
    PointArrive = []
    PointDepart.append(int(PointA[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointDepart.append(int(PointA[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[0] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
    PointArrive.append(int(PointB[1] * ImageOrigine.shape[0] / ImageAffichage.size[1]))
        
    #print("Départ : " + str(PointDepart))
    #print("Arrivé : " + str(PointArrive))
        
    # Regardons le nombre de pixels à l'horizontal/vertical pour passer du point de départ à l'arrivée
    DistanceX = abs(PointArrive[0] - PointDepart[0])
    DistanceY = abs(PointArrive[1] - PointDepart[1])
    
    # Si le nombre de pixels à l'horizontale à parcourir est plus grand que le nombre de pixels à la verticale
    # Alors, nous allons déterminer la position verticale du pixel pour chaque pixel à l'horizontal parcourue 
    if(DistanceX >= DistanceY):
        # Notre point de référence (ici vertical) correspond donc au départ à la position verticale du point de départ
        PositionYReference = PointDepart[1]
        # C'est deux variables sont pour définir le début et la fin des pixels horizontales (d'où le 0) à parcourir
        PositionXDepart = PointDepart[0]
        PositionXArrive = PointArrive[0]
        # Cette variable indique de combien devrait-on se déplacer sur la vertical si l'on se déplace de 1 en horizontal
        # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
        # il sera utilisé avec la position de référence pour déterminer le niveau vertical du pixel le plus adapté
        IncrementVertical = DistanceY / DistanceX
        
        # Suivant la direction du courant la boucle est légèrement différente, d'où l'existence de ce if
        if(MonImage.getSensCourant() == True):
            # Pour chacun des pixels parcourus horizontalement (car DistanceX > DistanceY)
            # Comme ici nous allons de droite vers la gauche, nous nous déplacons en réduisant la valeur des coordonnées (d'où le -1)
            for X in range (PositionXDepart, PositionXArrive, -1):
                # On caste donc en int pour avoir une coordonnées vertiale du tableau de l'image, c'est la coordonnée choisi de base (qui peux être décrémenté par la suite)
                PositionPixelVertiChoisi = int(PositionYReference)
                # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                # notre position de référence est donc réduite de la valeur incrémentale
                # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                PositionYReference -= IncrementVertical
                
                # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non
                # Prenons par exemple : IncrementVertical = 0.3
                # Itération 1: PositionYReference = 8.3 → on obtient 8.0 ,on est toujours dans le pixel à la position 8
                # PositionYReference = 8.0  → 7.7 ,on est passé à un niveau inférieur avec plus de la moitié de IncrementDeplacement (ici sa totalité 0.3) les pixels seront donc pris au niveau 7
                # PositionYReference = 7.7 - 0.3 → on obtient 7.4 ,on garde le niveau 7
                # PositionYReference = 7.4 - 0.3 → on obtient 7.1 ,on garde le niveau 7
                # PositionYReference = 7.1 - 0.3 → on obtient 6.8 ,on passe à un niveau inférieur avec 0.2 (soit > 1.5), les pixels seront au niveau 6
                # PositionYReference = 6.8 - 0.3 → 6.5 le niveau reste 6
                # PositionYReference = 6.5 - 0.3 → 6.2 le niveau reste à 6
                # PositionYReference = 6.2 - 0.3 → 5.9 le niveau reste à 6 (0.1 < (0.3/2))
                # PositionYReference = 5.9 - 0.3 → 5.6 le niveau passe à 5 (0.4 > (0.3/2))
                    
                if PositionYReference < (PositionPixelVertiChoisi - 1 - (IncrementVertical/2)):
                        PositionPixelVertiChoisi -= 1
                
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2 ))
            
            print(PositionYReference) 
        else:
            for X in range (PositionXDepart, PositionXArrive, +1):
                # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                PositionPixelVertiChoisi = int(PositionYReference)
                # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                # notre position de référence est donc réduite de la valeur incrémentale
                # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                PositionYReference += IncrementVertical
                    
                if PositionYReference > (PositionPixelVertiChoisi + 1 + (IncrementVertical/2)):
                    PositionPixelVertiChoisi += 1
                
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[PositionPixelVertiChoisi, X])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((X - PointDepart[0]) ** 2 + (PositionPixelVertiChoisi - PointDepart[1]) ** 2 ))
            
    else:
        # Ici c'est que le nombre de pixels à parcourir sur la verticale est plus grand que le nombre pour l'horizontal
        # Notre point de référence (ici vertical) correspond donc au départ à la position verticale du point de départ
        PositionXReference = PointDepart[0]
        # C'est deux variables sont pour définir le début et la fin des pixels vertical (d'où le 1) à parcourir
        PositionYDepart = PointDepart[1]
        PositionYArrive = PointArrive[1]
        # Cette variable indique de combien devrait-on se déplacer à l'horizontal si l'on se déplace de 1 en vertical
        # comme il y a de forte chance que ce nombre ne soit pas un entier, on se retrouvera avec des décalages de 0.4 pixel par exemple
        # il sera utilisé avec la position de référence pour déterminer le niveau horizontal du pixel le plus adapté
        IncrementHorinzontal = DistanceX / DistanceY
    
        # Suivant la direction du courant la boucle est légèrement différente, d'où l'existence de ce if
        if(MonImage.getSensCourant() == True):
            # Pour chacun des pixels parcourus (en horizontal ou vertical, cela est déterminé juste avant)
            # Comme ici nous allons de droite vers la gauche, nous nous déplacons en réduisant la valeur des coordonnées (d'où le -1)
            for Y in range (PositionYDepart, PositionYArrive, -1):
                # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                PositionPixelHoriChoisi = int(PositionXReference)
                # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                # notre position de référence est donc réduite de la valeur incrémentale
                # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                PositionXReference -= IncrementHorinzontal
                
                # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                if PositionXReference < (PositionPixelHoriChoisi - 1 - (IncrementHorinzontal/2)):
                        PositionPixelHoriChoisi -= 1
                
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
        else:
            for Y in range (PositionYDepart, PositionYArrive, +1):
                # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
                # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
                PositionPixelHoriChoisi = int(PositionXReference)
                # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
                # notre position de référence est donc réduite de la valeur incrémentale
                # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
                PositionXReference += IncrementHorinzontal
                
                # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
                if PositionXReference > (PositionPixelHoriChoisi + 1 + (IncrementHorinzontal/2)):
                    PositionPixelHoriChoisi += 1
                
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(AltitudeMinimum + ResolutionImage * ImageOrigine[Y, PositionPixelHoriChoisi])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((PositionPixelHoriChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))

    # On retourne les deux listes de données
    return ListeDistance, ListeAltitude
    
def DetectionDunesAxe(NumeroAxe, MonImage = None, LesAxes = None, ImageAffichage = [0], SeuilDetectionDune = 0, ListeDune = []):
    AltitudeMinimum = MonImage.getAltitudeMin()
    ResolutionImage = float(MonImage.getResolutionAltitude())
    
    #print("ResolutionImage = " + str(ResolutionImage))
        
    # Le seuil de hauteur minimum pour qualifier de dune
    # On ne peut pas directement exploiter la données renseignées par l'utilisateur du programme
    # On utilise donc le plus petit multiple de la résolution de l'image qui puisse au moins faire la hauteur désignée
    SeuilDetection = ceil(SeuilDetectionDune / ResolutionImage) * ResolutionImage
    # On calcul la valeur de l'altitude maximum, celle qui signifie que l'on est en surface
    AltitudeMax = AltitudeMinimum + ResolutionImage * 255
    ListeDistance, ListeAltitude = TableauAltitudeDistance(NumeroAxe, MonImage, LesAxes, ImageAffichage)
        
    IdDune = 0
        
    # indice de parcours des tableaux
    i = 0
    NombreElements = len(ListeAltitude)
    PrecedenteValeur = 255
        
    # On enlève toutes les valeurs d'altitude maximal au debut (ne sont pas associé à des dunes, c'est du blanc → la surface)
    while( i < NombreElements and ListeAltitude[i] == AltitudeMax):
        i += 1
        
    # On cherche ensuite à atteindre un minimum (qui sera le premier creux de la dune)
    while(i < NombreElements and ListeAltitude[i] <= PrecedenteValeur):
        PrecedenteValeur = ListeAltitude[i]
        i += 1
            
    # Maintenant pour tout les autres données restantes du tableau
    while (i < NombreElements):
            
        ProfondeurDune1 = ListeAltitude[i - 1]  # 'i - 1' car à l'indice 'i' on ne respecte plus la condition (la valeur mesuré diminue continuellement)
        Distance1 = 0
            
        while(i < NombreElements and ListeAltitude[i] >= PrecedenteValeur):
            Distance1 += 1
            PrecedenteValeur = ListeAltitude[i]
            i += 1
            
        # Si le pic de la dune possède le niveau d'altitude maximal, c'est que nous sommes en surface → ce n'est pas une dune !
        if(ListeAltitude[i - 1] == AltitudeMax):
            Distance1 = 0
            
        PicDune = ListeAltitude[i - 1]  # 'i - 1' car à l'indice 'i' on ne respecte plus la condition (la valeur mesuré augmente continuellement)
        Distance2 = 0
            
        while(i < NombreElements and ListeAltitude[i] <= PrecedenteValeur):
            Distance2 += 1
            PrecedenteValeur = ListeAltitude[i]
            i += 1
            
        ProfondeurDune2 = ListeAltitude[i - 1]  # 'i - 1' car à l'indice 'i' on ne respecte plus la condition (la valeur mesuré diminue continuellement)
    
        # Pour que l'on puisse juger si ce que l'on vient d'inspecter peut-être une dune, on peut déjà vérifier les distances mesurés
        if(Distance1 != 0 and Distance2 != 0):
            if(Distance1 < Distance2):
                HauteurDune = PicDune - ProfondeurDune1
            elif(Distance2 < Distance1):
                HauteurDune = PicDune - ProfondeurDune2
            else:
                HauteurDune = PicDune - ((ProfondeurDune1 + ProfondeurDune2) / 2)
            
            LongeurOnde = min(Distance1, Distance2)
            
            #print("Distance1 = " + str(Distance1) + " Distance2 = " + str(Distance2))
            #print("HautPic = " + str(PicDune) + " ProfondeurDune1 = " + str(ProfondeurDune1) + " ProfondeurDune2 = " + str(ProfondeurDune2))
            #print("Hauteur dune = " + str(HauteurDune) + " Longueur d'onde = " + str(LongeurOnde))
                
            if(HauteurDune >= SeuilDetection):
                # * 100 pour mettre en cm
                ListeDune.append([NumeroAxe, IdDune, LongeurOnde, round(HauteurDune * 100, 2)])
                IdDune += 1 # On incrémente l'identifiant de la dune
                    
    return ListeDune

def BilanDunesParAxe(ListeDesDunes = [], NombreAxes = 1):
    # Si il y a au moins une dune de référencé dans le tableau
    TableauBilanParAxe = [] # Tableau qui contiendra le nombre de dunes, la longeur d'onde et la hauteur moyenne des dunes par par axe
    
    NombreDeDunesTotal = len(ListeDesDunes)
    j = 0 # Indice de la dune que l'on lit dans le tableau
    
    if (NombreDeDunesTotal > 0):
        IdAxe = ListeDesDunes[j][0] # On commence par lire les dunes faisant partie de celles qui sont rattachées au premier axe ayant au moins une dune
        
        for i in range (0, NombreAxes): # Pour chaqu'un des axes pouvant être répertorié
            # Si nous sommes sur un axe qui ne possède pas de dune, Le tableau contiendra un ligne associé à cette axe avec des 0 comme résultats (nombre de dune, longeur d'onde moyenne, hauteur moyenne)
            if i != IdAxe:
                TableauBilanParAxe.append([i,0,0,0])
            else:
                # On prépare de quoi calculer les paramètres des dunes de l'axe concerné
                NombreDuneAxe = 0
                LongueurOndeMoyenneAxe = 0
                HauteurMoyenneAxe = 0
                while(i == IdAxe and j < NombreDeDunesTotal):
                    NombreDuneAxe += 1
                    LongueurOndeMoyenneAxe += ListeDesDunes[j][2]
                    HauteurMoyenneAxe += ListeDesDunes[j][3]
                    j += 1;
                    if (j < NombreDeDunesTotal): # Si nous avons pas atteint la fin du tableau (on incrémente j néanmoins pour sortir du while)
                        IdAxe = ListeDesDunes[j][0] # On passe à la dune suivante dans le tableau
                LongueurOndeMoyenneAxe = round(LongueurOndeMoyenneAxe/NombreDuneAxe, 2)
                HauteurMoyenneAxe = round(HauteurMoyenneAxe/NombreDuneAxe)
                
                TableauBilanParAxe.append([i, NombreDuneAxe, LongueurOndeMoyenneAxe, HauteurMoyenneAxe])
    # Si aucune dune n'est détecté, on ajoute alors des données nulles pour chacun des axes
    else:
        for i in range (0, NombreAxes):
            TableauBilanParAxe.append([i,0,0,0])
        
    return TableauBilanParAxe
            
def DetectionDunes(MonImage = None, LesAxes = None, ImageAffichage = [0], SeuilDetectionDune = 0):
    ListeTouteDunes = []
    for i in range (0, LesAxes.NombreAxes()):
        print(LesAxes.InfosAxe(i).getCoordonneAxe())
        DetectionDunesAxe(i, MonImage, LesAxes, ImageAffichage, SeuilDetectionDune, ListeTouteDunes)
                    
    #ListeTouteDunes = array([[0,0,10,15],[0,1,2,4],[1,2,3,4]])    # valeur test pour des résultats sur 2 tracés
    return ListeTouteDunes