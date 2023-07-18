from src.Grille import Grille 

class Ising():
    def __init__(self, Grille, iterations, temperature):
        self.Grille = Grille 
        self.iterations = iterations
        self.temperature = temperature

    def run(self):
        allMag = []
        allEnergy = []
        allGrid = []
        for i in range (self.iterations):
            mag = self.Grille.average_magnetization()
            energy = 0 

            for j in range (0, self.Grille.taille):
                for k in range (0, self.Grille.taille):
                    energy += self.Grille.energy(j,k) / 2
        
            allMag.append(mag)
            allEnergy.append(energy)
            self.Grille.metropolis(self.temperature)
            allGrid.append(self.Grille.lattice.copy())
         
        return allMag, allEnergy, allGrid