import numpy as np
from numpy import random

class Grille:
    def __init__(taille):
        np.random.choice([-1,1],size=(taille,taille))
