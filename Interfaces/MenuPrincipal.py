from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from Interfaces import ResultatsAxes
from Interfaces import ResultatsImage
from TraitementImage import ImageDune
from TraitementImage import GestionAxes

# Faire en sorte que l'application prenne en compte la mise à  l'échelle (scaling) de l'écran
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
        
        self.CourantVersLaGauche = True # Cette variable permet de savoir le sens de lecture du courant (par défaut vers la gauche → donnée cliente)
        
        # Création d'une sous frame pour placer correctement les divers éléments sur la moitié gauche de la fenêtre
        FrameMenu = Frame(self)
        FrameMenu.pack(side=LEFT, fill = BOTH, expand = 1)
        
        # Création de nos widgets
        Button(FrameMenu, text='Charger image', command = lambda : self.ChargerImage()).pack(side=TOP)
        
        FrameInfoImage = Frame(FrameMenu)
        FrameInfoImage.pack(side=TOP)
        
        Label(FrameInfoImage, text="Seuil détection des petites dunes").grid(row=0, column=0)
        # L'intervalle de choix de seuil de détection des petites dunes est un entier entre 0 et 100 (par défaut 10)
        self.SeuilDetectionDune = Spinbox(FrameInfoImage, from_=0, to=100, width = 10)
        self.SeuilDetectionDune.grid(row=0, column=1)
        self.SeuilDetectionDune.delete(0)    # On enlève la valeur par défaut dans la Spinbox (qui est de base la valeur minimum)
        self.SeuilDetectionDune.insert(0, "10")  # On place maintenant la valeur 10 comme valeur par défaut
        # pour récupérer la valeur de la Spinbox, il suffit de faire SeuilDetectionDune.get()
        Label(FrameInfoImage, text="cm").grid(row=0, column=2)
        
        Label(FrameInfoImage, text="Seuil détection des grandes dunes").grid(row=1, column=0)
        # L'intervalle de choix de seuil de détection des grandes dunes est un entier entre 0 et 100 (par défaut 50)
        self.SeuilDetectionDune = Spinbox(FrameInfoImage, from_=0, to=100, width = 10)
        self.SeuilDetectionDune.grid(row=1, column=1)
        self.SeuilDetectionDune.delete(0)    # On enlève la valeur par défaut dans la Spinbox (qui est de base la valeur minimum)
        self.SeuilDetectionDune.insert(0, "50")  # On place maintenant la valeur 50 comme valeur par défaut
        # pour récupérer la valeur de la Spinbox, il suffit de faire SeuilDetectionDune.get()
        Label(FrameInfoImage, text="cm").grid(row=1, column=2)
        
        Label(FrameInfoImage, text="Sens du courant").grid(row=2, column=0)
        self.ChoixSensCourant= ttk.Combobox(FrameInfoImage, state="readonly")
        self.ChoixSensCourant['values'] = ("Vers la gauche", "Vers la droite")
        self.ChoixSensCourant.set("Vers la gauche")
        self.ChoixSensCourant.grid(row=2, column=1, columnspan=2)
        self.ChoixSensCourant.bind("<<ComboboxSelected>>", lambda event : self.ChoisirSensCourant())
        
        self.BoutonDupliquerAxe = Button(FrameMenu, text="Dupliquer axe", state=DISABLED, command = lambda : self.DupliquerAxe())
        self.BoutonDupliquerAxe.pack(side=TOP)
        self.BoutonSupprimerDernierElement = Button(FrameMenu, text="Supprimer dernier axe / point", state=DISABLED, command = lambda : self.SupprimerDernierAxeOuPoint())
        self.BoutonSupprimerDernierElement.pack(side=TOP)
        self.BoutonSupprimerAxes = Button(FrameMenu, text="Supprimer axe(s)", state=DISABLED, command = lambda : self.SupprimerAxes())
        self.BoutonSupprimerAxes.pack(side=TOP)
        
        self.BoutonTraitementAxes = Button(FrameMenu, text="Traitement axe(s)", state=DISABLED, command = lambda : self.TraitementAxes())
        self.BoutonTraitementAxes.pack(side=TOP)
        self.BoutonTraitementImage = Button(FrameMenu, text="Traitement image", state=DISABLED, command = lambda : self.TraitementImage())
        self.BoutonTraitementImage.pack(side=TOP)
        
        FrameImage = Frame(self)
        FrameImage.pack(side=RIGHT, fill = BOTH, expand = 1)
        
        FrameResolutionImage = Frame(FrameImage)
        FrameResolutionImage.pack(side=TOP)
        
        Label(FrameResolutionImage, text="Résolution maximum d'affichage de l'image").pack(side=LEFT)
        
        self.ChoixResolutionImage = ttk.Combobox(FrameResolutionImage, state="readonly")
        self.ChoixResolutionImage['values'] = ("854 x 480", "1280 x 720", "1920 x 1080", "Natives")
        self.PrecedentChoixResolutionImage = "1280 x 720"
        self.ChoixResolutionImage.set(self.PrecedentChoixResolutionImage)
        self.ChoixResolutionImage.pack(side=RIGHT)
        self.ChoixResolutionImage.bind("<<ComboboxSelected>>", lambda event : self.AffichageImage())
        
        self.Canevas = Canvas(FrameImage)
        self.Canevas.create_image(0,0,anchor=NW)            # Règle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
        self.Canevas.configure(cursor="crosshair")
        self.Canevas.bind("<Button-1>", self.PlacementPoint)
        self.Canevas.pack(side=RIGHT, fill = BOTH, expand = 1) 
        
    # Comme il y a des bugs avec la librairie Pillow, les images TIFF utilisant la compression lzw ne sont pas corectement prises en charge
    # https://www.bountysource.com/issues/51811624-image-save-as-tiff-image-and-the-compression-parameter-does-not-work
    def ChargerImage(self):
        # On ouvre une boite de dialogue oà¹ l'utilisateur va choisir son image
        path = filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('tif','.tif'),('jpg','.jpg'),('bmp','.bmp'),('all files','.*')]) 
        # On vérifie que l'image est apte au traitements
        if path != "" :
            self.MonImage.AttribuerImage(path)
            # On affiche l'image dans l'interface
            self.AffichageImage()
            # On rend possible le bouton pour le traitement sur l'image
            self.BoutonTraitementImage['state'] = 'normal'
    
    def AffichageImage(self):
        
        #self.lab['text'] = str(self.winfo_screenwidth()) + " " + str(self.winfo_screenheight())
           
        # Il faut définir la variable au préalable (et par défaut à  false, pour correspondre à  la logique émise)
        ChoixPoursuivre = False
        
        # Avant d'afficher la nouvelle image (ou de changer la résolution d'affichage de celle actuelle),
        # on vérifie si l'utilisateur a pas déjà  posé des points, et si c'est le cas,
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
    
            # Attention, le ratio de mise à  l'echelle de l'écran doit aussi être prit en compte → bug de Pillow
            # par exemple sur mon poste, afficher une image en 1280x720 pixels s'affichée réellement en 1600x900, et cela dà» à  la mise à l'échelle de 125%
            # Plus d'info: https://github.com/python-pillow/Pillow/issues/2438
            ratio = max(self.MonImage.getLargeurImage()/LargeurMaxAffiche, self.MonImage.getHauteurImage()/HauteurMaxAffiche)
            self.MiniatureImage = self.MonImage.getImage().resize((int(self.MonImage.getLargeurImage() / ratio), int(self.MonImage.getHauteurImage() / ratio)), Image.ANTIALIAS)
            
            self.ImageAffiche = ImageTk.PhotoImage(self.MiniatureImage)
            self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAffiche)
            # On redéfini la taille du caneva associé à  la miniature de l'image sur l'interface graphique
            self.Canevas.config(width=self.MiniatureImage.size[0], height=self.MiniatureImage.size[1])
            
            # Comme nous utilisons la résolution indiquée dans la comboBox, elle devient celle de référence
            self.PrecedentChoixResolutionImage = self.ChoixResolutionImage.get()
    
    def ChoisirSensCourant(self):
        Choix = self.ChoixSensCourant.get()
        if (Choix == "Vers la gauche"):
            self.MonImage.setSensCourant(True)
        else:
            self.MonImage.setSensCourant(False)
    
    def PlacementPoint(self, event):    
        # Si une image valide est référencée
        if self.MonImage.PathValide():
            # On peux tracer 10 axes au maximum (pour garantir une couleur différente lors du traitement sur les axes)
            #On regarde donc si on en a plus de 9 et que le dernier (le dixième) est complets
            if(self.LesAxes.NombreAxes() > 9 and self.LesAxes.DernierAxeComplet()):
                messagebox.showerror("Erreur", "10 Tracés au maximum (limite atteinte).")
                return
                
            # On récupère la position du point que l'on va placer sur le canevas
            PositionXPoint = event.x
            PositionYPoint = event.y
            #print("X = " + str(PositionXPoint) + " Y = " + str(PositionYPoint))
            
            # Si le point que l'on s'apprête a ajouter est le deuxième d'un axe, et qu'il se trouve au même endroit que le premier
            # Alors on empêche la création de ce point
            if (self.LesAxes.NombreAxes() > 0 and not self.LesAxes.DernierAxeComplet()):
                CoordonneePremierPoint = self.LesAxes.PositionDernierPointDepart();
                if(CoordonneePremierPoint[0] == PositionXPoint and CoordonneePremierPoint[1] == PositionYPoint):
                    messagebox.showerror("Erreur", "Les 2 points de l'axe sont placés au même endroit")
                    return
            
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
            ResolutionLargeur = self.MonImage.getLargeurImage()
            ResolutionHauteur = self.MonImage.getHauteurImage()
                
        return ResolutionLargeur, ResolutionHauteur
    
    def TraitementAxes(self):
        # Si il y a un point non utilisé pour un axe on le supprime, avant d'en envoyer le tableau à  la fenêtre suivante
        if not self.LesAxes.DernierAxeComplet():
            self.SupprimerDernierAxeOuPoint()
            
        fenTraitementAxes = Toplevel()
        fenTraitementAxes.title("Résultats issus des axes - Analyse dunes 2018")
        ResultatsAxes.ResultatsAxes(fenTraitementAxes, self.MonImage, self.MiniatureImage, self.SeuilDetectionDune.get(), self.LesAxes)

    def TraitementImage(self):
        fenTraitementImage = Toplevel()
        fenTraitementImage.title("Résultats image complète - Analyse dunes 2018")
        ResultatsImage.ResultatsImage(fenTraitementImage, self.MonImage, self.MiniatureImage, self.SeuilDetectionDune.get())
