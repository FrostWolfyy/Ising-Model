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
def susceptibility(magnetizations, beta, size):
     return size * ( np.mean(magnetizations**2) - np.mean(magnetizations)**2 ) / beta

# Animate the evolution of spin over time, Working Good.


@njit
def cumulant(magnetizations):
     return 1 - ( np.mean(magnetizations**4) / (3 * (np.mean(magnetizations**2))**2) )
 
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
def runAll(size, Temp, J, kb):

    allT = np.empty(len(Temp))
    allMag = np.empty(len(Temp))
    allKhi = np.empty(len(Temp))

    for i in range(len(Temp)):
        allT[i] = Temp[i]
        beta = Temp[i] * kb
        print(i)
        np.random.seed(24032003)
        GrilleUp = np.ones((size, size))
        GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))

        tempMagUp = np.empty(0)
        tempMagRandom = np.empty(0)

        tempMagUp = np.append(tempMagUp, magnetization(GrilleUp, size))
        tempMagRandom = np.append(tempMagRandom, magnetization(GrilleRandom, size))
        iterations = 0
        while np.abs(np.mean(tempMagRandom[-10000:]) - np.mean(tempMagUp[-10000:])) > 0.000001:
            iterations += 1
            if iterations >= 1000000:
                print("Maximum iterations reached. Exiting loop.")
                
                break
            metropolis(GrilleUp, beta, size, J)
            metropolis(GrilleRandom, beta, size, J)
            tempMagUp = np.append(tempMagUp, magnetization(GrilleUp, size))
            tempMagRandom = np.append(tempMagRandom, magnetization(GrilleRandom, size))

        meanMag = (np.mean(tempMagRandom[-10000:]) + np.mean(tempMagUp[-10000:]) ) / 2
        allMag[i] = meanMag
        allKhi[i] = susceptibility( tempMagUp, beta, size)

    return allT, allMag, allKhi



# Test Susceptibility 

iterations = 5000000
kb = 1
Temp = np.array([1.80, 1.90, 2.0, 2.05, 2.10, 2.15, 2.20, 2.225, 2.25, 2.275, 2.30, 2.325, 2.35, 2.375, 2.40, 2.45, 2.50, 2.55, 2.60, 2.70, 2.80, 2.90, 3.00])
J = 1
beta = Temp * kb

Chi5 = np.zeros(len(Temp))
Chi10 = np.zeros(len(Temp))
Chi20 = np.zeros(len(Temp))
Chi30 = np.zeros(len(Temp))

size = 5

for i in range(1,len(Temp)):

    allMag = np.zeros(iterations)
    print(i)

    np.random.seed(24032003)
    grille = np.ones((size, size))

    for j in range(iterations):
        allMag[j] = magnetization(grille,size)
        metropolis(grille, beta[i-1], size, J)

    Chi5[i-1] = susceptibility(allMag, beta[i-1], size)

size = 10

for i in range(1,len(Temp)):

    allMag = np.zeros(iterations)
    print(i)

    np.random.seed(24032003)
    grille = np.ones((size, size))

    for j in range(iterations):
        allMag[j] = magnetization(grille,size)
        metropolis(grille, beta[i-1], size, J)

    Chi10[i-1] = susceptibility(allMag, beta[i-1], size)

size = 20

for i in range(1,len(Temp)):

    allMag = np.zeros(iterations)
    print(i)

    np.random.seed(24032003)
    grille = np.ones((size, size))

    for j in range(iterations):
        allMag[j] = magnetization(grille,size)
        metropolis(grille, beta[i-1], size, J)

    Chi20[i-1] = susceptibility(allMag, beta[i-1], size)

size = 30

for i in range(1,len(Temp)):

    allMag = np.zeros(iterations)
    print(i)

    np.random.seed(24032003)
    grille = np.ones((size, size))

    for j in range(iterations):
        allMag[j] = magnetization(grille,size)
        metropolis(grille, beta[i-1], size, J)

    Chi30[i-1] = susceptibility(allMag, beta[i-1], size)

plt.figure()
plt.plot(Temp / 2.27, Chi5, linestyle = "None", marker=".", color = "black", label = "$N = 5$" ) 
plt.plot(Temp / 2.27, Chi10, linestyle = "None", marker="x", color = "blue", label = "$N = 10$") 
plt.plot(Temp / 2.27, Chi20, linestyle = "None", marker="+", color = "green", label = "$N = 20$") 
plt.plot(Temp / 2.27, Chi30, linestyle = "None", marker="*", color = "red", label = "$N = 30$") 
plt.legend()
plt.xlabel("$T / T_C $")
plt.ylabel("$ \chi $")
plt.savefig("out/KhiTest.pdf")

# Critical Temp UL

# iterations = 2000000
# kb = 1
# Temp = np.array([2.15, 2.20, 2.25, 2.275, 2.30, 2.325])
# J = 1
# beta = Temp * kb

# size = 50

# UL50 = np.zeros(len(Temp))
# UL10 = np.zeros(len(Temp))
# UL8 = np.zeros(len(Temp))
# UL20 = np.zeros(len(Temp))

# for i in range(1,len(Temp) + 1):

#     allMag = np.zeros(iterations)
#     print(i)

#     #np.random.seed(24032003)
#     grille = np.ones((size, size))
#     #grille = np.random.choice(np.array([-1, 1]), size=(size, size))
#     for j in range(iterations):
#         allMag[j] = magnetization(grille,size)
#         metropolis(grille, beta[i-1], size, J)

#     UL50[i-1] = cumulant(allMag)


# size = 10
# for i in range(1,len(Temp)+1):

#     allMag = np.zeros(iterations)
#     print(i)

#     #np.random.seed(24032003)
#     grille = np.ones((size, size))
#     #grille = np.random.choice(np.array([-1, 1]), size=(size, size))
#     for j in range(iterations):
#         allMag[j] = magnetization(grille,size)
#         metropolis(grille, beta[i-1], size, J)

#     UL10[i-1] = cumulant(allMag)

# size = 8
# for i in range(1,len(Temp)+1):

#     allMag = np.zeros(iterations)
#     print(i)

#     #np.random.seed(24032003)
#     grille = np.ones((size, size))
#     #grille = np.random.choice(np.array([-1, 1]), size=(size, size))
#     for j in range(iterations):
#         allMag[j] = magnetization(grille,size)
#         metropolis(grille, beta[i-1], size, J)

#     UL8[i-1] = cumulant(allMag)

# size = 20
# for i in range(1,len(Temp) +1):

#     allMag = np.zeros(iterations)
#     print(i)

#     #np.random.seed(24032003)
#     grille = np.ones((size, size))
#     #grille = np.random.choice(np.array([-1, 1]), size=(size, size))
#     for j in range(iterations):
#         allMag[j] = magnetization(grille,size)
#         metropolis(grille, beta[i-1], size, J)

#     UL20[i-1] = cumulant(allMag)


# Diff = 1
# for i in range (len(Temp)):
#     if ( np.abs((1 - (UL50[i] / UL10[i]))) < Diff):
#         TC = Temp[i]
# print(TC)

# plt.figure()
# plt.plot(Temp, UL50 / UL10, marker="+", color = "black")
# plt.plot(Temp, UL8 / UL20, marker="x", color = "blue")
# plt.xlabel("Temperature")
# plt.ylabel("UL")
# plt.savefig("out/UTest.pdf")

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
# iterations = 20000000
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
# plt.savefig("out/Mag_Temp.pdf")
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Variables

kb = 1
Temp = np.array([1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.0, 2.05, 2.10, 2.15, 2.20, 2.25, 2.30, 2.35, 2.40, 2.45, 2.50, 2.55, 2.60, 2.70, 2.80, 2.90, 3.00, 3.10, 3.20 ])
J = 1
beta = kb * Temp

size = 5
allT10, allMag10, allKhi10 = runAll(size, Temp, J, kb)

size = 10
allT20, allMag20, allKhi20 = runAll(size, Temp, J, kb)

size = 20
allT30, allMag30, allKhi30 = runAll(size, Temp, J, kb)

size = 30
allT40, allMag40, allKhi40 = runAll(size, Temp, J, kb)

plt.figure()
plt.plot(allT10 / 2.27, allMag10, linestyle="None", marker=".", color = "black", label= "$N = 5$" )
plt.plot(allT20 / 2.27, allMag20, linestyle="None", marker="x", color = "blue", label= "$N = 10$")
plt.plot(allT30 / 2.27, allMag30, linestyle="None", marker="+", color = "green", label= "$N = 20$")
plt.plot(allT40 / 2.27, allMag40, linestyle="None", marker="*", color = "red", label= "$N = 30$")
plt.legend()
plt.xlabel("$T / T_C$")
plt.ylabel("$ M $")
plt.savefig("out/MagAll.pdf")


plt.figure()
plt.plot(allT10 / 2.27, allKhi10, linestyle="None", marker="o", color = "black", label= "$N = 5$" )
plt.plot(allT20 / 2.27, allKhi20, linestyle="None", marker="^", color = "blue", label= "$N = 10$")
plt.plot(allT30 / 2.27, allKhi30, linestyle="None", marker="*", color = "green", label= "$N = 20$")
plt.plot(allT40 / 2.27, allKhi40, linestyle="None", marker="s", color = "red", label= "$N = 30$")
plt.legend()
plt.xlabel("$T / T_C")
plt.ylabel("$ \chi$")
plt.savefig("out/KhiAll.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 # Equilibrium Arrival After T MTC

# size = 32
# iterations = 1000000
# kb = 1
# Temp = 3
# J = 1
# beta = kb * Temp

# np.random.seed(24032003)

# count = 0
# GrilleUp = np.ones((size,size))
# GrilleRandom = np.random.choice(np.array([-1, 1]), size=(size, size))
# magUp = [magnetization(GrilleUp, size)]
# magRandom = [magnetization(GrilleRandom, size)]
# t_MTC = [count]

# magUpGraph = [magnetization(GrilleUp, size)]
# magRandomGraph = [magnetization(GrilleRandom, size)]

# while (np.abs(np.mean(magUp[-50000:]) - np.mean(magRandom[-50000:]))) > 0.000001:
#     print(np.abs(magUp[count] - magRandom[count]))
#     metropolis(GrilleUp, beta, size, J)
#     metropolis(GrilleRandom, beta, size, J)
#     count += 1
#     magUp.append(magnetization(GrilleUp, size))
#     magRandom.append(magnetization(GrilleRandom, size))
#     if ((count % 2000) == 0 ):
#         t_MTC.append(count)
#         magUpGraph.append(np.mean(magUp[-10000:]))
#         magRandomGraph.append(np.mean(magRandom[-10000:]))

# plt.figure()
# plt.plot(t_MTC, magUpGraph, marker="None", color = "blue")
# plt.plot(t_MTC, magRandomGraph, marker="None", color = "black")
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

#     if ((i % 20000) == 0 ):
#         t_MTC.append(i)
#         magUp.append(magnetization(GrilleUp, size))
#         magRandom.append(magnetization(GrilleRandom, size))
# plt.figure()
# plt.plot(t_MTC, magUp, marker="None", color = "blue")
# plt.plot(t_MTC, magRandom, marker="None", color = "black")
# plt.xlabel("Monte Carlo Step")
# # plt.xscale("log")
# plt.ylabel("Magnetization")
# plt.savefig("out/Mag1.pdf")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

