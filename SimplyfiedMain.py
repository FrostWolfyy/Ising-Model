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
def magnetization(lattice, size):
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
        mag = magnetization(lattice, size)
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
        mag = magnetization(lattice, size)
        Energy = 0 

        for j in range (0, size):
            for k in range (0, size):
                Energy += energy(lattice, j,k, size, J) / 2
        
        metropolis(lattice, beta, size, J)
    return magnetization(lattice, size)

def runAll(size, TempNumber, initialT):
    allT = np.array()
    allMag = np.array()
    for i in range(TempNumber):
        np.append(allT, initialT * (i + 1))

        GrilleUp = np.ones((size,size))
        GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
        tempMagUp = np.zeros(1)

        tempMagRandom = np.zeros(1)
        while():  
            metropolis(GrilleUp, beta, size, J)
            metropolis(GrilleRandom, beta, size, J)

        np.append(allMag, np.mean(magnetization(GrilleUp, size), magnetization(GrilleRandom, size)))
    return allT, allMag

# Variables
size = 64
iterations = 100000
kb = 1
Temp = 5
J = 1
beta = kb * Temp

# Equilibrium Arrival After T MTC

# count = 0
# GrilleUp = np.ones((size,size))
# GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
# magUp = [magnetization(GrilleUp, size)]
# magRandom = [magnetization(GrilleRandom, size)]
# t_MTC = [count / size**2]
# while (np.abs(magUp[count] - magRandom[count]) > 0.0001):
    
#     metropolis(GrilleUp, beta, size, J)
#     metropolis(GrilleRandom, beta, size, J)
#     count += 1
#     magUp.append(magnetization(GrilleUp, size))
#     magRandom.append(magnetization(GrilleRandom, size))
#     t_MTC.append(count / size**2)

# plt.figure()
# plt.plot(t_MTC, magUp, linestyle="None", marker=".", color = "black")
# plt.plot(t_MTC, magRandom, linestyle="None", marker=".", color = "black")
# plt.xlabel("t_MTC")
# plt.ylabel("Magnetization")
# plt.savefig("out/Mag.pdf")


count = 0
GrilleUp = np.ones((size,size))
GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
magUp = [magnetization(GrilleUp, size)]
magRandom = [magnetization(GrilleRandom, size)]
t_MTC = [count / size**2]
for i in range(iterations):
    print(i)
    metropolis(GrilleUp, beta, size, J)
    metropolis(GrilleRandom, beta, size, J)
    magUp.append(magnetization(GrilleUp, size))
    magRandom.append(magnetization(GrilleRandom, size))
    t_MTC.append(i / size**2)

plt.figure()
plt.plot(t_MTC, magUp, linestyle="None", marker=".", color = "blue")
plt.plot(t_MTC, magRandom, linestyle="None", marker=".", color = "black")
plt.xlabel("t_MTC")
plt.xscale("log")
plt.ylabel("Magnetization")
plt.savefig("out/Mag1.pdf")

# Evolution of Magnetization Script

# mag5= np.zeros(150)
# betaList = np.zeros(150)

# for i in range (1,151):
#     print(i)
#     beta = kb * Temp
#     beta *= i
#     np.random.seed(24032003)
#     grille = np.random.choice(np.array([-1, 1]), size=(size, size))
#     betaList[i-1] = beta
#     mag5[i-1] = runMag(grille, iterations, size, beta, J)
# print(betaList)

# plt.figure()
# plt.plot(betaList, mag5, linestyle="None", marker=".", color = "black")
# plt.xlabel("Temperature")
# plt.ylabel("Magnetization")
# plt.savefig("out/Mag_Temp.pdf")

# Variables

# size = 8
# iterations = 1000
# kb = 1
# t = 0.05
# J = 1
# beta = kb * t

# # Initialize Lattice

# grille = np.random.choice(np.array([-1, 1]), size=(size, size))

# allMag, allEnergy, grid = runAnim(grille, iterations, size, beta, J)

# # Animation Script


# fig, ax = plt.subplots()

# # Initialize the image plot
# image = ax.imshow(grid[0], cmap='binary')

# # Update function for each frame

# def update(frame):
#     image.set_array(grid[frame])
#     return image,

# # Create the animation
# ani = animation.FuncAnimation(fig, update, frames=len(grid), interval=1)

# # Save the animation as a GIF
# ani.save('out/animation.gif', writer='pillow')

# print("Terminé")