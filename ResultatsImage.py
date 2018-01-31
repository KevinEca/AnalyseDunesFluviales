from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from scipy import array, shape

class ResultatsImage(Frame):  

    def __init__(self, fenetre, ImageOriginal = [0], ImageAffiche = [0], SeuilDetectionDune = 0, ResolutionNiveauGris = 0):
        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.ImageOrigine = ImageOriginal
        self.ImageAffichage = ImageAffiche
        self.DetectionDune = SeuilDetectionDune
        self.ResolutionImage = ResolutionNiveauGris
        self.ImageAAfficher = 0 # variable ne pouvant être une variable locale, sinon l'image n'apparaît pas à l'affichage
        
        # Création de nos widgets
        Button(self, text='Export des résultats', command = lambda : self.ExportTXT()).grid(row=0, column=0, columnspan = 1)

        self.FrameTable = Frame(self, height=255, width = 255, bd=1, relief=SUNKEN)
        self.FrameTable.grid(row=1, column=0)
        
        self.Table = ttk.Treeview(self.FrameTable, columns=('Nombre', 'LongOnde', 'HautDune'))
        self.VerticalBarreTable = ttk.Scrollbar(self.FrameTable, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.VerticalBarreTable.set)
        
        self.Table['show'] = 'headings' # On utilise pas la colonne avec les + (on ne l'affiche pas)
        self.Table.pack(side=LEFT)
        self.VerticalBarreTable.pack(side=RIGHT, fill = Y)
        
        self.Table.column('Nombre', width=100, anchor='center')
        self.Table.heading('Nombre', text='Nb Dunes')
        self.Table.column('LongOnde', width=150, anchor='center')
        self.Table.heading('LongOnde', text="Longueur d'onde (m)")
        self.Table.column('HautDune', width=140, anchor='center')
        self.Table.heading('HautDune', text="Hauteur dune (cm)")
        
        self.Canevas = Canvas(self)
        self.ImageAAfficher = ImageTk.PhotoImage(self.ImageAffichage)
        self.Canevas.create_image(0,0,anchor=NW,image = self.ImageAAfficher)
        self.Canevas.config(width=self.ImageAffichage.size[0], height=self.ImageAffichage.size[1])
        self.Canevas.grid(row=0, column=1, rowspan = 2)
        # On redéfini la taille du caneva associé à la miniature de l'image sur l'interface graphique
        #self.Canevas.config(width=self.ImageOrigine.size[0], height=self.ImageOrigine.size[1])
        
        self.RemplirTableauResultats()

    def ExportTXT(self):
        pass
    
    def RemplirTableauResultats(self, ResultatsDunes = array([[0,0,0]])):
        NombreDunes = shape(ResultatsDunes)[0]
        for i in range (0, NombreDunes):
            self.Table.insert('', 'end', str(i), text='Axe ' + str(i), values = (str(ResultatsDunes[i][0]), str(ResultatsDunes[i][1]), str(ResultatsDunes[i][2])))