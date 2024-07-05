# -*- coding: utf8 -*-

# -------------------------------------------------------------
# Auteur  : Henri-Paul Bolduc
#           Elisabeth Fortin
#           Nelson Peralta Matute
# Cours   : 420-C31-IN - GENIE LOGICIEL I : CONCEPTION ET GESTION
# TP 2    : Jeu Carre Rouge
# Fichier : jeu.py
# -------------------------------------------------------------

import tkinter as tk
from vues import FenetrePrincipale
from controlleurs import MainMenuController
# -------------------------------------------------------------

# Boucle de jeu
if __name__ == "__main__" :
    # Initialisation de root et de la fenetre initiale
    root = tk.Tk()
    FenetrePrincipale.show(root)

    # Ouvrir le controlleur
    MainMenuController(root)

    # Lance la boucle principale
    root.mainloop()