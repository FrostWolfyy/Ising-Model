import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from numba import njit

@njit
def energy(lattice, i, j, size, J):

    #                               LEFT                         RIGHT                        UP                           DOWN
    energy = - J * lattice[i, j] * (lattice[i, (j - 1) % size] + lattice[i, (j + 1) % size] + lattice[(i - 1) % size, j] + lattice[(i + 1) % size, j])

    return energy

@njit
def metropolis(lattice, beta, size, J):

        i = np.random.randint(0, size)
        j = np.random.randint(0, size)

        deltaE = -2 * energy(lattice, i, j, size, J)

        # Change the value of the spin as a function of the energy difference
        if deltaE < 0.0:
            lattice[i,j] *= -1
        elif np.random.random() < np.exp( - deltaE / beta):
            lattice[i,j] *= -1

@njit
def average_magnetization(lattice, size):
    mag = np.sum(lattice) / size**2 # Taille ** 2 = Number of spins
    return np.abs(mag)

@njit
def susceptibility(magnetizations, beta):
     return ( np.mean(magnetizations**2) - np.mean(magnetizations)**2 ) / beta

@njit

def runAnim(lattice, iterations, size, J, beta):
        
        allMag = np.zeros(iterations)
        allEnergy = np.zeros(iterations)
        allGrid = np.zeros((iterations, size, size))

        for i in range (iterations):
            mag = average_magnetization(lattice, size)
            Energy = 0 

            for j in range (0, size):
                for k in range (0, size):
                    Energy += energy(lattice, j, k, size, J) / 2
        
            allMag[i] = mag
            allEnergy[i] = Energy
            allGrid[i] = lattice.copy()

            metropolis(lattice, beta, size, J)
         
        return allMag, allEnergy, allGrid
    
@njit
def runMag(lattice, iterations, size, beta, J):
    for i in range (iterations):
        mag = average_magnetization(lattice, size)
        energy = 0 

        for j in range (0, size):
            for k in range (0, size):
                energy += energy(lattice, j,k, size, J) / 2
        
        metropolis(lattice, beta, J)
    return average_magnetization(lattice, size)

# Variables

size = 8
iterations = 1000
kb = 1
t = 0.05
J = 1
beta = kb * t

# Initialize Lattice

grille = np.random.choice(np.array([-1, 1]), size=(size, size))

allMag, allEnergy, grid = runAnim(grille, iterations, size, beta, J)

# Animation Script


fig, ax = plt.subplots()

# Initialize the image plot
image = ax.imshow(grid[0], cmap='binary')

# Update function for each frame

def update(frame):
    image.set_array(grid[frame])
    return image,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(grid), interval=1)

# Save the animation as a GIF
ani.save('out/animation.gif', writer='pillow')

print("Terminé")