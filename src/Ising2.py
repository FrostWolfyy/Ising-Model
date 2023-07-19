from src.Grille import Grille 

class Ising2():
    def __init__(self, Grille, iterations, beta):
        self.Grille = Grille 
        self.iterations = iterations
        self.beta = beta

    def run(self):

        for i in range (self.iterations):
            mag = self.Grille.average_magnetization()
            energy = 0 

            for j in range (0, self.Grille.taille):
                for k in range (0, self.Grille.taille):
                    energy += self.Grille.energy(j,k) / 2
        
            self.Grille.metropolis(self.beta)

        return self.Grille.average_magnetization()