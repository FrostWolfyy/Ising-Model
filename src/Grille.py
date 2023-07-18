import numpy as np
from numpy import random

class Grille:
    def __init__(self, taille):
        self.taille = taille
        self.lattice = np.random.choice([-1,1],size=(taille,taille))

    def energy(self, i,j):
        energy = - self.lattice[i, j] * (self.lattice[i, (j - 1) ] + self.lattice[i, (j + 1) ] + self.lattice[(i - 1) , j] + self.lattice[(i + 1), j])
        return energy
    
    def average_magnetization(self):
        mag = np.sum(self.lattice) / self.taille**2
        return mag
    
    def metropolis(self, temperature, i,j):
        deltaE = -2 * self.energy(i,j)

        if deltaE < 0.0:
            self.lattice[i,j] *= -1
        elif np.random.random() < np.exp( - deltaE / temperature):
            self.lattice[i,j] *= -1

