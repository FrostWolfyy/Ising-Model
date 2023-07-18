import numpy as np
from numpy import random

class Grille:
    def __init__(self, taille):
        self.taille = taille
        self.lattice = np.random.choice([-1,1],size=(taille,taille))

    def energy(i,j):
        energy = - Grille[i, j] * (Grille[i, (j - 1) ] + Grille[i, (j + 1) ] + Grille[(i - 1) , j] + Grille[(i + 1), j])
        return energy
    
    def average_magnetization(self):
        mag = np.sum(self.lattice) / self.taille
        return mag