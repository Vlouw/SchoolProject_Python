import tkinter as tk
import math
# Permet d'encapsuler une fonction et ses paramètres
from functools import partial, update_wrapper

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getCoordonate(self) :
        return (self.x, self.y)

    def __add__(self, other) :
        if not isinstance(other, Point) :
            raise Exception("Les deux paramètres doivent être des instances de Point")

        return Point(self.x + other.x, self.y + other.y)

    def __mult__(self, a) :
        if not isinstance(a, float) and not isinstance(a, int) :
            raise Exception("Le multiplicateur doit être un entier ou un nombre flottant")

        return Point(self.x * a, self.y * a)

    def __rmult__(self, a) :
        return self.__mult__(a)

    def mult(self, a) :
        return self.__mult__(a)

    def __sub__(self, other) :
        if not isinstance(other, Point) :
            raise Exception("Les deux paramètres doivent être des instances de Point")

        return self.__add__(other.mult(-1))

class Forme:
    def __init__(self, canvas, origine):#, vertex = []) :
        # if vertex == [] :
        #     self.vertex = vertex
        # elif isinstance(vertex, Point) :
        #     self.vertex = [vertex]
        # elif all(isinstance(x, Point) for x in vertex) :
        #     self.vertex = vertex
        # else :
        #     raise Exception("Vous devez fournir un tableau de point")

        if not isinstance(origine, Point) :
            raise Exception("Le paramètre origine doit être de type Point")
        else :
            self.origine = origine

        self.canvas = canvas
        self.result = None

    def clear(self) :
        if self.result is not None :
            self.canvas.delete(self.result)

    def draw(self) :
        raise Exception("Vous ne pouvez pas utiliser la méthode draw de forme. Elle doit être implantée dans un objet hérité.")

    def translate(self, deplacement) :
        if not isinstance(deplacement, Point) :
            raise Exception("Le paramètre deplacement doit être de type Point")

        self.origine += deplacement

    def rotate(self, angle) :
        raise Exception("Vous ne pouvez pas utiliser la méthode rotate de forme. Elle doit être implantée dans un objet hérité.")

    def localRotate(self, delta) :
        raise Exception("Vous ne pouvez pas utiliser la méthode rotate de forme. Elle doit être implantée dans un objet hérité.")

    def resize(self, multiplicateur) :
        raise Exception("Vous ne pouvez pas utiliser la méthode resize de forme. Elle doit être implantée dans un objet hérité.")

class Ligne(Forme) :
    def __init__(self, canvas, origine, distance, angle = 0, fill = 'black') :
        Forme.__init__(self, canvas, origine)

        if not isinstance(distance, int) :
            raise Exception("Le paramètre distance doit être un entier ")
        self.distance = distance
        
        if not isinstance(angle, float) and not isinstance(angle, int) :
            raise Exception("Le paramètre angle doit être un entier ou un nombre flottant")
        self.angle = math.radians(angle)

        self.fill = fill

    def draw(self) :
        self.clear()

        destination = self.origine + Point(math.cos(self.angle), math.sin(self.angle)).mult(self.distance)

        self.result = self.canvas.create_line(self.origine.getCoordonate(), destination.getCoordonate(), fill = self.fill)

        self.canvas.update()

    def rotate(self, angle) :
        if not isinstance(angle, float) and not isinstance(angle, int) :
            raise Exception("Le paramètre angle doit être un entier ou un nombre flottant")

        self.angle = angle

    def localRotate(self, delta) :
        if not isinstance(delta, float) and not isinstance(delta, int) :
            raise Exception("Le paramètre angle doit être un entier ou un nombre flottant")

        self.rotate(self.angle + math.radians(delta))

    def resize(self, multiplicateur) :
        if not isinstance(multiplicateur, float) and not isinstance(multiplicateur, int) :
            raise Exception("Le paramètre multiplicateur doit être un entier ou un nombre flottant")

        if multiplicateur >= 1 :
            self.distance *= multiplicateur
        else :
            self.distance *= (1 - multiplicateur)

class Rectangle(Forme) :
    def __init__(self, canvas, origine, largeur, hauteur, fill = '', outline='black', width=1) :
        Forme.__init__(self, canvas, origine)

        if not isinstance(largeur, int) :
            raise Exception("Le paramètre largeur doit être un entier ")
        self.demiLargeur = largeur / 2

        if not isinstance(hauteur, int) :
            raise Exception("Le paramètre hauteur doit être un entier ")
        self.demihauteur = hauteur / 2

        self.fill = fill
        self.outline = outline
        self.width = width

    def __calculateVectex(self, origine, a, b = 0) :
        x0 = origine.x
        y0 = origine.y

        vertex = []
        vertex.append(Point(x0 - a, y0 - b).getCoordonate())
        vertex.append(Point(x0 + a, y0 - b).getCoordonate())
        vertex.append(Point(x0 + a, y0 + b).getCoordonate())
        vertex.append(Point(x0 - a, y0 + b).getCoordonate())

        return vertex

    def draw(self) :
        self.clear()

        vertex = self.__calculateVectex(self.origine, self.demiLargeur, self.demihauteur)

        self.result = self.canvas.create_polygon(vertex, fill=self.fill, outline=self.outline, width=self.width)

        self.canvas.update()

    def resize(self, multiplicateur) :
        if not isinstance(multiplicateur, float) and not isinstance(multiplicateur, int) :
            raise Exception("Le paramètre multiplicateur doit être un entier ou un nombre flottant")

        if multiplicateur >= 1 :
            self.demiLargeur *= multiplicateur
        else :
            self.demiLargeur *= (1 - multiplicateur)

class Carre(Rectangle) :
    def __init__(self, canvas, origine, largeur, fill = '', outline='black', width=1) :
        Rectangle.__init__(self, canvas, origine, largeur, largeur, fill, outline, width)

class Cercle(Forme) :
    def __init__(self, canvas, origine, rayon, fill = '', outline='black', width=1) :
        Forme.__init__(self, canvas, origine)

        if not isinstance(rayon, int) :
            raise Exception("Le paramètre rayon doit être un entier ")
        self.rayon = rayon

        self.fill = fill
        self.outline = outline
        self.width = width

    def __calculateVectex(self, origine, a) :
        x0 = origine.x
        y0 = origine.y

        vertex = []
        vertex.append(Point(x0 - a, y0 - a).getCoordonate())
        vertex.append(Point(x0 + a, y0 + a).getCoordonate())

        return vertex

    def draw(self) :
        self.clear()

        vertex = self.__calculateVectex(self.origine, self.rayon)

        self.result = self.canvas.create_oval(vertex, fill=self.fill, outline=self.outline, width=self.width)

        self.canvas.update()

    def resize(self, multiplicateur) :
        if not isinstance(multiplicateur, float) and not isinstance(multiplicateur, int) :
            raise Exception("Le paramètre multiplicateur doit être un entier ou un nombre flottant")

        if multiplicateur >= 1 :
            self.rayon *= multiplicateur
        else :
            self.rayon *= (1 - multiplicateur)

class Croix(Forme) :
    def __init__(self, canvas, origine, largeur, fill = 'black', width = 1) :
        Forme.__init__(self, canvas, origine)

        if not isinstance(largeur, float) and not isinstance(largeur, int) :
            raise Exception("Le paramètre largeur doit être un entier ou un nombre flottant")
        self.largeur = largeur

        self.width = width * 2

        self.fill = fill

    def clear(self) :
        if self.result is not None :
            self.canvas.delete(self.result)
            self.canvas.delete(self.result2)

    def draw(self) :
        self.clear()

        # Croix 1
        origine = self.origine - Point(-1, -1).mult(self.largeur / 2)
        destination = self.origine - Point(1, 1).mult(self.largeur / 2)

        self.result = self.canvas.create_line(origine.getCoordonate(), destination.getCoordonate(), fill = self.fill, width = self.width)

        # Croix 2
        origine = self.origine - Point(-1, 1).mult(self.largeur / 2)
        destination = self.origine - Point(1, -1).mult(self.largeur / 2)

        self.result2 = self.canvas.create_line(origine.getCoordonate(), destination.getCoordonate(), fill = self.fill, width = self.width)

        self.canvas.update()

    def rotate(self, angle) :
        if not isinstance(angle, float) and not isinstance(angle, int) :
            raise Exception("Le paramètre angle doit être un entier ou un nombre flottant")

        self.angle = angle

    def localRotate(self, delta) :
        if not isinstance(delta, float) and not isinstance(delta, int) :
            raise Exception("Le paramètre angle doit être un entier ou un nombre flottant")

        self.rotate(self.angle + math.radians(delta))

    def resize(self, multiplicateur) :
        if not isinstance(multiplicateur, float) and not isinstance(multiplicateur, int) :
            raise Exception("Le paramètre multiplicateur doit être un entier ou un nombre flottant")

        if multiplicateur >= 1 :
            self.largeur *= multiplicateur
        else :
            self.largeur *= (1 - multiplicateur)

class AfterEvent:
    """Cette classe permet de définir une action à exécuter
       après un certain temps (par défaut 500 ms).
    """

    def __init__(self, root, callback = lambda : print("Event"), timesleep = 500) :
        self.root = root
        self.function = callback
        self.timesleep = timesleep

    def start(self) :
        self.root.after(self.timesleep, AfterEvent.prepareCallback(AfterEvent.__loop, self, self.function))

    def startImmediately(self) :
        AfterEvent.__loop(self, self.function)

    @staticmethod
    def __loop(afterevent, callback) :
        callback()
        afterevent.start()

    @staticmethod
    def prepareCallback(func, *args, **kwargs):
        partial_func = partial(func, *args, **kwargs)
        update_wrapper(partial_func, func)
        return partial_func
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    