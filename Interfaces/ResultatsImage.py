from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from scipy import array, shape
from numpy import asmatrix
from TraitementImage import ImageDune, AlgorithmeImageComplete, ExportTXT

class ResultatsImage(Frame):  

    def __init__(self, fenetre, MonImage = None, ImageAffiche = [0], SeuilDetectionDune = 0):
        
        self.MonImage = MonImage
        self.ImageAffichage = ImageAffiche
        self.DetectionDune = SeuilDetectionDune
        self.ImageAAfficher = 0 # variable ne pouvant être une variable locale, sinon l'image n'apparaît pas à l'affichage
        
        # Création d'une sous frame pour placer correctement les divers éléments sur la moitié gauche de la fenêtre
        FrameMenu = Frame(fenetre)
        FrameMenu.pack(side=LEFT, fill = BOTH, expand = 1)
        
        # Création de nos widgets
        Button(FrameMenu, text='Export des résultats', command = lambda : self.ExportTxt()).pack(side=TOP)

        self.FrameTable = Frame(FrameMenu, height=255, width = 255, bd=1, relief=SUNKEN)
        self.FrameTable.pack(side=TOP, fill = BOTH, expand = 1)
        
        self.Table = ttk.Treeview(self.FrameTable, columns=('Nombre', 'LongOnde', 'HautDune'))
        self.VerticalBarreTable = ttk.Scrollbar(self.FrameTable, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.VerticalBarreTable.set)
        
        self.Table['show'] = 'headings' # On utilise pas la colonne avec les + (on ne l'affiche pas)
        self.Table.pack(side=LEFT, fill = BOTH, expand = 1)
        self.VerticalBarreTable.pack(side=RIGHT, fill = Y)
        
        self.Table.column('Nombre', width=100, anchor='center')
        self.Table.heading('Nombre', text='Nb Dunes')
        self.Table.column('LongOnde', width=150, anchor='center')
        self.Table.heading('LongOnde', text="Longueur d'onde (m)")
        self.Table.column('HautDune', width=140, anchor='center')
        self.Table.heading('HautDune', text="Hauteur dune (cm)")
        
        self.Canevas = Canvas(fenetre)
        self.ImageAAfficher = ImageTk.PhotoImage(self.ImageAffichage)
        self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAAfficher)
        self.Canevas.config(width=self.ImageAffichage.size[0], height=self.ImageAffichage.size[1])
        self.Canevas.pack(side=RIGHT)
        
        self.RemplirTableauResultats()
        self.TableauAnalyseImage = [0,0,0,0,0]
        self.BilanDunesImage = [0,0,0]
        
        AlgorithmeImageComplete.FiltrageLaplacien(MonImage)

    def ExportTxt(self):
        ExportTXT.ExportResultatsDunes(self.TableauAnalyseImage, self.MonImage, self.BilanDunesImage)
    
    def RemplirTableauResultats(self, ResultatsDunes = array([[0,0,0]])):
        NombreDunes = shape(ResultatsDunes)[0]
        for i in range (0, NombreDunes):
            self.Table.insert('', 'end', str(i), text='Axe ' + str(i), values = (str(ResultatsDunes[i][0]), str(ResultatsDunes[i][1]), str(ResultatsDunes[i][2])))