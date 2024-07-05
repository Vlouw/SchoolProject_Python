# -*- coding: utf8 -*-

# -------------------------------------------------------------
# Auteur  : Henri-Paul Bolduc
#           Elisabeth Fortin
#           Nelson Peralta Matute
# Cours   : 420-C31-IN - GENIE LOGICIEL I : CONCEPTION ET GESTION
# TP 2    : Jeu Carre Rouge
# Fichier : vues.py
# -------------------------------------------------------------

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from modeles import *
# -------------------------------------------------------------

# Fenetre du programme 
class FenetrePrincipale:
    @staticmethod
    def show(root):
        taille = 480                              # En pixels
        root.title("Jeu Carre Rouge")             # Modifie le titre de la fenetre
        root.geometry("{0}x{0}".format(taille))   # Modifie la taille de la fenetre
# -------------------------------------------------------------

# Fenetre score
class FenetreScore(tk.Toplevel):
    def __init__(self, parent, openTous, openFile, deleteInsideFile):
        # Initialisation de la fenetre score
        super().__init__(parent)
        self.geometry('480x480')
        self.title('Score')      
       
        # Boite de ScrolledText
        self.scoreText = ScrolledText(self, height=25, width=53)
        
        # Creation des boutons
        self.scoreTous =            tk.Button(self, text='Afficher tous\nles scores', width = 12, height = 2, command=openTous)
        self.ouvrirFichierScore =   tk.Button(self, text='Ouvrir un\nfichier score',  width = 12, height = 2, command=openFile)  
        self.deleteScore =          tk.Button(self, text='Effacer Score\n(Fichiers)', width = 12, height = 2, command=deleteInsideFile)
        self.close =                tk.Button(self, text='Fermer',                    width = 12, height = 2, command=self.destroy)
        
        # Couleur
        self.configure(background = 'red')        
        self.scoreText.configure(background = 'black', foreground = 'white smoke')        
        self.scoreTous.configure(background = 'gray6', foreground = 'white smoke')
        self.ouvrirFichierScore.configure(background = 'gray6', foreground = 'white smoke')
        self.deleteScore.configure(background = 'red3', foreground = 'white smoke')
        self.close.configure(background = 'gray6', foreground = 'white smoke') 
        
        # Pack / Positionnement
        self.scoreText.pack(expand = True, pady = 20)        
        self.scoreTous.pack(side = "left", padx = 12)
        self.ouvrirFichierScore.pack(side = "left", padx = 12)
        self.deleteScore.pack(side = "left", padx = 12)
        self.close.pack(side = "left", padx = 12)
        
    
    def writeScore(self, lignes, bool):        
        # Compteur
        i = 0
        # Changer le bouton delete à Fichier
        self.deleteScore.configure(text = 'Effacer Score\n(Fichiers)')        
        
        # Effacer le contenu de ScrolledText
        if bool == 0 :
            self.deleteText()
            self.deleteScore.configure(text = 'Effacer Score\n(Ds le .txt)')
        
        # Activer la boite ScrolledText
        self.scoreText.configure(state ='normal')
        
        # Ecrire le texte du fichier dans ScrolledText
        for item in lignes :
            for element in item :                
                if i == 0:
                    self.scoreText.insert(tk.INSERT, "{:<8}".format(element))                    
                    i = 1
                
                elif i == 1:
                    self.scoreText.insert(tk.INSERT, " (" + element + ")")
                    self.scoreText.insert(tk.INSERT,"\n")
                    i = 2
                
                elif i == 2:                    
                    self.scoreText.insert(tk.INSERT,"{:<8}".format(element))
                    self.scoreText.insert(tk.INSERT,"\n")
                    self.scoreText.insert(tk.INSERT,"{:-<53}".format(''))
                    self.scoreText.insert(tk.INSERT,"\n")
                    i = 3
                
                elif i <= 7:
                    self.scoreText.insert(tk.INSERT,"{:<8}".format(element))
                    i += 1
                    
                else:
                    self.scoreText.insert(tk.INSERT,"{:<}".format(element))
                    self.scoreText.insert(tk.INSERT,"\n")
                    i = 3            

        self.scoreText.insert(tk.INSERT,"\n")
        self.scoreText.insert(tk.INSERT,"{:-<53}".format(''))
        self.scoreText.insert(tk.INSERT,"\n\n")
        
        # Making the text read only 
        self.scoreText.configure(state ='disabled')    
        
    def deleteText(self): 
        self.scoreText.configure(state ='normal')
        self.scoreText.delete('0.0', 'end') 
        self.scoreText.configure(state ='disabled')                      
# -------------------------------------------------------------
 
# Vue Main Menu     
class MainMenuUI:
    def __init__(self, root, nouvellePartie, scores):
        # Creation des frames
        self.frameNom = tk.LabelFrame(root)
        self.frameOpt = tk.LabelFrame(root)  
        
        # Creation du champs text
        self.eti = tk.Label(root, text='Jeu Carre Rouge', font= ('Arial', 25,'underline'))
        self.nomText = tk.Label(self.frameNom, text='Nom du joueur', font= ('Arial', 8))
        self.nom = tk.Entry(self.frameNom, width = 15, justify = 'center')
        self.nom.insert(0, "Don Juan")   
    
        # Creation des boutons
        self.btnNP   = tk.Button(root, text='Nouvelle Session',  font = 18,  width = 15, command = nouvellePartie)
        self.btnSco  = tk.Button(root, text='Scores',            font = 18,  width = 15, command = scores)
        self.btnQui  = tk.Button(root, text='Quitter',           font = 18,  width = 15, command = root.destroy)
        
        # Creation des boutons radios
        self.radioValue = tk.StringVar()
        
        
        # indicatoron = 0, pas de point
        self.R1 = tk.Radiobutton(self.frameOpt, variable=self.radioValue, indicatoron = 0, width = 15, text="Facile",      value="Facile")
        self.R2 = tk.Radiobutton(self.frameOpt, variable=self.radioValue, indicatoron = 0, width = 15, text="Moyen",       value="Moyen")
        self.R3 = tk.Radiobutton(self.frameOpt, variable=self.radioValue, indicatoron = 0, width = 15, text="Difficile",   value="Difficile")
        self.R4 = tk.Radiobutton(self.frameOpt, variable=self.radioValue, indicatoron = 0, width = 15, text="Progressif",  value="Progressif") 
        
        self.radioValue.set("Facile")
        
        # Couleur
        root.configure(background = 'red')
        
        self.frameNom.configure(background = 'orange red')
        self.frameOpt.configure(background = 'orange red')
        
        self.eti.configure(background = 'red', foreground = 'white smoke')
        self.nomText.configure(background = 'orange red', foreground = 'white smoke')
        self.nom.configure(background = 'black', foreground = 'white smoke')
        
        self.btnNP.configure(background = 'gray6', foreground = 'white smoke')
        self.btnSco.configure(background = 'gray6', foreground = 'white smoke')
        self.btnQui.configure(background = 'gray6', foreground = 'white smoke')  

        self.R1.configure(background = 'gray20', foreground = 'white smoke', selectcolor = 'orange red')
        self.R2.configure(background = 'gray20', foreground = 'white smoke', selectcolor = 'orange red')
        self.R3.configure(background = 'gray20', foreground = 'white smoke', selectcolor = 'orange red')
        self.R4.configure(background = 'gray20', foreground = 'white smoke', selectcolor = 'orange red')
      
        
        # Pack
        self.eti.pack(pady = 20)
        self.btnNP.pack()
        
        self.frameNom.pack()
        self.nomText.pack()
        self.nom.pack()
        
        self.frameOpt.pack()
        self.R1.pack(anchor = 'w')
        self.R2.pack(anchor = 'w')
        self.R3.pack(anchor = 'w')
        self.R4.pack(anchor = 'w')
        
        self.btnSco.pack(pady = 20)
        self.btnQui.pack()
# -------------------------------------------------------------

class NewGameUI(tk.Toplevel):
    def __init__(self, parent, difficulte, nomJoueur, newSession):
        # Initialisation de la fenetre score
        super().__init__(parent)
        self.geometry('900x605')
        self.title('Partie : ' + difficulte)

        # Création des frames        
        self.frameTimer = tk.LabelFrame(self)
        self.frameJeu = tk.LabelFrame(self)
        self.frameScore = tk.LabelFrame(self)

        self.frameTimer.grid(row=0, column=0, sticky="nsew")
        self.frameJeu.grid(row=1, column=0, sticky="nsew")
        self.frameScore.grid(rowspan=2, row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=550)
        self.grid_columnconfigure(1, weight=350)
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=600)
        
        # Création du timer
        self.timeText = tk.Label(self.frameTimer, text="Temps (sec)", font= ('Arial', 10,'underline'), justify = 'center')        
        self.time = tk.Label(self.frameTimer, text="0", font= ('Arial', 10), justify = 'center')        
        
        self.timeText.pack(fill='both')
        self.time.pack(fill='both') 
        
        # Boite de ScrolledText
        self.scoreText = ScrolledText(self.frameScore, font= ('Arial', 10), width = 5, height = 38)
        self.scoreText.pack(fill='both')
        self.updateScore(newSession.readNewSession())        
                
        # Couleur
        self.frameTimer.configure(background = 'red')        
        self.timeText.configure(background = 'red' )
        self.time.configure(background = 'red')        
        self.scoreText.configure(background = 'black', foreground = 'white smoke') 
        
    def updateScore(self, lignes):        
        # Compteur
        i = 0        

        self.deleteText()
        
        # Activer la boite ScrolledText
        self.scoreText.configure(state ='normal')
        
        # Ecrire le texte du fichier dans ScrolledText
        for item in lignes :
            for element in item :                
                if i == 0:
                    self.scoreText.insert(tk.INSERT, element)
                    self.scoreText.insert(tk.INSERT,"\n")                   
                    i = 1
                
                elif i == 1:
                    self.scoreText.insert(tk.INSERT, "--------------------------")
                    self.scoreText.insert(tk.INSERT,"\n")  
                    i = 2
                
                elif i == 2:                    
                    i = 3
                    
                else:
                    self.scoreText.insert(tk.INSERT,element)
                    self.scoreText.insert(tk.INSERT,"\n")
        
        # Making the text read only 
        self.scoreText.configure(state ='disabled')    
        
    def deleteText(self): 
        self.scoreText.configure(state ='normal')
        self.scoreText.delete('0.0', 'end') 
        self.scoreText.configure(state ='disabled')
        
    def updateTimer(self, timeAlive):
        self.time.configure(text=round(timeAlive,2))
        
    def getFrameJeu(self):
        return self.frameJeu

# -------------------------------------------------------------