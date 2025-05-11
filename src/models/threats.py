import pandas as pd
import random
import numpy as np

class Threat:
    def __init__(self, x, y, tipo, range):
        """Inicializa una amenaza con posición, tipo y rango."""
        self.x = int(x)  # Coordenada x (columna)
        self.y = int(y)  # Coordenada y (fila)
        self.tipo = tipo  # Tipo de amenaza (e.g., 'antiaerea', 'radar')
        self.range = int(range)  # Rango de influencia

    def move(self, grid):
        """Mueve la amenaza aleatoriamente dentro de los límites del grid."""
        # Posibles desplazamientos: -1, 0, 1
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        # Calcular nueva posición asegurando que esté dentro del grid (50x50)
        new_x = max(0, min(grid.shape[1] - 1, self.x + dx))  # shape[1] = 50
        new_y = max(0, min(grid.shape[0] - 1, self.y + dy))  # shape[0] = 50
        # Actualizar posición solo si la nueva celda es transitable (valor 0)
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