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

        # Cette valeur permet de seuiller quand le passage à la ligne suivante ou non pour le pixel à la colonne X
        SeuilPassageSuivant = 1 + (IncrementVertical/2)
        DirectionIncremet = 1
        DirectionBoucle = 1
            
        # Si le point de départ est verticalement plus faible (positionné plus haut dans l'image) que le point d'arrivé
        if(PointDepart[1] > PointArrive[1]):             
            DirectionIncremet = -1
        
        # Si le sens du courant est de la droite vers la gauche, le pixel de départ est alors plus à droite que celui d'arrivé (Depart[0] > Arive[0])
        # pour la boucle for on effectue une décrémentation
        if(MonImage.getSensCourant() == True):
            DirectionBoucle = -1
            
        for X in range (PositionXDepart, PositionXArrive, DirectionBoucle):
            # On caste donc en int pour avoir une coordonnées vertiale du tableau de l'image
            # c'est la coordonnée choisie de base pour détermniter sur quelle ligne (verticalité) prendre le pixel sur la colonne X de l'image
            PositionPixelVertiChoisi = int(PositionYReference)
            # Comme PointDepart[1] < PointArrive[1]
            # notre position de référence est donc augmenté de la valeur incrémentale
            # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
            PositionYReference += IncrementVertical * DirectionIncremet
                   
            # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau vertical précédemment ou non
            if PositionYReference >= (PositionPixelVertiChoisi + SeuilPassageSuivant * DirectionIncremet):
                PositionPixelVertiChoisi += 1 * DirectionIncremet
                    
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
        IncrementHorizontal = DistanceX / DistanceY
        
        # Cette valeur permet de seuiller quand le passage à la colonne suivante ou non pour le pixel à la ligne Y
        SeuilPassageSuivant = 1 + (IncrementHorizontal/2)
        DirectionBoucle = 1
        DirectionIncremet = 1
            
        if(PointDepart[1] > PointArrive[1]):
            DirectionBoucle = -1
        
        # Si le sens du courant est de la droite vers la gauche, c'est que horizontalement les pixels choisi aurant des valeurs de + en + faible
        # pour tester la position horizon du pixel à prendre, on effectue une décrémentation
        if(MonImage.getSensCourant() == True):
            DirectionIncremet = -1
            
        for Y in range (PositionYDepart, PositionYArrive, DirectionBoucle):
            # On suppose que le pixel que l'on va prendre sera sur le même niveau (horizontal ou vertical, celui qui n'est pas concerné par la boucle for)
            # On caste donc en int pour avoir une coordonnées dadu tableau de l'image
            PositionPixelHoriChoisi = int(PositionXReference)
            # Comme nous sommes dans le cas du courant qui se déplace vers la gauche,
            # notre position de référence est donc réduite de la valeur incrémentale
            # Ainsi nous obtenons la position théorique du pixel que l'on doit prendre (c'est un nombre flottant)
            PositionXReference += IncrementHorizontal * DirectionIncremet
                    
            # Comme notre position théorique est un nombre flottant, nous allons savoir si le pixel que l'on doit prendre est sur le même niveau que précédemment ou non                    
            if PositionXReference >= (PositionPixelHoriChoisi + SeuilPassageSuivant * DirectionIncremet):
                PositionPixelHoriChoisi += 1 * DirectionIncremet
                    
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