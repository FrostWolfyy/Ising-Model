from src.Grille import Grille
from src.Ising import Ising
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# # Variables
# size = 8
# iterations = 10000
# kb = 1
# t = 0.05
# beta = kb * t
# J = 1

# np.random.seed(24032003)

# system = Grille(size)
# test = Ising(system, iterations, beta, J)

# allMag, allEnergy, grid = test.runAnim()

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


# Variables
size = 16
iterations = 10000
kb = 0.1
t = 0.05
J = 1

# Evolution of Magnetization Script

mag=[]
betaList = []
for i in range (1,120):
    beta = kb * t
    print(i)
    beta *= i
    np.random.seed(24032003)
    system = Grille(size)
    test = Ising(system, iterations, beta, J)
    betaList.append(beta)
    mag.append(test.runMag())

plt.figure()
plt.plot(betaList, mag, linestyle= "None", marker=".")
plt.savefig("out/Mag_Temp.pdf")


# # Graphs


# ###########################

# plt.figure(figsize=(10, 4))

# plt.subplot(1, 2, 1)
# plt.plot(mag)
# plt.xlabel('Iteration')
# plt.ylabel('Magnetization')
# plt.title('2D Ising Model - Magnetization')

# plt.subplot(1, 2, 2)
# plt.plot(en)
# plt.xlabel('Iteration')
# plt.ylabel('Energy')
# plt.title('2D Ising Model - Energy')

# plt.tight_layout()
# plt.savefig("out/Mag_En_Iterations.pdf")

# #############################

