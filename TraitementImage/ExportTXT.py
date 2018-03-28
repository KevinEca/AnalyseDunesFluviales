import datetime
from tkinter import filedialog, messagebox

def ExportResultatsDunesAxe(TableauInfoDunes = [0,0,0,0,0,0,0], Image = None, NumeroAxe = 0, CoordonneesAxe = None, DonneesBilanAxe = [0,0,0,0], DetectionDune = 10):
    NombreDeDunesTotal = len(TableauInfoDunes)
    j = 0 # Indice de la dune que l'on lit dans le tableau
        
    if (NombreDeDunesTotal > 0):
        IdAxe = TableauInfoDunes[j][0] # On commence par lire les dunes faisant partie de celles qui sont rattachées au premier axe ayant au moins une dune
                
        #Tant que nous sommes pas sur une dune de l'axe choisi on passe à la dune suivante
        while(IdAxe != NumeroAxe and j < NombreDeDunesTotal):
            j += 1
            if (j < NombreDeDunesTotal): # Si nous avons pas atteint la fin du tableau (on incrémente j néanmoins pour sortir du while)
                IdAxe = TableauInfoDunes[j][0]
                
        # Si l'axe choisi possède au moins 1 dune, on demande à l'utilisateur où sauvegarder le fichier txt
        if(IdAxe == NumeroAxe and j < NombreDeDunesTotal):
            
            f = filedialog.asksaveasfilename(defaultextension='.txt',filetypes = (("Texte","*.txt"),("CSV","*.csv*")))
            if f:
                with open(f, "w") as fic:
                    EnteteFichierTxt(fic, Image, DetectionDune)
                    # Reste de l'entête du fichier
                    print(f"""Numéro axe choisi {NumeroAxe} constitué des pixels aux extrémités {CoordonneesAxe}
Nombre de dunes = {DonneesBilanAxe[1]} | Longeur d'onde moyenne = {DonneesBilanAxe[2]}m | Hauteur moyenne {DonneesBilanAxe[3]}cm
IdDune;Longeur d'onde(m);Hauteur(cm);AltitudeCreux1(m);AltitudePic(m);AltitudeCreux2(m)""", file = fic)
                        
                    # Pour chacune des dunes de l'axe voulu
                    while(IdAxe == NumeroAxe and j < NombreDeDunesTotal):
                        print(f"{TableauInfoDunes[j][1]};{TableauInfoDunes[j][2]};{TableauInfoDunes[j][3]};{TableauInfoDunes[j][4]};{TableauInfoDunes[j][5]};{TableauInfoDunes[j][6]}", file = fic)
                        j += 1
                        if (j < NombreDeDunesTotal): # Si nous avons pas atteint la fin du tableau (on incrémente j néanmoins pour sortir du while)
                            IdAxe = TableauInfoDunes[j][0]
        else:
            messagebox.showerror("Erreur", "Aucune dune n'a été trouvé pour l'axe choisi")
    else:
        messagebox.showerror("Erreur", "Aucune dune n'a été trouvé")

def ExportResultatsDunesAxes(TableauInfoDunes = [0,0,0,0,0,0], Image = None, Axes = None, DonneesBilanAxe = [0,0,0,0], DetectionDune = 10):
    NombreDeDunesTotal = len(TableauInfoDunes)
    j = 0 # Indice de la dune que l'on lit dans le tableau
        
    if (NombreDeDunesTotal > 0):
        IdAxe = TableauInfoDunes[j][0] # On commence par lire les dunes faisant partie de celles qui sont rattachées au premier axe ayant au moins une dune

        f = filedialog.asksaveasfilename(defaultextension='.txt',filetypes = (("Texte","*.txt"),("CSV","*.csv*")))
        if f:
            with open(f, "w") as fic:
                EnteteFichierTxt(fic, Image, DetectionDune)
            
                # On affiche les informations générales pour chacun des axes
                NombreAxe = len(DonneesBilanAxe)
                for i in range (0, NombreAxe):
                    print(f"""Numéro axe {i} constitué des pixels aux extrémités {Axes.InfosAxe(i).getCoordonneesAxe()}
Nombre de dunes = {DonneesBilanAxe[i][1]} | Longeur d'onde moyenne = {DonneesBilanAxe[i][2]}m | Hauteur moyenne {DonneesBilanAxe[i][3]}cm""", file = fic)
                
                # La légende pour comprendre la structure des informations listés pour chacune des dunes
                print(f"""IdAxe;IdDune;Longeur d'onde(m);Hauteur(cm);AltitudeCreux1(m);AltitudePic(m);AltitudeCreux2(m)""", file = fic)
                
                while(j < NombreDeDunesTotal):
                    print(f"{TableauInfoDunes[j][0]};{TableauInfoDunes[j][1]};{TableauInfoDunes[j][2]};{TableauInfoDunes[j][3]};{TableauInfoDunes[j][4]};{TableauInfoDunes[j][5]};{TableauInfoDunes[j][6]}", file = fic)
                    j += 1
    else:
        messagebox.showerror("Erreur", "Aucune dune n'a été trouvé")          
                
def ExportResultatsDunes(TableauInfoDunes = [0,0,0,0,0], Image = None, DonneesBilanImage = [0,0,0], DetectionDune = 10):
    NombreDeDunesTotal = len(TableauInfoDunes)
    j = 0 # Indice de la dune que l'on lit dans le tableau
        
    if (NombreDeDunesTotal > 0):
        f = filedialog.asksaveasfilename(defaultextension='.txt',filetypes = (("Texte","*.txt"),("CSV","*.csv*")))
        if f:
            with open(f, "w") as fic:
                EnteteFichierTxt(fic, Image, DetectionDune)
                # Reste de l'entête du fichier
                print(f"""Analyse de l'image complète : nombre de dunes {DonneesBilanImage[0]} | Longueur d'onde moyenne = {DonneesBilanImage[1]} | Hauteur moyenne = {DonneesBilanImage[2]}
IdDune;Longeur d'onde(m);Hauteur(cm);AltitudeCreux1(m);AltitudePic(m);AltitudeCreux2(m)""", file = fic)

                while(j < NombreDeDunesTotal):
                    print(f"{DonneesBilanImage[j][0]};{DonneesBilanImage[j][1]};{DonneesBilanImage[j][2]};{DonneesBilanImage[j][3]};{DonneesBilanImage[j][4]};{DonneesBilanImage[j][5]}", file = fic)
                    j += 1
    else:
        messagebox.showerror("Erreur", "Aucune dune n'a été trouvé")
        
def EnteteFichierTxt(FichierTexteOuvert, Image = None, DetectionDune = 10):
    if Image.getSensCourantGauche() == True:
        SensCourant = "gauche"
    else:
        SensCourant = "droite"
        
    print(f"""Traitement analyse dunes de l'image " {Image.getNomImage()} " fait le {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
Altitude minimum = {Image.getAltitudeMin()} Résolution altitude = {Image.getResolutionAltitude()}
Detection des dunes (petites) dès {DetectionDune}m
Le sens du courant choisi est vers la {SensCourant}""", file = FichierTexteOuvert)
    
    