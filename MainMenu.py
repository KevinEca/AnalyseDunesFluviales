from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from matplotlib import image

path = "" # chemin indiquant où se trouve l'image sélectionnée
image = Image # variable pour stocker en mémoire le tableau original de l'image (après passage en noir et blanc 8 bits)
ResolutionAltitude = 0 # La résolution de l'altitude de l'image → nombre de cm en altitude entre 2 niveaux de gris
ImageOrigine = PhotoImage
PrecedentChoixResolutionImage = "" # Sauvegarder le précédent choix dans la comboBox, pour éventuellement le remettre (si l'utilisateur annule sont nouveau choix de résolution d'affichage de l'image)

DessinPoint = [] # Garder une référence sur l'ensemble des points tracés (pour en permettre leur suppression)
DessinLigne = [] # Garder une référence de l'ensemble des tracés (axes) effectués
CoordonneesPoints = [] # Garder en mémoire les coordonnées des points
NombreLignes = 0 # Savoir à quelles coordonnées (CoordonneesPoints) on se réfère pour tracer la ligne (et ainsi combien de ligne est tracé)

def ChargerImage():
    global path, image
    # On ouvre une boite de dialogue où l'utilisateur va choisir son image
    path = filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('tif files','.tif'),('jpg files','.jpg'),('bmp files','.bmp'),('all files','.*')]) 
    # On vérifie que l'image est apte au traitements
    if VerifierImage() == True :
        # On Convertie l'image en noir et blanc 8 bits et on la sauvegarde en mémoire
        image = Image.open(path).convert('L')
        # On affiche l'image dans l'interface
        AffichageImage()
        
def VerifierImage():
    global path, ResolutionAltitude
    # par défaut on suppose que l'image ne correspond pas aux contraintes nécessaires pour effectuer un traitement de l'image
    ImageValide = False

    try:
        # exemple de nom d'image Exemple_8,508_5,029.tif
        # on découpe donc par le caractère "_"
        # Altitude maximum : on en prend l'avant dernier morceau et on remplace la ',' par un '.' → conversion en float
        # Altitude minimum : on prend le dernier morceau, 
        #                    on le coupe par le caractère '.' pour enlever le '.tiff'
        #                    on en prend le premier morceau "5,029" et on remplace la ',' par un '.' → conversion en float
        
        MotImage = ((path.split("/"))[-1]).split("_")
        AltitudeMaximum = MotImage[-2].replace(',', '.')
        AltitudeMinimun = (MotImage[-1].split("."))[0].replace(',', '.')
        # la résolution de l'altitude 
        # nombre de mètre correspond à la différence d'altitude entre 2 niveaux de gris successif
        # 256 niveaux de gris * 100 cm par mètre
        ResolutionAltitude = str(round( (float(AltitudeMaximum) - float(AltitudeMinimun)) / 2.56, 2))
        
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

def AffichageImage():
    global imgtk, image, Canevas, path, ImageOrigine, DessinPoint, PrecedentChoixResolutionImage
    
    # Il faut définir la variable au préalable (et par défaut à false, pour correspondre à la logique émise)
    ChoixPoursuivre = False
    
    # Avant d'afficher la nouvelle image (ou de changer la résolution d'affichage de celle actuelle),
    # on vérifie si l'utilisateur a pas déjà posé des points, et si c'est le cas,
    # Alors on l'avertie signalant que les points posés seront supprimés
    # (bien évidemment, il n'est pas possible d'ajouter des points si aucune image est affichée)
    if len(DessinPoint) > 0:
        ChoixPoursuivre = messagebox.askquestion("Attention", """Au moins un point est placé sur l'image actuelle
Poursuivre entrainerai leur suppression.
Voulez-vous poursuivre ?""")
        
        # Si l'utilisateur a demandé de poursuivre, on supprime alors les points et tracés (axes) établis
        if ChoixPoursuivre == 'yes' :
            SupprimerAxes()
        else :
            # Comme nous annulons la suppression des points, on réaffiche la résolution de référence dans la comboBox
            ChoixResolutionImage.set(PrecedentChoixResolutionImage)
    
    if len(path) > 0 and len(DessinPoint) == 0 :
        
        # On récupère la taille voulue (maximal) pour l'affichage de l'image
        LargeurMaxAffiche, HauteurMaxAffiche = DimensionMaxChoisi()

        # On redimensionne l'image pour qu'elle puisse rentrer dans la résolution maximale indiquée par l'utilisateur (comboBox)
        # D'où sort le 1.248 ?
        # Entre la taille réelle de l'image et celle affiché dans la fenêtre, celle-ci n'adopte pas la même taille, pourquoi ? je ne sais pas un bug peut-être ?
        # quant l'on affiche une image faisant 1280 pixel de large, et que l'on défini "LargeurMaxAffiche" à 1280, l'image sur la fenêtre est affiché sur 1598 pixels
        # Donc pour compenser cet agrandissement, il a été déterminé le coefficent d'agrandissement, 1598/1280 soit environ 1.248
        # ainsi en appliquant ce coefficient une image en 1280 x 720 pixels, avec "LargeurMaxAffiche" = "1280 x 720" affiche l'image concrètement en 1279 x 718 pixels
        ratio = max(image.size[0]/LargeurMaxAffiche, image.size[1]/HauteurMaxAffiche) * 1.248
        MiniatureImage = image.resize((int(image.size[0] / ratio), int(image.size[1] / ratio)), Image.ANTIALIAS)
        
        ImageOrigine = ImageTk.PhotoImage(MiniatureImage)
        Canevas.create_image(0,0,anchor=NW,image = ImageOrigine)
        # On redéfini la taille des canevas coller à celui de la miniature de l'image sur l'interface graphique
        Canevas.config(width=MiniatureImage.size[0], height=MiniatureImage.size[1])
        
        # Comme nous utilisons la résolution indiquée dans la comboBox, elle devient celle de référence
        PrecedentChoixResolutionImage = ChoixResolutionImage.get()

def PlacementPoint(event):
    global points, DessinLigne, DessinPoint, NombreLignes

    # Si une image valide est référencée
    if (len(path) > 0):
        # On rajoute le point sur le canevas
        DessinPoint.append(Canevas.create_oval(event.x, event.y, event.x+1, event.y+1, fill="red"))
        # on garde en mémoire les coordonnées du points
        CoordonneesPoints.append(event.x)
        CoordonneesPoints.append(event.y)
        # Si onajoute le deuxième point pour le tracé d'un axe
        if (len(DessinPoint) % 2 == 0):
            # On trace la ligne entre les deux points tracés (avec la couleur rouge)
            DessinLigne.append(Canevas.create_line(CoordonneesPoints[4*NombreLignes:4*(NombreLignes + 1)], fill="red"))
            # On change la couleur de la ligne précédente → mettre en valeur le dernier tracé (celui qui peut être supprimé ou dupliqué)
            if(NombreLignes > 0):
                Canevas.itemconfig(DessinLigne[NombreLignes - 1], fill = "blue")
            NombreLignes+=1  

def DupliquerAxe():
    global points, DessinLigne, DessinPoint, NombreLignes
    
    if(NombreLignes < 1):
        messagebox.showerror("Erreur", "Aucun axe n'est encore tracé.")
    # S'il y a un point non utilisé pour un tracé
    elif len(DessinPoint) % 2 == 1:
            # Le tracé qui se fait dupliqué n'est plus le dernier effectué → il passe donc en bleu
            Canevas.itemconfig(DessinLigne[NombreLignes - 1], fill = "blue")
            # Calcul des coordonnées du deuxième point en se basant sur le vecteur entre les deux points du tracé précédent
            NouveauPointX = CoordonneesPoints[NombreLignes * 4] - ( CoordonneesPoints[4*(NombreLignes - 1)] - CoordonneesPoints[4*(NombreLignes - 1) + 2])
            NouveauPointY = CoordonneesPoints[NombreLignes * 4 +  1] - ( CoordonneesPoints[4*(NombreLignes - 1) + 1] - CoordonneesPoints[4*(NombreLignes - 1) + 3])
            # On place maintenant le deuxième point, ainsi que le tracé les reliant
            DessinPoint.append(Canevas.create_oval(NouveauPointX, NouveauPointY, NouveauPointX+1, NouveauPointY+1, fill="red"))
            CoordonneesPoints.append(NouveauPointX)
            CoordonneesPoints.append(NouveauPointY)
            DessinLigne.append(Canevas.create_line(CoordonneesPoints[4*NombreLignes:4*(NombreLignes + 1)], fill="red"))
            NombreLignes+=1
    else :
        messagebox.showerror("Information", """Placer le premier point d'abord
puis cliquer sur ce même bouton""")
        
def SupprimerDernierAxeOuPoint():
    global points, DessinLigne, DessinPoint, NombreLignes
    
    if (len(path) > 0):
        # Si il y a pas de point seul placé et au moins un axe de tracé → on supprime le dernier tracé
        if (len(DessinPoint) % 2 == 0 and NombreLignes > 0):
            NombreLignes -= 1
            Canevas.after(1000, Canevas.delete, DessinLigne[-1])
            Canevas.after(1000, Canevas.delete, DessinPoint[-2])
            Canevas.after(1000, Canevas.delete, DessinPoint[-1])
            del DessinLigne[-1]
            del CoordonneesPoints[-4:]
            del DessinPoint[-2:]
            # Si il reste encore au moins 1 tracé sur l'image, l'avant dernier tracé effectué repasse en rouge (il devient celui qui peut être supprimé / dupliqué) 
            if(NombreLignes > 0):
                Canevas.itemconfig(DessinLigne[NombreLignes - 1], fill = "red")

        # Si un point a été placé sans qu'il soit utilisé par un tracé → on supprime le point en question
        elif (len(DessinPoint) % 2):
            Canevas.after(1000, Canevas.delete, DessinPoint[2 * NombreLignes])
            del CoordonneesPoints[-2:]
            del DessinPoint[-1:]
            
def SupprimerAxes():
    global points, DessinLigne, DessinPoint, NombreLignes
    # On supprime toutes les lignes sur le canevas
    for i in range (0, len(DessinLigne)):
        Canevas.after(1000, Canevas.delete, DessinLigne[i])
    
    # on supprime tous les points sur le canevas
    for i in range (0, len(DessinPoint)):
        Canevas.after(1000, Canevas.delete, DessinPoint[i])
    
    # On vide les tableaus référencant les éléments graphiques lignes et points, ainsi que celui contenant les coordonnées des points
    del DessinLigne[:]
    del CoordonneesPoints[:]
    del DessinPoint[:]
    NombreLignes = 0
           
def DimensionMaxChoisi():
    Resolution = ChoixResolutionImage.get().split(" ")
    return int(Resolution[0]), int(Resolution[2])

fenetre = Tk()
fenetre.title("Menu principal - Analyse dunes 2018")
# On empèche l'utilisateur de redimensionner la taille de la fenêtre
fenetre.resizable(width=False, height=False)

Button(fenetre, text='Charger image', command = lambda : ChargerImage()).grid(row=0, column=0, columnspan = 3)
Label(fenetre, text="Seuil détection des dunes").grid(row=1, column=0)

# L'intervalle de choix de seuil de détection des dunes est un entier entre 0 et 100 (par défaut 10)
SeuilDetectionDune = Spinbox(fenetre, from_=0, to=100, width = 10)
SeuilDetectionDune.grid(row=1, column=1)
SeuilDetectionDune.delete(0)    # On enlève la valeur par défaut dans la Spinbox (qui est de base la valeur minimum)
SeuilDetectionDune.insert(0, "10")  # On place maintenant la valeur 10 comme valeur par défaut
# pour récupérer la valeur de la Spinbox, il suffit de faire SeuilDetectionDune.get()
#Label(fenetre, text="cm").grid(row=1, column=3)
lab= Label(fenetre, text="cm")
lab.grid(row=1, column=3)

Button(fenetre, text="Dupliquer axe", command = lambda : DupliquerAxe()).grid(row=2, column=0, columnspan = 3)
Button(fenetre, text="Supprimer dernier axe / point", command = lambda : SupprimerDernierAxeOuPoint()).grid(row=3, column=0, columnspan = 3)
Button(fenetre, text="Supprimer axe(s)", command = lambda : SupprimerAxes()).grid(row=4, column=0, columnspan = 3)

Button(fenetre, text="Traitement axe(s)", command = lambda : SupprimerAxes()).grid(row=5, column=0, columnspan = 3)
Button(fenetre, text="Traitement image", command = lambda : SupprimerAxes()).grid(row=6, column=0, columnspan = 3)

Label(fenetre, text="Résolution maximum d'affichage de l'image").grid(row=0, column=4)

ChoixResolutionImage = ttk.Combobox(fenetre)
ChoixResolutionImage['values'] = ("854 x 480", "1280 x 720", "1920 x 1080")
PrecedentChoixResolutionImage = "1280 x 720"
ChoixResolutionImage.set(PrecedentChoixResolutionImage)
ChoixResolutionImage.grid(row=0, column=5)
ChoixResolutionImage.bind("<<ComboboxSelected>>", lambda event : AffichageImage())

Canevas = Canvas(fenetre) 
Canevas.config(height=200,width=250)  # Règle la taille du canvas par rapport à la taille de l'image 
Canevas.create_image(0,0,anchor=NW)            # Règle l'emplacement du milieu de l'image, ici dans le coin Nord Ouest (NW) de la fenetre
Canevas.configure(cursor="crosshair")
Canevas.bind("<Button-1>", PlacementPoint)
Canevas.grid(row=1, column=4, rowspan = 6, columnspan = 2)

fenetre.mainloop()
