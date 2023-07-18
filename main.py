from src.Grille import Grille
from src.Ising import Ising

system = Grille(4)

test = Ising(system,100, 1)

mag,en = test.run()

print(mag)
print("          ")
print(en)