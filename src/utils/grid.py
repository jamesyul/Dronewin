import pandas as pd
import numpy as np

def load_map(file_path):
    try:
        grid = pd.read_csv(file_path, header=None).values
        print(f"Mapa cargado: {grid.shape}")
        if grid.shape != (50, 50):
            raise ValueError(f"Se esperaba una cuadrícula de 50x50, pero se encontró {grid.shape}")
        return grid
    except Exception as e:
        raise Exception(f"Error al cargar el mapa: {str(e)}")

def is_transitable(grid, x, y):
    """
    Verifica si una celda es transitable.
    
    Parámetros:
    - grid: La cuadrícula del mapa.
    - x: Coordenada x (columna).
    - y: Coordenada y (fila).
    
    Retorna:
    - True si la celda es transitable (0), False si es un obstáculo (1) o está fuera de límites.
    """
    if 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]:
        return grid[y, x] == 0
    return False