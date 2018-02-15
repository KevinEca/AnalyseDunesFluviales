from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from scipy import array, shape
from Interfaces import VisualiserProfil
from TraitementImage import AlgorithmeAxe

ListeCouleurs = ["blue", "red", "sienna", "chartreuse", "darkgreen", "deepskyblue", "crimson", "darkorange", "yellow", "purple"]

class ResultatsAxes(Frame):  

    def __init__(self, fenetre, MonImage = None, ImageAffiche = [0], SeuilDetectionDune = 0, LesAxes = None):
        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.MonImage = MonImage
        self.ImageAffichage = ImageAffiche
        self.DetectionDune = float(SeuilDetectionDune) / 100
        self.LesAxes = LesAxes
        self.ImageAAfficher = 0 # variable ne pouvant être une variable locale, sinon l'image n'apparaît pas à l'affichage
        self.NombreAxes = self.LesAxes.NombreAxes()
        
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
        #self.RemplirTableauResultats(self.DetectionDunes())
        self.RemplirTableauResultats(AlgorithmeAxe.DetectionDunes(self.MonImage, self.LesAxes, self.ImageAffichage, self.DetectionDune))
        
    def PlacementAxes(self):
        for i in range (0, self.NombreAxes):
            self.Canevas.create_line(self.LesAxes.CoordonneesAxe(i), fill=ListeCouleurs[i])

    def ExportTXT(self):
        pass
    
    def VisualiserProfil(self):
        AxeChoisi = int(self.NumeroAxeChoisi.get())
        XCoordonnee, YCoordonnee = AlgorithmeAxe.TableauAltitudeDistance(AxeChoisi, self.MonImage, self.LesAxes, self.ImageAffichage)
        
        fenVisualiseAxe = Toplevel()
        fenVisualiseAxe.title("Profil de l'axe " + str(AxeChoisi) + " - Analyse dunes 2018")
        VisualiserProfil.VisualiserProfil(fenVisualiseAxe, AxeChoisi, ListeCouleurs[AxeChoisi], XCoordonnee, YCoordonnee)
                   
    def RemplirTableauResultats(self, ResultatsDunesAxes = array([[0,0,0,0]])):
        for i in range (0, self.NombreAxes):
            self.Table.insert('', 'end', str(i), text='Axe ' + str(i), tags = ('Color' + str(i)))
            self.Table.tag_configure('Color' + str(i), background=ListeCouleurs[i])
        
        for i in range (0, shape(ResultatsDunesAxes)[0]):
            self.Table.insert(str(ResultatsDunesAxes[i][0]), 'end', values = (str(ResultatsDunesAxes[i][1]), str(ResultatsDunesAxes[i][2]), str(ResultatsDunesAxes[i][3])))
            