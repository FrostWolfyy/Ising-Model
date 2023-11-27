import numpy as np
from numpy import random

class Grille:

    # Initialising the grid
    def __init__(self, taille):
        self.taille = taille
        self.lattice = np.random.choice([-1,1],size=(taille,taille))

    # Energy of 1 spin
    def energy(self, i,j, J): # J = Coupling Constant
        size = self.lattice.shape[0]
        energy = - J * self.lattice[i, j] * (self.lattice[i, (j - 1) % size] + self.lattice[i, (j + 1)% size ] + self.lattice[(i - 1) % size, j] + self.lattice[(i + 1) % size, j])
        return energy
    
    # Average magnetization computation
    def average_magnetization(self):
        mag = np.sum(self.lattice) / self.taille**2 # Taille ** 2 = Number of spins
        return mag
    
    # Running algorithm --> Swap 1 random spin
    def metropolis(self, beta, J):

        i = np.random.randint(0,self.taille)
        j = np.random.randint(0,self.taille)

        deltaE = -2 * J * self.energy(i,j)

        # Change the value of the spin as a function of the energy difference
        if deltaE < 0.0:
            self.lattice[i,j] *= -1
        elif np.random.random() < np.exp( - deltaE / beta):
            self.lattice[i,j] *= -1

