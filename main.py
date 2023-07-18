from src.Grille import Grille

system = Grille(4)
print(system.lattice)
print(system.average_magnetization())

system.metropolis(1, 0, 0)

print(system.lattice)
print(system.average_magnetization())