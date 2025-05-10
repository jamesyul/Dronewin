from grid import load_map, is_transitable
import pandas as pd

# Cargar el mapa
grid = load_map('data/mapas/mapa_inicial.csv')

# Cargar las amenazas
amenazas = pd.read_csv('data/amenazas/amenazas_iniciales.csv')

# Verificar cada amenaza
for index, amenaza in amenazas.iterrows():
    x, y = amenaza['x'], amenaza['y']
    if is_transitable(grid, x, y):
        print(f"Amenaza en ({x}, {y}) está en una celda transitable.")
    else:
        print(f"¡Error! Amenaza en ({x}, {y}) está en un obstáculo o fuera de límites.")