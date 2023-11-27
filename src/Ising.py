from src.Grille import Grille 

class Ising():
    def __init__(self, Grille, iterations, beta, J):
        self.Grille = Grille 
        self.iterations = iterations
        self.beta = beta
        self.J = J

    def runAnim(self):
        allMag = []
        allEnergy = []
        allGrid = []
        for i in range (self.iterations):
            mag = self.Grille.average_magnetization()
            energy = 0 

            for j in range (0, self.Grille.taille):
                for k in range (0, self.Grille.taille):
                    energy += self.Grille.energy(j,k,self.J) / 2
        
            allMag.append(mag)
            allEnergy.append(energy)
            self.Grille.metropolis(self.beta, self.J)
            allGrid.append(self.Grille.lattice.copy())
         
        return allMag, allEnergy, allGrid
    
    def runMag(self):
        for i in range (self.iterations):
            mag = self.Grille.average_magnetization()
            energy = 0 

            for j in range (0, self.Grille.taille):
                for k in range (0, self.Grille.taille):
                    energy += self.Grille.energy(j,k, self.J) / 2
        
            self.Grille.metropolis(self.beta,self.J)

        return self.Grille.average_magnetization()