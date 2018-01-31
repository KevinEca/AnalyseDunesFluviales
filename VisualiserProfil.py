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

        # Comment rendre dynamique affiche courbe ?
        self.fig = plt.figure(figsize=(6, 4))
        plt.xlabel('Distance (m)')
        plt.ylabel('Altitude (m)')
        plt.title('Vue de profil axe ' + str(self.NumeroAxe))
        ax = self.fig.add_subplot(111)
        ax.plot(CoordonneesProfilX, CoordonneesProfilY)
         
        graph = FigureCanvasTkAgg(self.fig, master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=2, column=0, columnspan = 2)
        
    def ExportProfil(self):
        f = filedialog.asksaveasfilename()
        if f:
            self.fig.savefig(f)
