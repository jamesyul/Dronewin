import pandas as pd
import random
import numpy as np

class Threat:
    def __init__(self, x, y, tipo, range):
        self.x = int(x)
        self.y = int(y)
        self.tipo = tipo
        self.range = int(range)

    def move(self, grid, drones):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        new_x = max(0, min(grid.shape[1] - 1, self.x + dx))
        new_y = max(0, min(grid.shape[0] - 1, self.y + dy))
        # Evitar superposición con drones
        for drone in drones:
            if (new_x, new_y) == drone.start:
                return  # No mover si la nueva posición está ocupada por un dron
        if grid[new_y, new_x] == 0:
            self.x, self.y = new_x, new_y

def load_threats(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['x', 'y', 'tipo', 'rango']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("El archivo CSV debe contener las columnas: x, y, tipo, rango")
        threats = [Threat(row['x'], row['y'], row['tipo'], row['rango']) for _, row in df.iterrows()]
        for threat in threats:
            if not (0 <= threat.x < 50 and 0 <= threat.y < 50):
                raise ValueError(f"Posición de amenaza ({threat.x}, {threat.y}) fuera del mapa 50x50")
        return threats
    except Exception as e:
        raise Exception(f"Error al cargar las amenazas: {str(e)}")