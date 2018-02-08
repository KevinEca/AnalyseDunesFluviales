from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from scipy import array, shape
import VisualiserProfil
from math import sqrt, ceil
from numpy import asmatrix

ListeCouleurs = ["blue", "red", "sienna", "chartreuse", "darkgreen", "deepskyblue", "crimson", "darkorange", "yellow", "purple"]

class ResultatsAxes(Frame):  

    def __init__(self, fenetre, ImageOriginal = [0], ImageAffiche = [0], SeuilDetectionDune = 0, AltitudeMin = 0, ResolutionNiveauGris = 0, TableauPoints = [0]):
        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.ImageOrigine = asmatrix(ImageOriginal)
        self.ImageAffichage = ImageAffiche
        self.DetectionDune = float(SeuilDetectionDune) / 100
        self.AltitudeMinimum = AltitudeMin
        self.ResolutionImage = float(ResolutionNiveauGris)
        self.TableauCoordonneePoint = TableauPoints
        self.ImageAAfficher = 0 # variable ne pouvant être une variable locale, sinon l'image n'apparaît pas à l'affichage
        self.NombreAxes = int(len(self.TableauCoordonneePoint) / 4)
        
        # Création de nos widgets
        Button(self, text="Export des résultats", command = lambda : self.ExportTXT()).grid(row=0, column=0)
        Button(self, text="Visualisation d'un profil", command = lambda : self.VisualiserProfil()).grid(row=0, column=1)
        Label(self, text="Numéro de l'axe choisi").grid(row=1, column=0)
        
        # Pour que le spinBox puisse fonctionner, il faut qu'il propose 2 valeurs au minimum
        # On regarde donc si l'utilisateur n'a fait qu'un seul axe
        if (self.NombreAxes < 2):
            # Si c'est le cas, on désactive le spinBox, ainsi on force la valeur à 0
            self.NumeroAxeChoisi = Spinbox(self, from_=0, to=1, width = 10, state = 'disabled')
        else:
            self.NumeroAxeChoisi = Spinbox(self, from_=0, to= (self.NombreAxes - 1), width = 10, state = 'readonly')
        self.NumeroAxeChoisi.grid(row=1, column = 1)

        # On place une frame pour y placer notre treeview avec sa barre de défilement vertical
        self.FrameTable = Frame(self, height=255, width = 255, bd=1, relief=SUNKEN)
        self.FrameTable.grid(row=2, column=0, columnspan = 2)
        
        # on crée notre treeview
        self.Table = ttk.Treeview(self.FrameTable, columns=('IdDune', 'LongOnde', 'HautDune'))
        # On lui associe une barre de défilement vertical
        self.VerticalBarreTable = ttk.Scrollbar(self.FrameTable, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.VerticalBarreTable.set)
        self.Table.pack(side=LEFT)
        self.VerticalBarreTable.pack(side=RIGHT, fill = Y)
        
        self.Table.column('#0', width=60, anchor='center')  # la colonne #0 correspond à celle où se trouve les + pour dérouler
        self.Table.column('IdDune', width=100, anchor='center')
        self.Table.heading('IdDune', text='ID Dune')
        self.Table.column('LongOnde', width=150, anchor='center')
        self.Table.heading('LongOnde', text="Longueur d'onde (m)")
        self.Table.column('HautDune', width=140, anchor='center')
        self.Table.heading('HautDune', text="Hauteur dune (cm)")
        
        self.Canevas = Canvas(self)
        self.ImageAAfficher = ImageTk.PhotoImage(self.ImageAffichage)
        self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAAfficher)
        # On redéfini la taille du caneva associé à la miniature de l'image sur l'interface graphique
        self.Canevas.config(width=self.ImageAffichage.size[0], height=self.ImageAffichage.size[1])
        self.Canevas.grid(row=0, column=2, rowspan = 3)
        
        # On place les axes sur la miniatures, mais on les colorie d'une couleur différentes afin de les différencier
        self.PlacementAxes()
        
        # On rempli le tableau des résultats par les données obtenues par analyse de tous les axes tracés par l'utilisateur
        self.RemplirTableauResultats(self.DetectionDunes())
        
    def PlacementAxes(self):
        for i in range (0, self.NombreAxes):
            self.Canevas.create_line(self.TableauCoordonneePoint[4*i : 4*(i + 1)], fill=ListeCouleurs[i])

    def ExportTXT(self):
        pass
    
    def VisualiserProfil(self):
        AxeChoisi = int(self.NumeroAxeChoisi.get())
        XCoordonnee, YCoordonnee = self.TableauAltitudeDistance(AxeChoisi)
        
        fenVisualiseAxe = Toplevel()
        fenVisualiseAxe.title("Profil de l'axe " + str(AxeChoisi) + " - Analyse dunes 2018")
        VisualiserProfil.VisualiserProfil(fenVisualiseAxe, AxeChoisi, ListeCouleurs[AxeChoisi], XCoordonnee, YCoordonnee)
    
    def TableauAltitudeDistance(self, NumeroAxe):
        # On prepare les listes des coordonnées X et Y (distance par rapport au point de départ et altitude respectivement)
        ListeDistance = []
        ListeAltitude = []
        
        # On prélève les deux points définissant le tracé de l'axe
        PointA = self.TableauCoordonneePoint[NumeroAxe * 4 : NumeroAxe * 4 + 2]
        PointB = self.TableauCoordonneePoint[NumeroAxe * 4 + 2 : (NumeroAxe + 1) * 4]
        # On permute leurs données, de telle sorte que le point A soit avant le point B
        # (il est le plus haut placé des 2. Et si ils sont à la même hauteur, c'est celui le plus à gauche)
        if(PointA[0] > PointB[0] or (PointA[0] == PointB[0] and PointA[1] > PointB[1])):
            PointA = PointB
            PointB = self.TableauCoordonneePoint[NumeroAxe * 4 : NumeroAxe * 4 + 2]
        
        # Nous avons maintenant les points de départ et d'arrivée (sur la miniature)
        # transposons les coordonnées des points de la miniature affichée sur l'image en taille réelle
        # le ratio de l'image étant conservé, on n'a pas besoin de regarder le nombre de lignes et colonne de l'image d'origine et sa miniature
        # seuls les nombres de lignes OU de colonnes suffisent (pour les 2 images bien évidemment)
        PointDepart = []
        PointArrive = []
        PointDepart.append(int(PointA[0] * self.ImageOrigine.shape[0] / self.ImageAffichage.size[1]))
        PointDepart.append(int(PointA[1] * self.ImageOrigine.shape[0] / self.ImageAffichage.size[1]))
        PointArrive.append(int(PointB[0] * self.ImageOrigine.shape[0] / self.ImageAffichage.size[1]))
        PointArrive.append(int(PointB[1] * self.ImageOrigine.shape[0] / self.ImageAffichage.size[1]))
        
        #print("Départ : " + str(PointDepart))
        #print("Arrivé : " + str(PointArrive))
        
        # Regardons le nombre de pixel à l'horizontal/vertical pour passer du point de départ à l'arrivée
        DistanceX = PointArrive[0] - PointDepart[0]
        DistanceY = PointArrive[1] - PointDepart[1]
        
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
                # PositionY = 8,4 et IncrementVertical = 0.4 → on obtient 8,8, ce qui est plus proche de 9, d'où le faite que l'on prend le pixel sur la 9ème colonne
                PixelVerticalChoisi = int(PositionY)
                if(PositionY + IncrementVertical) > (PixelVerticalChoisi + 0.5):
                    PixelVerticalChoisi += 1
                
                # On ajoute la valeur du pixel de l'image dans sa liste dédiée
                ListeAltitude.append(self.AltitudeMinimum + self.ResolutionImage * self.ImageOrigine[PixelVerticalChoisi, X])
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
                ListeAltitude.append(self.AltitudeMinimum + self.ResolutionImage * self.ImageOrigine[Y, PixelHorizontalChoisi])
                # On ajoute la distance entre le point de départ, et celui du pixel que l'on vient d'ajouter ci-dessus (pythagore)
                ListeDistance.append(sqrt((PixelHorizontalChoisi - PointDepart[0]) ** 2 + (Y - PointDepart[1]) ** 2 ))
                
                # Pour chaque passage à la ligne suivante, on incrémente la position horizontale de sa valeur préalablement calculée 
                PositionX += IncrementHorizontal
        
        # On retourne les deux listes de données
        return ListeDistance, ListeAltitude
    
    def DetectionDunesAxe(self, NumeroAxe, ListeDune = []):
        # Le seuil de hauteur minimum pour qualifier de dune
        # On ne peut pas directement exploiter la données renseignées par l'utilisateur du programme
        # On utilise donc le plus petit multiple de la résolution de l'image qui puisse au moins faire la hauteur désignée
        SeuilDetection = ceil(self.DetectionDune / self.ResolutionImage) * self.ResolutionImage
        # On calcul la valeur de l'altitude maximum, celle qui signifie que l'on est en surface
        AltitudeMax = self.AltitudeMinimum + self.ResolutionImage * 255
        ListeDistance, ListeAltitude = self.TableauAltitudeDistance(NumeroAxe)
        
        IdDune = 0
        
        # indice de parcours des tableaux
        i = 0
        NombreElements = len(ListeAltitude)
        PrecedenteValeur = 255
        
        # On enlève toutes les valeurs d'altitude maximal au debut (ne sont pas associé à des dunes, c'est du blanc → la surface)
        while( i < NombreElements and ListeAltitude[i] == AltitudeMax):
            i += 1
            
        #print(i)    # ici en tout cas c'est OK!!!!!!!!!!
        
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
            
            while(i < NombreElements and ListeAltitude[i] <= PrecedenteValeur and i < NombreElements):
                Distance2 += 1
                PrecedenteValeur = ListeAltitude[i]
                i += 1
            
            ProfondeurDune2 = ListeAltitude[i - 1]  # 'i - 1' car à l'indice 'i' on ne respecte plus la condition (la valeur mesuré diminue continuellement)
    
            print("Distance1 = " + str(Distance1) + " Distance2 = " + str(Distance2))
    
            # Pour que l'on puisse juger si ce que l'on vient d'inspecter peut-être une dune, on peut déjà vérifier les distances mesurés
            if(Distance1 != 0 and Distance2 != 0):
                if(Distance1 < Distance2):
                    HauteurDune = (PicDune - ProfondeurDune1) * self.ResolutionImage
                elif(Distance2 < Distance1):
                    HauteurDune = (PicDune - ProfondeurDune2) * self.ResolutionImage
                else:
                    HauteurDune = (PicDune - ((ProfondeurDune1 + ProfondeurDune2) / 2)) * self.ResolutionImage
            
                LongeurOnde = min(Distance1, Distance2)
                
                print("Hauteur dune = " + str(HauteurDune) + " Longueur d'onde = " + str(LongeurOnde))
                
                if(HauteurDune >= SeuilDetection):
                    ListeDune.append(NumeroAxe, IdDune, HauteurDune, LongeurOnde)
                    
                return ListeDune
            
    def DetectionDunes(self):
        ListeTouteDunes = []
        for i in range (0, self.NombreAxes):
            self.DetectionDunesAxe(i, ListeTouteDunes)
                    
        #ListeTouteDunes = array([[0,0,10,15],[0,1,2,4],[1,2,3,4]])    # valeur test pour des résultats sur 2 tracés
        return ListeTouteDunes
                                
    def RemplirTableauResultats(self, ResultatsDunesAxes = array([[0,0,0,0]])):
        for i in range (0, self.NombreAxes):
            self.Table.insert('', 'end', str(i), text='Axe ' + str(i), tags = ('Color' + str(i)))
            self.Table.tag_configure('Color' + str(i), background=ListeCouleurs[i])
        
        for i in range (0, shape(ResultatsDunesAxes)[0]):
            self.Table.insert(str(ResultatsDunesAxes[i][0]), 'end', values = (str(ResultatsDunesAxes[i][1]), str(ResultatsDunesAxes[i][2]), str(ResultatsDunesAxes[i][3])))
            