# -*- coding: utf8 -*-

# -------------------------------------------------------------
# Auteur  : Henri-Paul Bolduc
#           Elisabeth Fortin
#           Nelson Peralta Matute
# Cours   : 420-C31-IN - GENIE LOGICIEL I : CONCEPTION ET GESTION
# TP 2    : Jeu Carre Rouge
# Fichier : controlleurs.py
# -------------------------------------------------------------

import os
import time
import math
import random
import tkinter as tk

from tkinter import filedialog, messagebox
from functools import partial
from datetime import datetime
from vues import MainMenuUI, FenetreScore, NewGameUI
from _ast import Try
from modeles import *
from c31Geometry import *
# -------------------------------------------------------------

class MainMenuController:  
    def __init__ (self, root):
        #Importation de root pour ré-utilisation
        self.root = root
        
        # Affichage de la fenetre principale et envoie des commandes boutons
        self.mainMenu = MainMenuUI(self.root, self.nouvellePartie, self.scores)
        
        # Création d'un controlleur des scores
        self.highscore = HighScoreController(self)

    def scores(self):
        # Si la fenetre existe, la detruire sinon ne rien faire
        try:
            self.score.destroy()
        except AttributeError:            
            # Ne rien faire
            bidon = 0
        
        # Ouvrir la fenetre des scores et lui envoyer des commandes bouton
        self.score = FenetreScore(self.root, self.highscore.openTous, self.highscore.openFile, self.highscore.deleteInsideFile)  

    def nouvellePartie(self):
        # Aller checher la difficulte et le nom de la fenetre principale                
        difficulte = self.mainMenu.radioValue.get()        
        nomJoueur = self.mainMenu.nom.get() 
        
        # Création d'un controleur de score pour la nouvelle fenetre
        newSession = HighScoreController(self)
        newSession.newSession(nomJoueur, difficulte)
        
        # Création d'une nouvelle fenetre pour le jeu
        nouvelVue = NewGameUI(self.root, difficulte, nomJoueur, newSession)
        
        # Initialiser la partie
        nouvelpartie = NewGameController(nouvelVue, difficulte, newSession)
        nouvelpartie.start()

# -------------------------------------------------------------

class HighScoreController :    
    def __init__ (self, mainMenu) :        
        # Passer la fenetre principale
        self.mainMenu = mainMenu
        
        # Variable pour ecriture du fichier     
        self.separateur = ";"
        
        # Aller chercher le directory de .py et ajoute \_Log
        self.dir = os.getcwd() + "\\_Log\\"
        
        # Code from GitHub - Creation du dossier s'il n'existe pas
        #------------------------------------------------------
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        #------------------------------------------------------
        #------------------------------------------------------
        
    def openTous(self):       
        # Choisir si on efface [0] le text ou non [1]
        bool = 0
        
        # Passer à traver tous les fichiers et dossier sous self.dir
        files = os.listdir(self.dir)        
        for f in files:
            fichier = open(self.dir + f, 'r')
            self.lignes = HighScoreController.importData(self, fichier)
            
            # Effacer le texte de ScrolledText pour le premier fichier et ensuite ne pas effacer
            if bool == 0:
                self.mainMenu.score.writeScore(self.lignes, bool)
                bool =  1
            else :
                self.mainMenu.score.writeScore(self.lignes, bool)
        
        # Vider la cache nomFichier        
        self.nomFichierAffichage = ''  
    
    def openFile(self):
        #Code de StackOverflow - Prompt choisir un fichier texte dans self.dir et enregistrer son nom *.txt
        #------------------------------------------------------
        self.fichierScore = filedialog.askopenfile(initialdir = self.dir,
                           filetypes =[("Text File", "*.txt")],
                           title = "Choose a file."
                           )
        
        try:
            self.nomFichierAffichage = self.fichierScore.name
        #------------------------------------------------------
        #------------------------------------------------------
        
        except AttributeError:
            return
        
        # Importer le data dans un tableau et lancer l'affichage du .txt choisi        
        self.lignes = HighScoreController.importData(self, self.fichierScore)
        self.mainMenu.score.writeScore(self.lignes, 0) # Effacer le text bool = 0        
  
    
    def deleteInsideFile(self):
        # Si un fichier n'a pas été choisi ou en mode tous les scores, effacer tous les fichiers        
        try :            
            # Effacer le contenu et écrire dans le fichier
            fichier = open(self.nomFichierAffichage, 'w')
            compteurElement = 0   
    
            for item in self.lignes:
                for element in item :
                    compteurElement += 1
                
                    # Ajouter le separateur seulement au 2 premiers items sinon remettre le compteur à 0
                    if compteurElement < 4 :
                        fichier.write(element) # On écrit l'élément dans le fichier
                        fichier.write(self.separateur) # On ajoute le séparateur à chaque ligne
                    elif compteurElement == 4:
                        fichier.write("Deleted") # On ajoute le separateur à chaque ligne
                        fichier.close()
        
            # Importer le data et mettre a jour l'affichage
            fichier = open(self.nomFichierAffichage, 'r')
            self.lignes = HighScoreController.importData(self, fichier)
            self.mainMenu.score.writeScore(self.lignes, 0)
            
        # Erreur quand on a cliquer sur Tous les scores
        except FileNotFoundError :
            self.deleteAllFiles()
        
        # Erreur quand la fenetre load et on click sur effacer
        except AttributeError :
            self.deleteAllFiles()
            
    def deleteAllFiles(self): #All files

        # Validation
        yes = tk.messagebox.askquestion("Delete All files","Are you sure?")
            
        if yes == 'yes' :
            # Delete all files from self.dir
            files = os.listdir(self.dir)        
            for f in files:
                os.remove(self.dir + f)  
        
            # Effacer les scores du texte
            self.mainMenu.score.deleteText()
        
    def importData(self, fichier) :
        # Code source du prof : 04_lire_ecrire_fichier.py
        # -----------------------------------------------------
        contenu = fichier.read() # Lit et renvoie TOUTES les lignes du fichier
        fichier.close() # Obligatoire, on ferme toujours le fichier après son utilisation

        lignes = contenu.split("\n") # On sépare chaque ligne (ensemble de données)

        # On transforme chaque ligne en tableau
        for i in range(0, len(lignes)) :
            lignes[i] = lignes[i].split(self.separateur)
    
        return lignes
        # -----------------------------------------------------
        # -----------------------------------------------------

    def newSession(self, nomJoueur, difficulte) :        
        # Creation d'un fichier .txt et initialisation de son nom
        self.now = datetime.now()
        self.nomFichierSession = "Score_CR_" + self.now.strftime("%Y-%m-%d %Hh%Mm%Ss") + ".txt"
        self.fichierSession = open(self.dir + self.nomFichierSession, "w+") # w+ Creation si n'existe pas        

        # Entrer les donnees de base du fichier
        self.fichierSession.write(nomJoueur)
        self.fichierSession.write(self.separateur)
        self.fichierSession.write(difficulte)
        self.fichierSession.write(self.separateur)
        self.fichierSession.write(self.now.strftime("%Y-%m-%d %Hh%Mm%Ss"))      
        
        # Fermer le fichier
        self.fichierSession.close()
        
    def readNewSession(self) :   
        # Lire le fichier de la session     
        self.fichierSession = open(self.dir + self.nomFichierSession, "r")
        return self.importData(self.fichierSession)
    
    def appendNewSession(self, timeAlive):
        # Ajouter le score à la fin de la partie
        self.fichierSession = open(self.dir + self.nomFichierSession, "a")   
             
        self.fichierSession.write(self.separateur)
        self.fichierSession.write(str(round(timeAlive,2)))
        
        self.fichierSession.close()
         
# -------------------------------------------------------------

class NewGameController:
    def __init__(self, Vue, difficulte, newSession):
        # Importer les parametres
        self.Vue = Vue
        self.difficulte = difficulte
        self.newSession = newSession
        
        # Création du jeu 
        self.aireDeJeu = AireDeJeu(self.Vue.getFrameJeu())
        self.tailleCanvas = AireDeJeu.getTailleCanvas(self.aireDeJeu)
        self.canvasBordure = AireDeJeu.getCanvasBordure(self.aireDeJeu)
        
        # Cote de la bordure
        self.coteGauche = self.canvasBordure
        self.coteDroit = self.tailleCanvas + self.canvasBordure
        self.coteHaut = self.canvasBordure
        self.coteBas = self.tailleCanvas + self.canvasBordure
        
        # After Event (Partir After Event, seulement une fois)
        self.AfterEventOnce = False        
        
    def start(self):
        # Initialisation des variables de controle
        self.isClickingPlayer = False
        self.gameInProgress = False
        
        # Vitesse selon difficulté
        self.setSpeed()
        
        # Initialisation du timer
        self.setTimer()
        
        # Création et positionnement du joueurs et pion
        self.joueurPos = [225, 225]
        self.pionPos = [[100, 100], [300, 85], [85, 350], [355, 340]]
        
        self.joueurSize = 40
        self.pionSize = [[60, 60], [60, 50], [30, 60], [100, 20]] 
        
        self.nbPions = 4
    
        self.joueur = Joueur(self.aireDeJeu.getCanvas(), self.joueurPos[0], self.joueurPos[1], self.joueurSize) 
    
        self.spawnPions()
        
        # Création des reactions de la souris
        self.aireDeJeu.getCanvas().bind('<Motion>', self.motion) 
        self.aireDeJeu.getCanvas().bind('<ButtonPress-1>', self.click)
        self.aireDeJeu.getCanvas().bind('<ButtonRelease-1>', self.unclick)
        
        # Partir after event pour le deplacement des pions et du timer
        if self.AfterEventOnce == False :
            self.afterEventMov = AfterEvent(self.Vue, self.pionMovement, 10) # .01 seconde
            self.afterEventMov.start()
            self.afterEventTime = AfterEvent(self.Vue, self.updateTimer, 10) # .01 seconde
            self.afterEventTime.start()
            self.AfterEventOnce = True

    def setTimer(self):
        # Mettre le temps a 0 et l'ecrire ds la boite texte
        self.timeAlive = 0
        self.Vue.updateTimer(self.timeAlive)
        
    def updateTimer(self):
        # Instancier le temps lorsque le jeu est en progres
        if self.gameInProgress == True:
            self.timeAlive += 0.01
            self.Vue.updateTimer(self.timeAlive)  
    
    def spawnPions(self):
        # Création des pions
        self.listePions = []
        
        counter = 0
        for nvPion in range(self.nbPions):            
            ranDir = random.randint(5, 355) # Direction aléatoire
            
            nvPion = Pion(self.aireDeJeu.getCanvas(), self.pionPos[counter][0], self.pionPos[counter][1], self.pionSize[counter][0], self.pionSize[counter][1], ranDir)
            
            counter = counter + 1
            self.listePions.append(nvPion) 
        
    def motion(self, event):        
        # 4 cotes du joueur, [0] = Gauche, [1] = Droite, [2] = Haut et [3] = Bas
        joueurInter = self.joueur.getSpace()
        
        # Verification collision avec bordure
        if joueurInter[0] <=  self.coteGauche or joueurInter[1] >= self.coteDroit or joueurInter[2] <= self.coteHaut or joueurInter[3] >= self.coteBas:
            if self.gameInProgress == True:
                self.stopGame()
        
        # Déplacer le carré rouge      
        if self.isClickingPlayer == True and self.gameInProgress == True:
            x, y= event.x, event.y
            self.joueur.setPos(x, y)
    
    def click(self, event):
        # Positionnement de la souris
        x, y = event.x, event.y
        
        # 4 cotes du joueur, [0] = Gauche, [1] = Droite, [2] = Haut et [3] = Bas
        joueurInter = self.joueur.getSpace()
        
        # Trouver si on click dans le carré rouge et demaree le jeu
        if x >= joueurInter[0] and x <= joueurInter[1] and y >= joueurInter[2] and y <= joueurInter[3]:
            self.isClickingPlayer = True             
            self.gameInProgress = True

                
    def unclick(self, event):
        # Si on relache la souris arrete le jeu
        if self.gameInProgress == True:
            self.stopGame()
        
    def pionMovement(self):
        # 4 cotes du joueur, [0] = Gauche, [1] = Droite, [2] = Haut et [3] = Bas
        joueurInter = self.joueur.getSpace()
        
        for i in range(0, len(self.listePions)):
            # 4 cotes du pion, [0] = Gauche, [1] = Droite, [2] = Haut et [3] = Bas
            pionSide = self.listePions[i].getSpace()            
            pionDirection = self.listePions[i].getDirection()
            
            # Validation collision
            if self.gameInProgress == True and \
             ((joueurInter[1] > pionSide[0] and joueurInter[1] < pionSide[1] and joueurInter[3] > pionSide[2] and joueurInter[3] < pionSide[3]) or \
              (joueurInter[0] > pionSide[0] and joueurInter[0] < pionSide[1] and joueurInter[3] > pionSide[2] and joueurInter[3] < pionSide[3]) or \
              (joueurInter[1] > pionSide[0] and joueurInter[1] < pionSide[1] and joueurInter[2] > pionSide[2] and joueurInter[2] < pionSide[3]) or \
              (joueurInter[0] > pionSide[0] and joueurInter[0] < pionSide[1] and joueurInter[2] > pionSide[2] and joueurInter[2] < pionSide[3])) : 
                self.stopGame()
            
            # Changement de direction
            if pionSide[0] <= self.coteGauche or pionSide[1] >= self.coteDroit:
                self.listePions[i].setDirection(180 - pionDirection)
            elif pionSide[2] <= self.coteHaut or pionSide[3] >= self.coteBas:
                self.listePions[i].setDirection(360 - pionDirection)

            # Transformer la direction en direction x et y
            xDir = math.cos(math.radians(self.listePions[i].direction))
            yDir = -math.sin(math.radians(self.listePions[i].direction))

            # Deplacer le pions selon sa vitesse et direction
            if self.gameInProgress == True:
                self.listePions[i].movePos(xDir * self.speed, yDir * self.speed)
                
            # Incrementer la vitesse si progressif
            if self.difficulte == "Progressif":
                self.speed = self.speed + .0005
                
    def stopGame(self):
        # Ajouter le temps au fichier .txt
        self.newSession.appendNewSession(self.timeAlive)
        
        # Mettre a jour la fenetre score
        self.Vue.updateScore(self.newSession.readNewSession())
        
        # Arreter le jeu
        self.gameInProgress = False
        self.isClickingPlayer = False
  
        # Effacer le canvas
        self.aireDeJeu.getCanvas().delete("all")        
        
        # Recommencer le jeu
        self.start()
        
    def setSpeed(self):        
        if self.difficulte == "Facile":
            self.speed = 4
        elif self.difficulte == "Moyen":
            self.speed = 7
        elif self.difficulte == "Difficile":
            self.speed = 10
        elif self.difficulte == "Progressif":
            self.speed = 4
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        