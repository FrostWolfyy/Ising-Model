from src.Grille import Grille
from src.Ising import Ising

system = Grille(16)

test = Ising(system,100, 0.01)

mag,en = test.run()

print(mag)
print("          ")
print(en)