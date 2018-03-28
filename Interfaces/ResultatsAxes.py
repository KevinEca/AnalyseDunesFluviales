from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from scipy import shape
from Interfaces import VisualiserProfil
from TraitementImage import AlgorithmeAxe, ExportTXT

ListeCouleurs = ["blue", "red", "sienna", "chartreuse", "darkgreen", "deepskyblue", "crimson", "darkorange", "yellow", "purple"]

class ResultatsAxes(Frame):  

    def __init__(self, fenetre, MonImage = None, ImageAffiche = [0], SeuilDetectionDune = 0, LesAxes = None):    
        
        self.MonImage = MonImage
        self.ImageAffichage = ImageAffiche
        self.DetectionDune = float(SeuilDetectionDune) / 100
        self.LesAxes = LesAxes
        self.ImageAAfficher = 0 # variable ne pouvant être une variable locale, sinon l'image n'apparaît pas à l'affichage
        self.NombreAxes = self.LesAxes.NombreAxes()
        
        # Création d'une sous frame pour placer correctement les divers éléments sur la moitié gauche de la fenêtre
        FrameMenu = Frame(fenetre)
        FrameMenu.pack(side=LEFT, fill = BOTH, expand = 1)
        
        # Création de nos widgets (à placer dans la moitié gauche de la fenêtre)
        Button(FrameMenu, text="Export de tous les résultats", command = lambda : self.ExportTxt()).pack(side=TOP)
        
        # On crée une nouvelle sous-frame afn de pouvoir placer les 4 éléments graphique suivant sous forme d'un table 2*2 emplacements
        FrameChoixAxe = Frame(FrameMenu)
        FrameChoixAxe.pack(side=TOP, fill = Y)
        
        Label(FrameChoixAxe, text="Numéro de l'axe choisi").grid(row=0, column=0)
        # Pour que le spinBox puisse fonctionner, il faut qu'il propose 2 valeurs au minimum
        # On regarde donc si l'utilisateur n'a fait qu'un seul axe
        if (self.NombreAxes < 2):
            # Si c'est le cas, on désactive le spinBox, ainsi on force la valeur à 0
            self.NumeroAxeChoisi = Spinbox(FrameChoixAxe, from_=0, to=1, width = 10, state = 'disabled')
        else:
            self.NumeroAxeChoisi = Spinbox(FrameChoixAxe, from_=0, to= (self.NombreAxes - 1), width = 10, state = 'readonly')
        self.NumeroAxeChoisi.grid(row=0, column=1)
        Button(FrameChoixAxe, text="Export résultats axe", command = lambda : self.ExportTxtAxe()).grid(row=1, column=0)
        Button(FrameChoixAxe, text="Visualisation profil axe", command = lambda : self.VisualiserProfil()).grid(row=1, column=1)

        # On place une frame pour y placer notre treeview (gauche) avec sa barre de défilement vertical (droite)
        # fill = BOTH + exppand = 1 → permet d'étendre le tableau au reste de la moitié gauche de la fenêtre restante
        self.FrameTable = Frame(FrameMenu, height=255, width = 255, bd=1, relief=SUNKEN)
        self.FrameTable.pack(side=TOP, fill = BOTH, expand = 1)
        
        # on crée notre treeview
        self.Table = ttk.Treeview(self.FrameTable, columns=('IdDune', 'LongOnde', 'HautDune'))
        # On lui associe une barre de défilement vertical
        self.VerticalBarreTable = ttk.Scrollbar(self.FrameTable, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.VerticalBarreTable.set)
        self.Table.pack(side=LEFT, fill = BOTH, expand = 1)
        self.VerticalBarreTable.pack(side=RIGHT, fill = Y)
        
        self.Table.column('#0', width=60, anchor='center')  # la colonne #0 correspond à celle où se trouve les + pour dérouler
        self.Table.column('IdDune', width=100, anchor='center')
        self.Table.heading('IdDune', text='ID Dune')
        self.Table.column('LongOnde', width=150, anchor='center')
        self.Table.heading('LongOnde', text="Longueur d'onde (m)")
        self.Table.column('HautDune', width=140, anchor='center')
        self.Table.heading('HautDune', text="Hauteur dune (cm)")
        
        # On créé notre Convas permettant d'afficher l'image et on demande de la placer sur la moitié droite de la fenêtre
        self.Canevas = Canvas(fenetre)
        self.ImageAAfficher = ImageTk.PhotoImage(self.ImageAffichage)
        self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAAfficher)
        # On redéfini la taille du caneva associé à la miniature de l'image sur l'interface graphique
        self.Canevas.config(width=self.ImageAffichage.size[0], height=self.ImageAffichage.size[1])
        self.Canevas.pack(side=RIGHT)
        
        # On place les axes sur la miniatures, mais on les colorie d'une couleur différentes afin de les différencier
        self.PlacementAxes()
        
        # On rempli le tableau des résultats par les données obtenues par analyse de tous les axes tracés par l'utilisateur
        self.TableauAnalyseImageAxe = AlgorithmeAxe.DetectionDunes(self.MonImage, self.LesAxes, self.ImageAffichage, self.DetectionDune)
        self.BilanDunesAxe = AlgorithmeAxe.BilanDunesParAxe(self.TableauAnalyseImageAxe, self.NombreAxes)
        self.RemplirTableauResultats()
        
    def PlacementAxes(self):
        for i in range (0, self.NombreAxes):
            self.Canevas.create_line(self.LesAxes.CoordonneesAxe(i), fill=ListeCouleurs[i])

    def ExportTxt(self):
        ExportTXT.ExportResultatsDunesAxes(self.TableauAnalyseImageAxe, self.MonImage, self.LesAxes, self.BilanDunesAxe, self.DetectionDune)
    
    def ExportTxtAxe(self):
        AxeChoisi = int(self.NumeroAxeChoisi.get())
        ExportTXT.ExportResultatsDunesAxe(self.TableauAnalyseImageAxe, self.MonImage, AxeChoisi, self.LesAxes.InfosAxe(AxeChoisi).getCoordonneesAxe(), self.BilanDunesAxe[AxeChoisi], self.DetectionDune)
    
    def VisualiserProfil(self):
        AxeChoisi = int(self.NumeroAxeChoisi.get())
        XCoordonnee, YCoordonnee = AlgorithmeAxe.TableauAltitudeDistance(AxeChoisi, self.MonImage, self.LesAxes, self.ImageAffichage)
        NombreDuneAxe = self.BilanDunesAxe[AxeChoisi][1]
        MoyenneLongeurOndeAxe = self.BilanDunesAxe[AxeChoisi][2]
        MoyenneHauteurAxe = self.BilanDunesAxe[AxeChoisi][3]
        fenVisualiseAxe = Toplevel()
        fenVisualiseAxe.title("Profil de l'axe " + str(AxeChoisi) + " - Analyse dunes 2018")
        VisualiserProfil.VisualiserProfil(fenVisualiseAxe, AxeChoisi, ListeCouleurs[AxeChoisi], XCoordonnee, YCoordonnee, NombreDuneAxe, MoyenneLongeurOndeAxe, MoyenneHauteurAxe)
                   
    def RemplirTableauResultats(self):
        for i in range (0, self.NombreAxes):
            self.Table.insert('', 'end', str(i), text='Axe ' + str(i), tags = ('Color' + str(i)))
            self.Table.tag_configure('Color' + str(i), background=ListeCouleurs[i])
        
        for i in range (0, shape(self.TableauAnalyseImageAxe)[0]):
            self.Table.insert(str(self.TableauAnalyseImageAxe[i][0]), 'end', values = (str(self.TableauAnalyseImageAxe[i][1]), str(self.TableauAnalyseImageAxe[i][2]), str(self.TableauAnalyseImageAxe[i][3])))
            