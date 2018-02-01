from tkinter import *
from scipy import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ListeCouleurs = ["blue", "red", "sienna", "chartreuse", "darkgreen", "deepskyblue", "crimson", "darkorange", "yellow", "purple"]

class VisualiserProfil(Frame):  

    def __init__(self, fenetre, NumeroAxe = 0, CouleurAssocie = 'black', CoordonneesProfilX = array([0]), CoordonneesProfilY = array([0]), NombreDunes = 0, LongeurOndeMoyenne = 0, HauteurMoyenne = 0):
        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.CoordonneesProfilX = CoordonneesProfilX
        self.CoordonneesProfilY = CoordonneesProfilY
        self.NumeroAxe = NumeroAxe
        
        # Création de nos widgets
        Label(self, text="Profil dunes axe " + str(self.NumeroAxe), font=("Courier", 20), fg = CouleurAssocie).grid(row=0, column=0)
        Button(self, text="Export profil", command = lambda : self.ExportProfil()).grid(row=0, column=1)
        Label(self, text = "Nombre de dunes: " + str(NombreDunes) + "    Longeur d'onde moyenne: " + str(LongeurOndeMoyenne) + "m    Hauteur moyenne: " + str(HauteurMoyenne) + "cm").grid(row=1, column=0, columnspan = 2)

        # Comment afficher correctement son graphique
        # https://python4astronomers.github.io/plotting/advanced.html
        self.fig = plt.figure(figsize=(6, 4))
        ax = self.fig.add_subplot(111)
        ax.plot(CoordonneesProfilX, CoordonneesProfilY)
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Altitude (m)")
        ax.set_title("Vue de profil axe " + str(self.NumeroAxe))
         
        graph = FigureCanvasTkAgg(self.fig, master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=2, column=0, columnspan = 2)
        
    def ExportProfil(self):
        f = filedialog.asksaveasfilename()
        if f:
            self.fig.savefig(f)
