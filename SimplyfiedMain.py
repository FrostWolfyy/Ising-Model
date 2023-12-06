import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import numba

def energy(lattice, i, j, size, J):

    #                               LEFT                         RIGHT                        UP                           DOWN
    energy = - J * lattice[i, j] * (lattice[i, (j - 1) % size] + lattice[i, (j + 1) % size] + lattice[(i - 1) % size, j] + lattice[(i + 1) % size, j])

    return energy

def metropolis(lattice, beta, size, J):

        i = np.random.randint(0, size)
        j = np.random.randint(0, size)

        deltaE = -2 * energy(lattice, i, j, size, J)

        # Change the value of the spin as a function of the energy difference
        if deltaE < 0.0:
            lattice[i,j] *= -1
        elif np.random.random() < np.exp( - deltaE / beta):
            lattice[i,j] *= -1

def average_magnetization(lattice, size):
    mag = np.sum(lattice) / size**2 # Taille ** 2 = Number of spins
    return mag

def runAnim(lattice, iterations, size, J, beta):
        allMag = []
        allEnergy = []
        allGrid = []
        for i in range (iterations):
            mag = average_magnetization(lattice, size)
            energy = 0 

            for j in range (0, size):
                for k in range (0, size):
                    energy += energy(lattice, j, k, size, J) / 2
        
            allMag.append(mag)
            allEnergy.append(energy)
            metropolis(lattice, beta, size, J)
            allGrid.append(lattice.copy())
         
        return allMag, allEnergy, allGrid
    
def runMag(lattice, iterations, size, beta, J):
    for i in range (iterations):
        mag = average_magnetization(lattice, size)
        energy = 0 

        for j in range (0, size):
            for k in range (0, size):
                energy += energy(lattice, j,k, size, J) / 2
        
        metropolis(lattice, beta, J)
    return average_magnetization(lattice, size)