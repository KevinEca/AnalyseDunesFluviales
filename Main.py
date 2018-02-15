from tkinter import Tk
from Interfaces import MenuPrincipal

fenetre = Tk()
fenetre.title("Menu principal - Analyse dunes 2018")
# On empèche l'utilisateur de redimensionner la taille de la fenêtre
fenetre.resizable(width=False, height=False)
interface = MenuPrincipal.MenuPrincipal(fenetre)
interface.mainloop()