# -*- coding: utf8 -*-

# -------------------------------------------------------------
# Auteur  : Henri-Paul Bolduc
#           Elisabeth Fortin
#           Nelson Peralta Matute
# Cours   : 420-C31-IN - GENIE LOGICIEL I : CONCEPTION ET GESTION
# TP 2    : Jeu Carre Rouge
# Fichier : modeles.py
# -------------------------------------------------------------

import tkinter as tk
from c31Geometry import *

class Joueur:
    def __init__ (self, canvas, x, y, size):
        self.size = size
        
        self.xPos = x
        self.yPos = y
        
        self.forme = Rectangle(canvas, Point(x, y), size, size, 'red')
        self.forme.draw()
        
    def getSpace(self):        
        return self.xPos - (self.size / 2), self.xPos + (self.size / 2), self.yPos - (self.size / 2), self.yPos + (self.size / 2)
        
    def setPos(self, x, y):
        self.xPos = x
        self.yPos = y
        self.forme.origine = Point(x,y)
        self.forme.draw()
        
    def getXPos(self):
        return self.xPos
    
    def getYPos(self):
        return self.yPos
    
    def getSize(self):
        return self.size
    
    def getForme(self):
        return self.forme

class Pion:
    def __init__ (self, canvas, x, y, largeur, hauteur, direction):            
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
    
        self.direction = direction
        
        self.xPos = x
        self.yPos = y
        
        self.forme = Rectangle(canvas, Point(x, y), largeur, hauteur, 'blue')
        self.forme.draw()
        
    def getSpace(self):        
        return self.xPos - (self.largeur / 2), self.xPos + (self.largeur / 2), self.yPos - (self.hauteur / 2), self.yPos + (self.hauteur / 2)
    
    def movePos(self, x, y):        
        self.xPos = self.xPos + x
        self.yPos = self.yPos + y
        self.forme.translate(Point(x,y))
        self.forme.draw()
    
    def setPos(self, x, y):        
        self.xPos = x
        self.yPos = y
        self.forme.translate(Point(x,y))
        self.forme.draw()    
    
    def getXPos(self):
        return self.xPos
    
    def getYPos(self):
        return self.yPos
    
    def setDirection(self, direction):
        self.direction = direction
        
    def getDirection(self):
        return self.direction
    
    def getForme(self):
        return self.forme

        
class AireDeJeu:
    def __init__ (self, parent):
        self.tailleCanvas = 450
        self.canvasBordure = 50 # Largeur de la bordure 
        
        self.canvas = tk.Canvas(parent, background='white', height=self.tailleCanvas, width=self.tailleCanvas, highlightthickness=self.canvasBordure, highlightbackground="black")
        self.canvas.pack(expand = 'false')
        
    def getTailleCanvas(self):
        return self.tailleCanvas
    
    def getCanvas(self):
        return self.canvas
    
    def getCanvasBordure(self):
        return self.canvasBordure