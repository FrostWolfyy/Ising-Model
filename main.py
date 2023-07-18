from src.Grille import Grille
from src.Ising import Ising
import matplotlib.pyplot as plt

system = Grille(10)

test = Ising(system,10000, 0.001)

mag,en = test.run()

#
# Graphs
#

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(mag)
plt.xlabel('Iteration')
plt.ylabel('Magnetization')
plt.title('2D Ising Model - Magnetization')

plt.subplot(1, 2, 2)
plt.plot(en)
plt.xlabel('Iteration')
plt.ylabel('Energy')
plt.title('2D Ising Model - Energy')

plt.tight_layout()
plt.savefig("out/Mag_En_Iterations.pdf")