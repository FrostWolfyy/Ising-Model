import numpy as np
from numpy import random

class Grille:
    def __init__(self, taille):
        self.taille = taille
        self.lattice = np.random.choice([-1,1],size=(taille,taille))

    def energy(i,j):
        size = Grille.shape[0]
        left = Grille[i, (j - 1) ]
        right = Grille[i, (j + 1) ]
        up = Grille[(i - 1) , j]
        down = Grille[(i + 1), j]
        energy = - Grille[i, j] * (left + right + up + down)
        return energy
    
    def average_magnetization(self):
        mag = np.sum(self.lattice) / self.taille
        return mag