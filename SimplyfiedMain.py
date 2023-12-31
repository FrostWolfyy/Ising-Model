import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from numba import njit

# Calculte Energy of site (i,j) Working Good.
@njit
def energy(lattice, i, j, size, J):

    #                               LEFT                         RIGHT                        UP                           DOWN
    energy = - J * lattice[i, j] * (lattice[i, (j - 1) % size] + lattice[i, (j + 1) % size] + lattice[(i - 1) % size, j] + lattice[(i + 1) % size, j])

    return energy

# Monte Carlo Step, Working Good.

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

# Calculate the magnetization of a given spin grid, Working Good

@njit
def magnetization(lattice, size):
    mag = np.sum(lattice) / size**2 # Taille ** 2 = Number of spins
    return np.abs(mag)

# Calculate the magnetic susceptibility for a given evolution of magnetization over time, Working Good.

@njit
def susceptibility(magnetizations, beta):
     return ( np.mean(magnetizations**2) - np.mean(magnetizations)**2 ) / beta

# Animate the evolution of spin over time, Working Good.

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

# Calculate the magnetization after a certain number of MTC Step, Working Good.
@njit
def runMag(lattice, iterations, size, beta, J):
    for i in range (iterations):
        metropolis(lattice, beta, size, J)
    return magnetization(lattice, size)

@njit
def runAll(size, TempNumber, initialT, J, kb):

    allT = np.empty(TempNumber)
    allMag = np.empty(TempNumber)
    allKhi = np.empty(TempNumber)

    for i in range(TempNumber):
        allT[i] = initialT - (i * 0.03)
        beta = (initialT - (i * 0.03)) * kb
        print(i)
        np.random.seed(24032003)
        GrilleUp = np.ones((size, size))
        GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))

        tempMagUp = np.empty(0)
        tempMagRandom = np.empty(0)

        tempMagUp = np.append(tempMagUp, magnetization(GrilleUp, size))
        tempMagRandom = np.append(tempMagRandom, magnetization(GrilleRandom, size))

        iterations = 0
        while np.abs(np.mean(tempMagRandom[-1000:]) - np.mean(tempMagUp[-1000:])) > 0.001:
            if iterations >= 100000:
                print("Maximum iterations reached. Exiting loop.")
                break

            metropolis(GrilleUp, beta, size, J)
            metropolis(GrilleRandom, beta, size, J)
            tempMagUp = np.append(tempMagUp, magnetization(GrilleUp, size))
            tempMagRandom = np.append(tempMagRandom, magnetization(GrilleRandom, size))

        meanMag = (magnetization(GrilleUp, size) + magnetization(GrilleRandom, size)) / 2
        allMag[i] = meanMag
        allKhi[i] = susceptibility(tempMagUp, beta)

    return allT, allMag, allKhi

# Animation of spin changing direction over time

# Variables

# size = 8
# iterations = 1000
# kb = 1
# t = 0.05
# J = 1
# beta = kb * t

# np.random.seed(24032003)

# # Initialize Lattice
# grille = np.random.choice(np.array([-1, 1]), size=(size, size))
# allMag, allEnergy, grid = runAnim(grille, iterations, size, J, beta)

# # Animation Script

# fig, ax = plt.subplots()

# # Initialize the image plot
# image = ax.imshow(grid[0], cmap='binary')

# # Update function for each frame

# def update(frame):
#     image.set_array(grid[frame])
#     return image,

# # Create the animation
# ani = animation.FuncAnimation(fig, update, frames=len(grid), interval=0.1)

# # Save the animation as a GIF
# ani.save('out/animation.gif', writer='pillow')

# print("Terminé")


# Evolution of Magnetization Script

# Variables

# size = 32
# iterations = 100000
# kb = 1
# Temp = 0.05
# J = 1

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
# plt.savefig("out/Mag_Temp3.pdf")

# Test Susceptibility 

# size = 32
# iterations = 1000000
# kb = 1
# Temp = 0.05
# J = 1

# Chi = np.zeros(150)
# betaList = np.zeros(150)
# for i in range(1,151):

#     allMag = np.zeros(iterations)

#     print(i)
#     beta = kb * Temp
#     beta *= i

#     np.random.seed(24032003)
#     grille = np.ones((size, size))

#     for j in range(iterations):
#         allMag[j] = magnetization(grille,size)
#         metropolis(grille, beta, size, J)

#     betaList[i-1] = beta
#     Chi[i-1] = susceptibility(allMag, beta)

# plt.figure()
# plt.plot(betaList, Chi, linestyle="None", marker=".", color = "black")
# plt.xlabel("Temperature")
# plt.ylabel("Susceptibility")
# plt.savefig("out/KhiTest.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Variables
# size = 16
# iterations = 106
# kb = 1
# Temp = 4
# J = 1
# beta = kb * Temp

# allT, allMag, allKhi = runAll(size, iterations, Temp, J, kb)

# plt.figure()
# plt.plot(allT, allMag, linestyle="None", marker=".", color = "black")
# plt.xlabel("Temperzture")
# plt.ylabel("Magnetization")
# plt.savefig("out/MagAll.pdf")

# plt.figure()
# plt.plot(allT, allKhi, linestyle="None", marker=".", color = "black")
# plt.xlabel("Temperzture")
# plt.ylabel("Susceptibility")
# plt.savefig("out/Khi.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 # Equilibrium Arrival After T MTC

# count = 0
# GrilleUp = np.ones((size,size))
# GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
# magUp = [magnetization(GrilleUp, size)]
# magRandom = [magnetization(GrilleRandom, size)]
# t_MTC = [count / size**2]
# while (np.abs(magUp[count] - magRandom[count]) > 0.01):
#     print(np.abs(magUp[count] - magRandom[count]))
#     metropolis(GrilleUp, beta, size, J)
#     metropolis(GrilleRandom, beta, size, J)
#     count += 1
#     magUp.append(magnetization(GrilleUp, size))
#     magRandom.append(magnetization(GrilleRandom, size))
#     t_MTC.append(count / size**2)

# plt.figure()
# plt.plot(t_MTC, magUp, linestyle="None", marker=".", color = "blue")
# plt.plot(t_MTC, magRandom, linestyle="None", marker=".", color = "black")
# plt.xlabel("t_MTC")
# plt.ylabel("Magnetization")
# plt.savefig("out/Mag.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# count = 0
# GrilleUp = np.ones((size,size))
# GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
# magUp = [magnetization(GrilleUp, size)]
# magRandom = [magnetization(GrilleRandom, size)]
# t_MTC = [count / size**2]
# for i in range(iterations):
#     print(i)
#     metropolis(GrilleUp, beta, size, J)
#     metropolis(GrilleRandom, beta, size, J)
#     magUp.append(magnetization(GrilleUp, size))
#     magRandom.append(magnetization(GrilleRandom, size))
#     t_MTC.append(i / size**2)

# plt.figure()
# plt.plot(t_MTC[90000,99999], magUp[90000,99999], linestyle="None", marker=".", color = "blue")
# plt.plot(t_MTC[90000,99999], magRandom[90000,99999], linestyle="None", marker=".", color = "black")
# plt.xlabel("t_MTC")
# plt.xscale("log")
# plt.ylabel("Magnetization")
# plt.savefig("out/Mag1.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%