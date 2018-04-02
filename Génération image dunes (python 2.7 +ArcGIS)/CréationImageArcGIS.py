from Tkinter import *
import tkFileDialog
import ttk
import os

# Le fonctionnement de la création du image .TIF à partir de données raster provient de la source suivante
# http://desktop.arcgis.com/fr/arcmap/latest/tools/data-management-toolbox/copy-raster.htm

# Il semble néanmoins aussi possible de créer les images .TIF à partir de l'outil en ligne "Copy Raster" disponible seulement de la manière suivante
# (dans la barre de menu) GeoProcessing → Search For Tool → copy raster (data management)
# Cependant, je n'ai jamais pu sortir une image .TIF à partir de cette méthode, d'où l'usage d'une interface Python que voici

class MenuPrincipal(Frame):
    
    def __init__(self, fenetre):
        Frame.__init__(self, fenetre)
        self.pack(fill=BOTH)
        
        self.NomDossierParentGDB = StringVar()
        self.NomFichierTableGDB = StringVar()
        self.NomImageTIF = StringVar()

        # Ceci est une valeur par défaut utilisée pour les tests de fonctionnement
        #self.NomFichierTableGDB.set("Default.gdb\\test16bit")
        
        Label(self, text="Dossier parent GDB").grid(row=0, column=0)
        Entry(self, width=40, textvariable=self.NomDossierParentGDB).grid(row=0, column=1)
        Button(self, text='Choisir dossier GDB', command = lambda : self.ChoixDossierGDB()).grid(row=0, column=2)

        Label(self, text="Nom fichier GDB + raster").grid(row=1, column=0)
        Entry(self, width=40, textvariable=self.NomFichierTableGDB).grid(row=1, column=1)
        Label(self, text="exemple : Monfichier.gdb\\MonRaster").grid(row=2, column=0, columnspan = 3)

        Label(self, text=".TIF de sortie").grid(row=3, column=0)
        Entry(self, width=40, textvariable=self.NomImageTIF).grid(row=3, column=1)
        Button(self, text='Emplacement', command = lambda : self.ChoixTIF()).grid(row=3, column=2)
        Label(self, text="Attention penser à ajouter l'altitude minimum/maximum au nom de l'image pour pouvoir la traiter").grid(row=4, column=0, columnspan = 3)
        Label(self, text="Exemple : LoireNord_1,92_12.7.tif").grid(row=5, column=0, columnspan = 3)

        Label(self, text="Niveau de gris de l'image").grid(row=6, column=0)
        self.ChoixResolutionImage = ttk.Combobox(self, state="readonly")
        self.ChoixResolutionImage['values'] = ("16 bits", "8 bits")
        self.ChoixResolutionImage.set("16 bits")
        self.ChoixResolutionImage.grid(row=6, column=1)
        
        Button(self, text='Créer .TIF', command = lambda : self.CreationTIF()).grid(row=7, column=0, columnspan = 3)

        # Ce label est juste pour indiquer à l'utilisateur si l'image a été crée ou non
        self.MessageRetour = Label(self, text="")
        self.MessageRetour.grid(row=8, column=0, columnspan = 3)

    def ChoixDossierGDB(self):
        GDBdossierChoisi = tkFileDialog.askdirectory()

        # Si l'utilisateur a bien choisi un répertoire, on rempli l'élément Entry du choix fait
        if GDBdossierChoisi != "":
            self.NomDossierParentGDB.set(GDBdossierChoisi)

    def ChoixTIF(self):
        NomFichierTIF = tkFileDialog.asksaveasfilename()
        
        if NomFichierTIF != "":
            # Si l'utilisateur n'a pas mit le type de fichier, on le rajoute manuellement
            if NomFichierTIF[-4:] != ".tif" or len(NomFichierTIF < 5):
                NomFichierTIF += ".tif"
            self.NomImageTIF.set(NomFichierTIF)

    def CreationTIF(self):
        try:
            import arcpy

            # Le nombre de bit occupant les 2 premiers caractères ("8 " ou "16"), on peux procéder ainsi
            NombreBitsImage = int(self.ChoixResolutionImage.get()[:2])

            # ValeurNoData corespond au niveau de gris que l'on associe si aucune données ne peux être obtenue sur le niveau d'altitude
            # Il correspond ainsi aux mesures n'ayant pas pu être faites, car étant en surface
            # On y attribu la valeur maximale, soit 2^NombreBitsImage - 1
            # pour 8 bits → 255, 16 bits → 65535
            ValeurNoData = 2 ** NombreBitsImage - 1
            # Pour le type de pixel, nous choississons de traiter avec des bits non signés par commodités
            TypePixel = str(NombreBitsImage) + "_BIT_UNSIGNED"
            
            arcpy.env.workspace = self.NomDossierParentGDB.get()

            # documentation sur la compression
            # http://desktop.arcgis.com/fr/arcmap/latest/tools/environments/compression.htm
            
            # La compression "NONE" rend toujours un bug lors de l'affichage
            # https://github.com/ali1234/bitmap2ttf/issues/2
            #arcpy.env.compression = "NONE"
            # PackBits renvoi la même erreur que pour NONE
            #arcpy.env.compression = "PackBits"
            # Comme il y a des bugs avec la librairie Pillow, les images TIFF utilisant la compression lzw ne sont pas corectement prises en charge
            # https://www.bountysource.com/issues/51811624-image-save-as-tiff-image-and-the-compression-parameter-does-not-work
            #arcpy.env.compression = "LZW"
            # même erreur que pour LZW
            #arcpy.env.compression = "LZ77"

            arcpy.env.compression = "LERC"

            arcpy.CopyRaster_management(self.NomFichierTableGDB.get(),self.NomImageTIF.get(), nodata_value = ValeurNoData, pixel_type = TypePixel, scale_pixel_value = True, format = "TIFF", transform = True)
            
            self.MessageRetour['text'] = "Création de l'image terminé"

            # On supprime les fichiers autres que le .TIF généré durant la procédure
            os.remove(self.NomImageTIF.get()[:-4]+".tfw")
            os.remove(self.NomImageTIF.get()+".aux.xml")
            os.remove(self.NomImageTIF.get()+".ovr")
            os.remove(self.NomImageTIF.get()+".xml")

        except:
            self.MessageRetour['text'] = "Erreur lors de la création de l'image"
            #print "Copy Raster example failed."
            #print arcpy.GetMessages()

fenetre = Tk()
fenetre.title("Création image TIF niveaux de gris 8/16 Bits")
# On empèche l'utilisateur de redimensionner la taille de la fenêtre
fenetre.resizable(width=False, height=False)
interface = MenuPrincipal(fenetre)
interface.mainloop()
