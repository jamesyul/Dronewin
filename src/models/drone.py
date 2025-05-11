import numpy as np

class Drone:
    def __init__(self, start, goal, fuel):
        self.start = start  # Tupla (x, y)
        self.goal = goal    # Tupla (x, y)
        self.fuel = fuel    # Combustible inicial
        self.path = None    # Ruta calculada (lista de tuplas)

    def move(self, drones):
        """Mueve el dron al siguiente punto de su ruta, evitando colisiones."""
        if self.path is not None and len(self.path) > 1 and self.fuel > 0:
            next_pos = self.path[1]
            # Verificar si la próxima posición está ocupada por otro dron
            for other_drone in drones:
                if other_drone != self and other_drone.start == next_pos:
                    return  # No moverse si hay colisión
            self.start = next_pos
            self.path = self.path[1:]
            self.fuel -= 1