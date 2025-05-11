import numpy as np

class Drone:
    def __init__(self, start, goal, fuel):
        self.start = start  # Tupla (x, y)
        self.goal = goal    # Tupla (x, y)
        self.fuel = fuel    # Combustible inicial
        self.path = None    # Ruta calculada (lista de tuplas)

    def move(self):
        """Mueve el dron al siguiente punto de su ruta si hay combustible."""
        if self.path is not None and len(self.path) > 1 and self.fuel > 0:
            self.start = self.path[1]
            self.path = self.path[1:]
            self.fuel -= 1
            return True
        return False