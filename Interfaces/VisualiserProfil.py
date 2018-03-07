from tkinter import *
from scipy import array
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import searchsorted

ListeCouleurs = ["blue", "red", "sienna", "chartreuse", "darkgreen", "deepskyblue", "crimson", "darkorange", "yellow", "purple"]

class VisualiserProfil(Frame):  

    def __init__(self, fenetre, NumeroAxe = 0, CouleurAssocie = 'black', CoordonneesProfilX = array([0]), CoordonneesProfilY = array([0]), NombreDunes = 0, LongeurOndeMoyenne = 0, HauteurMoyenne = 0):
        self.window = fenetre
        
        self.CoordonneesProfilX = CoordonneesProfilX
        self.CoordonneesProfilY = CoordonneesProfilY
        self.NumeroAxe = NumeroAxe
        
        # Cette donnée est sauvegardée pour éviter de la recalculer à chaque fois
        self.MaxX = max(self.CoordonneesProfilX)
        
        # Création de nos widgets
        Label(fenetre, text="Profil dunes axe " + str(self.NumeroAxe), font=("Courier", 20), fg = CouleurAssocie).pack(side=TOP)
        Button(fenetre, text="Export profil", command = lambda : self.ExportProfil(), height = 1, width = 25).pack(side=TOP)
        Label(fenetre, text = "Nombre de dunes: " + str(NombreDunes) + "    Longeur d'onde moyenne: " + str(LongeurOndeMoyenne) + "m    Hauteur moyenne: " + str(HauteurMoyenne) + "cm").pack(side=TOP)


        MaFrame = Frame(fenetre)
        MaFrame.pack(side=TOP, fill = BOTH, expand = 1)
        
        # Comment afficher correctement son graphique
        # https://python4astronomers.github.io/plotting/advanced.html
        self.fig = plt.figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(CoordonneesProfilX, CoordonneesProfilY)
        self.ax.set_xlabel("Distance (m)")
        self.ax.set_ylabel("Altitude (m)")
        self.ax.set_title("Vue de profil axe " + str(self.NumeroAxe))
        
        # On change les valeurs min/max pour la légende du graphique afin d'éviter d'occuper de la place pour des valeurs qui ne sont pas atteinte (comme 0m d'altitude par exemple)
        self.ax.set_ylim(min(CoordonneesProfilY) - 0.3, max(CoordonneesProfilY) + 0.3)
         
        # On affiche le graphe matplotlib, et on le praramètre pour que ces dimensions s'adaptent à la taille de la fenêtre
        graph = FigureCanvasTkAgg(self.fig, master=MaFrame)
        graph.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # On prépare de quoi faire les lignes horizonale/verticale pour cibler la valeur du graphe que l'on cible avec le curseur de la souris
        self.lx = self.ax.axhline(color='k', linewidth = 1)  # the horiz line
        self.ly = self.ax.axvline(color='k', linewidth = 1)  # the vert line
        # Localisation du texte qui affichera les valeurs numériques du point ciblé
        self.txt = self.ax.text(0.7, 0.9, '', transform=self.ax.transAxes)
        
        # On associe un évènement quand l'on déplace le curseur de la souris sur le graphique matplotlib
        self.fig.canvas.mpl_connect ('motion_notify_event', self.mouse_move)
        
    # Évènement inspiré par celui sur https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
    def mouse_move(self, event):

        if (not event.inaxes):
            return

        x = event.xdata
        
        # Ce texte est pour éviter les erreurs si l'on place le curseur de la souris (dans sa coordonnée X)
        # à des valeurs plus grande que celle utilisées dans le tableau de valeur générant le graphique
        if (x > self.MaxX):
            return

        # La recherche du point de la courbe dont sa coordonnée en X et la plus proche de celle pointée par le curseur de la souris
        indx = searchsorted(self.CoordonneesProfilX, [x])[0]
        x = self.CoordonneesProfilX[indx]
        y = self.CoordonneesProfilY[indx]
        # Mise à jour de la position des lignes horizontale/verticale
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('Dist = %1.2f, Alti = %1.2f' % (x, y))
        self.fig.canvas.draw()
        
    def ExportProfil(self):
        f = filedialog.asksaveasfilename()
        if f:
            # Avant de sauvegarder, nous allons enlever les lignes horizontale/verticale
            self.lx.remove()
            self.ly.remove()
            
            # On sauvegarde l'image
            self.fig.savefig(f)
            
            # On remet les traits
            self.lx = self.ax.axhline(color='k')  # the horiz line
            self.ly = self.ax.axvline(color='k')  # the vert line
