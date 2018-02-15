from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from Interfaces import ResultatsAxes
from Interfaces import ResultatsImage
from TraitementImage import ImageDune
from TraitementImage import GestionAxes

# Faire en sorte que l'application prenne en compte la mise à l'échelle (scaling) de l'écran
# ! Attention ! Changer le scaling de l'écran en pleine exécution du programme ne permet plus d'afficher l'image en X sur Y pixels → cela ne peut PAS être corrigé (mais la prise en compte des coordonnées des pixels correspond toujours)
import os

# Si nous sommes sur une machine Windows
if os.name == 'nt':
    from ctypes import windll
    user32 = windll.user32
    user32.SetProcessDPIAware()

class MenuPrincipal(Frame):
    
    def __init__(self, fenetre):

        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.MonImage = ImageDune.ImageDune()
        self.LesAxes = GestionAxes.GestionAxes()
        
        self.ResolutionAltitude = 0 # La résolution de l'altitude de l'image → différence d'altitude (cm) entre 2 niveaux de gris
        self.ImageAffiche = 0
        self.PrecedentChoixResolutionImage = "" # Sauvegarder le précédent choix dans la comboBox, pour éventuellement le remettre (si l'utilisateur annule sont nouveau choix de résolution d'affichage de l'image)
        
        self.DessinPoint = [] # Garder une référence sur l'ensemble des points tracés (pour en permettre leur suppression)
        self.DessinLigne = [] # Garder une référence de l'ensemble des tracés (axes) effectués
        
        # Création de nos widgets
        Button(self, text='Charger image', command = lambda : self.ChargerImage()).grid(row=0, column=0, columnspan = 3)
        Label(self, text="Seuil détection des dunes").grid(row=1, column=0)
        
        # L'intervalle de choix de seuil de détection des dunes est un entier entre 0 et 100 (par défaut 10)
        self.SeuilDetectionDune = Spinbox(self, from_=0, to=100, width = 10)
        self.SeuilDetectionDune.grid(row=1, column=1)
        self.SeuilDetectionDune.delete(0)    # On enlève la valeur par défaut dans la Spinbox (qui est de base la valeur minimum)
        self.SeuilDetectionDune.insert(0, "10")  # On place maintenant la valeur 10 comme valeur par défaut
        # pour récupérer la valeur de la Spinbox, il suffit de faire SeuilDetectionDune.get()
        #Label(fenetre, text="cm").grid(row=1, column=3)
        self.lab = Label(self, text="cm")
        self.lab.grid(row=1, column=3)
        
        self.BoutonDupliquerAxe = Button(self, text="Dupliquer axe", state=DISABLED, command = lambda : self.DupliquerAxe())
        self.BoutonDupliquerAxe.grid(row=2, column=0, columnspan = 3)
        self.BoutonSupprimerDernierElement = Button(self, text="Supprimer dernier axe / point", state=DISABLED, command = lambda : self.SupprimerDernierAxeOuPoint())
        self.BoutonSupprimerDernierElement.grid(row=3, column=0, columnspan = 3)
        self.BoutonSupprimerAxes = Button(self, text="Supprimer axe(s)", state=DISABLED, command = lambda : self.SupprimerAxes())
        self.BoutonSupprimerAxes.grid(row=4, column=0, columnspan = 3)
        
        self.BoutonTraitementAxes = Button(self, text="Traitement axe(s)", state=DISABLED, command = lambda : self.TraitementAxes())
        self.BoutonTraitementAxes.grid(row=5, column=0, columnspan = 3)
        self.BoutonTraitementImage = Button(self, text="Traitement image", state=DISABLED, command = lambda : self.TraitementImage())
        self.BoutonTraitementImage.grid(row=6, column=0, columnspan = 3)
        
        Label(self, text="Résolution maximum d'affichage de l'image").grid(row=0, column=4)
        
        self.ChoixResolutionImage = ttk.Combobox(self, state="readonly")
        self.ChoixResolutionImage['values'] = ("854 x 480", "1280 x 720", "1920 x 1080", "Natives")
        self.PrecedentChoixResolutionImage = "1280 x 720"
        self.ChoixResolutionImage.set(self.PrecedentChoixResolutionImage)
        self.ChoixResolutionImage.grid(row=0, column=5)
        self.ChoixResolutionImage.bind("<<ComboboxSelected>>", lambda event : self.AffichageImage())
        
        self.Canevas = Canvas(self)
        #Canevas.config(height=200,width=250)  # Règle la taille du canvas par rapport à la taille de l'image 
        self.Canevas.create_image(0,0,anchor=NW)            # Règle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
        self.Canevas.configure(cursor="crosshair")
        self.Canevas.bind("<Button-1>", self.PlacementPoint)
        self.Canevas.grid(row=1, column=4, rowspan = 6, columnspan = 2)        
        
    # Comme il y a des bugs avec la librairie Pillow, les images TIFF utilisant la compression lzw ne sont pas corectement prises en charge
    # https://www.bountysource.com/issues/51811624-image-save-as-tiff-image-and-the-compression-parameter-does-not-work
    def ChargerImage(self):
        # On ouvre une boite de dialogue où l'utilisateur va choisir son image
        path = filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('tif','.tif'),('jpg','.jpg'),('bmp','.bmp'),('all files','.*')]) 
        # On vérifie que l'image est apte au traitements
        if path != "" :
            self.MonImage.AttribuerImage(path)
            # On affiche l'image dans l'interface
            self.AffichageImage()
            # On rend possible le bouton pour le traitement sur l'image
            self.BoutonTraitementImage['state'] = 'normal'
        
    def VerifierImage(self):
        # par défaut on suppose que l'image ne correspond pas aux contraintes nécessaires pour effectuer un traitement de l'image
        ImageValide = False
    
        try:
            # exemple de nom d'image Exemple_8,508_5,029.tif
            # on découpe donc par le caractère "_"
            # Altitude maximum : on en prend l'avant dernier morceau et on remplace la ',' par un '.' → conversion en float
            # Altitude minimum : on prend le dernier morceau, 
            #                    on le coupe par le caractère '.' pour enlever le '.tiff'
            #                    on en prend le premier morceau "5,029" et on remplace la ',' par un '.' → conversion en float
            
            MotImage = ((self.path.split("/"))[-1]).split("_")
            AltitudeMaximum = float(MotImage[-2].replace(',', '.'))
            self.AltitudeMin = float((MotImage[-1].split("."))[0].replace(',', '.'))
            # la résolution de l'altitude 
            # nombre de mètre correspond à la différence d'altitude entre 2 niveaux de gris successif
            # 256 niveaux de gris 
            self.ResolutionAltitude = round((AltitudeMaximum - self.AltitudeMin) / 256, 5)
            
            #print("Altitude Max = " + str(AltitudeMaximum))
            #print("Altitude Min = " + str(self.AltitudeMin))
            #print("Resolution image = " + str(self.ResolutionAltitude))
            
            # Si nous somme arrivé jusque ici, c'est que l'image est valide
            ImageValide = True
                
        except (ValueError, IndexError) :
            messagebox.showerror("Erreur", """L'image ouverte en paramètre ne respecte pas la convention de nommage pour utiliser le programme.
Les niveaux d'altitude minimum et maximum (m) doivent être indiqués dans le nom de l'image séparé par le caractère '_'.        
Exemples de noms valides :
A_5,284_9,21.tif
Exemple_-3,1_-8,867.tif
Projet_de_PRD_4,26_-8,141.tif""")
            
        return ImageValide
    
    def AffichageImage(self):
        
        #self.lab['text'] = str(self.winfo_screenwidth()) + " " + str(self.winfo_screenheight())
           
        # Il faut définir la variable au préalable (et par défaut à false, pour correspondre à la logique émise)
        ChoixPoursuivre = False
        
        # Avant d'afficher la nouvelle image (ou de changer la résolution d'affichage de celle actuelle),
        # on vérifie si l'utilisateur a pas déjà posé des points, et si c'est le cas,
        # Alors on l'avertie signalant que les points posés seront supprimés
        # (bien évidemment, il n'est pas possible d'ajouter des points si aucune image est affichée)
        if len(self.DessinPoint) > 0:
            ChoixPoursuivre = messagebox.askquestion("Attention", """Au moins un point est placé sur l'image actuelle
Poursuivre entrainerai leur suppression.
Voulez-vous poursuivre ?""")
            
            # Si l'utilisateur a demandé de poursuivre, on supprime alors les points et tracés (axes) établis
            if ChoixPoursuivre == 'yes' :
                self.SupprimerAxes()
            else :
                # Comme nous annulons la suppression des points, on réaffiche la résolution de référence dans la comboBox
                self.ChoixResolutionImage.set(self.PrecedentChoixResolutionImage)
        
        if len(self.MonImage.getPath()) > 0 and len(self.DessinPoint) == 0 :
            
            # On récupère la taille voulue (maximal) pour l'affichage de l'image
            LargeurMaxAffiche, HauteurMaxAffiche = self.DimensionMaxChoisi()
    
            # Attention, le ratio de mise à l'echelle de l'écran doit aussi être prit en compte → bug de Pillow
            # par exemple sur mon poste, afficher une image en 1280x720 pixels s'affichée réellement en 1600x900, et cela dû à la mise à l'échelle de 125%
            # Plus d'info: https://github.com/python-pillow/Pillow/issues/2438
            ratio = max(self.MonImage.getLargeurImage()/LargeurMaxAffiche, self.MonImage.getHauteurImage()/HauteurMaxAffiche)
            self.MiniatureImage = self.MonImage.getImage().resize((int(self.MonImage.getLargeurImage() / ratio), int(self.MonImage.getHauteurImage() / ratio)), Image.ANTIALIAS)
            
            self.ImageAffiche = ImageTk.PhotoImage(self.MiniatureImage)
            self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAffiche)
            # On redéfini la taille du caneva associé à la miniature de l'image sur l'interface graphique
            self.Canevas.config(width=self.MiniatureImage.size[0], height=self.MiniatureImage.size[1])
            
            # Comme nous utilisons la résolution indiquée dans la comboBox, elle devient celle de référence
            self.PrecedentChoixResolutionImage = self.ChoixResolutionImage.get()
    
    def PlacementPoint(self, event):    
        # Si une image valide est référencée
        if self.MonImage.PathValide():
            # On peux tracer 10 axes au maximum (pour garantir une couleur différente lors du traitement sur les axes 
            if(self.LesAxes.NombreAxes() > 9):
                messagebox.showerror("Erreur", "10 Tracés au maximum (limite atteinte).")
                return
                
            # On récupère la position du point que l'on va placer sur le canevas
            PositionXPoint = event.x
            PositionYPoint = event.y
            #print("X = " + str(PositionXPoint) + " Y = " + str(PositionYPoint))
            
            # On rajoute le point sur le canevas
            self.DessinPoint.append(self.Canevas.create_oval(PositionXPoint, PositionYPoint, PositionXPoint+1, PositionYPoint+1, fill="red"))
            # on garde en mémoire les coordonnées du points
            self.LesAxes.AjouterPoint(PositionXPoint, PositionYPoint)
            # On permet de supprimer le dernier élément
            self.BoutonSupprimerDernierElement['state'] = 'normal'
            
            # Si on vient d'ajouter le deuxième point pour le tracé d'un axe
            if self.LesAxes.DernierAxeComplet():
                # On trace la ligne entre les deux points tracés (avec la couleur rouge)                
                self.DessinLigne.append(self.Canevas.create_line(self.LesAxes.CoordonneesDernierAxe(), fill="red"))
                
                # On rend actif le bouton de traitement sur les axes (et de duplication des axes)
                self.BoutonTraitementAxes['state'] = 'normal'
                self.BoutonDupliquerAxe['state'] = 'normal'
                self.BoutonSupprimerAxes['state'] = 'normal'
                
                # On change la couleur du dernier axe précédent → mettre en valeur le dernier tracé (celui qui peut être supprimé ou dupliqué)
                if(self.LesAxes.NombreAxes() > 1):
                    self.Canevas.itemconfig(self.DessinLigne[self.LesAxes.NombreAxes() - 2], fill = "blue")
    
    def DupliquerAxe(self):        
        if(self.LesAxes.NombreAxes() < 1):
            messagebox.showerror("Erreur", "Aucun axe n'est encore tracé.")
        # S'il y a un point non utilisé pour un tracé (le dernier axe n'est pas complet)
        elif not self.LesAxes.DernierAxeComplet():
                # Le tracé qui se fait dupliqué n'est plus le dernier effectué → il passe donc en bleu
                self.Canevas.itemconfig(self.DessinLigne[self.LesAxes.NombreAxes() - 2], fill = "blue")
                # Calcul des coordonnées du deuxième point en se basant sur le vecteur entre les deux points du tracé précédent
                VecteurAncienAxe = self.LesAxes.VecteurDernierAxe()
                PointDepart = self.LesAxes.PositionDernierPointDepart()
                NouveauPointX = PointDepart[0] + VecteurAncienAxe[0]
                NouveauPointY = PointDepart[1] + VecteurAncienAxe[1]
                # On place maintenant le deuxième point, ainsi que le tracé les reliant
                self.DessinPoint.append(self.Canevas.create_oval(NouveauPointX, NouveauPointY, NouveauPointX+1, NouveauPointY+1, fill="red"))
                self.LesAxes.AjouterPoint(NouveauPointX, NouveauPointY)
                self.DessinLigne.append(self.Canevas.create_line(self.LesAxes.CoordonneesDernierAxe(), fill="red"))
        else :
            messagebox.showerror("Information", """Placer le premier point d'abord
    puis cliquer sur ce même bouton""")
            
    def SupprimerDernierAxeOuPoint(self):
        # Si tous les axes sont complet (pas de point tout seul → on supprime le dernier tracé (la ligne et les 2 points)
        if (self.LesAxes.DernierAxeComplet()):
            # On enlève les points + la ligne sur l'affichage du canevas
            self.Canevas.after(1000, self.Canevas.delete, self.DessinLigne[-1])
            self.Canevas.after(1000, self.Canevas.delete, self.DessinPoint[-2])
            self.Canevas.after(1000, self.Canevas.delete, self.DessinPoint[-1])
            # On supprime les supprimer de leur liste
            del self.DessinLigne[-1]
            del self.DessinPoint[-2:]
            
            self.LesAxes.SupprimerDernierAxe()
            # Si il reste encore au moins 1 tracé sur l'image, l'avant dernier tracé effectué repasse en rouge (il devient celui qui peut être supprimé / dupliqué) 
            if(self.LesAxes.NombreAxes() > 0):
                self.Canevas.itemconfig(self.DessinLigne[self.LesAxes.NombreAxes() - 1], fill = "red")
            else:
                # On désactive le bouton de traitement sur les axes
                self.BoutonTraitementAxes['state'] = 'disabled'
                self.BoutonDupliquerAxe['state'] = 'disabled'
                self.BoutonSupprimerAxes['state'] = 'disabled'
    
            # Si un point a été placé sans qu'il soit utilisé par un tracé → on supprime le point en question
        else:
            self.Canevas.after(1000, self.Canevas.delete, self.DessinPoint[-1])
            del self.DessinPoint[-1]
            self.LesAxes.SupprimerDernierAxe()
                
        # si il n'y a plus de point placé par l'utilisateur → désactiver le bouton
        if(self.LesAxes.NombreAxes() == 0):
            self.BoutonSupprimerDernierElement['state'] = 'disabled'
            
    def SupprimerAxes(self):
        # On supprime toutes les lignes sur le canevas
        for i in range (0, len(self.DessinLigne)):
            self.Canevas.after(1000, self.Canevas.delete, self.DessinLigne[i])
        
        # on supprime tous les points sur le canevas
        for i in range (0, len(self.DessinPoint)):
            self.Canevas.after(1000, self.Canevas.delete, self.DessinPoint[i])
            
        # On vide les tableaus référencant les éléments graphiques lignes et points
        del self.DessinLigne[:]
        del self.DessinPoint[:]
            
        self.LesAxes.SupprimerTousAxes()
        
        # On désactive le bouton de traitement sur les axes
        self.BoutonTraitementAxes['state'] = 'disabled'
        self.BoutonDupliquerAxe['state'] = 'disabled'
        self.BoutonSupprimerDernierElement['state'] = 'disabled'
        self.BoutonSupprimerAxes['state'] = 'disabled'
               
    def DimensionMaxChoisi(self):
        Resolution = self.ChoixResolutionImage.get().split(" ")
        
        # Cas particulier, on a choisi d'afficher l'image dans sa résolution d'origine
        try:
            ResolutionLargeur = int(Resolution[0])
            ResolutionHauteur = int(Resolution[2])
        except ValueError:
            ResolutionLargeur = self.image.size[0]
            ResolutionHauteur = self.image.size[1]
                
        return ResolutionLargeur, ResolutionHauteur
    
    def TraitementAxes(self):
        # Si il y a un point non utilisé pour un axe on le supprime, avant d'en envoyer le tableau à la fenêtre suivante
        if not self.LesAxes.DernierAxeComplet():
            self.SupprimerDernierAxeOuPoint()
            
        fenTraitementAxes = Toplevel()
        fenTraitementAxes.title("Résultats issus des axes - Analyse dunes 2018")
        ResultatsAxes.ResultatsAxes(fenTraitementAxes, self.MonImage, self.MiniatureImage, self.SeuilDetectionDune.get(), self.LesAxes)

    def TraitementImage(self):
        fenTraitementImage = Toplevel()
        fenTraitementImage.title("Résultats image complète - Analyse dunes 2018")
        ResultatsImage.ResultatsImage(fenTraitementImage, self.MonImage, self.MiniatureImage, self.SeuilDetectionDune.get())