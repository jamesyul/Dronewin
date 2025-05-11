import numpy as np
from src.utils.grid import load_map
from src.models.threats import load_threats

# Cargar el mapa
grid = load_map('data/mapas/mapa_inicial.csv')

# Cargar las amenazas
threats = load_threats('data/amenazas/amenazas_iniciales.csv')

# Imprimir las amenazas cargadas
for threat in threats:
    print(f"Amenaza: ({threat.x}, {threat.y}), Tipo: {threat.type}, Rango: {threat.range}")

# Probar el movimiento de una amenaza
print("\nMoviendo la primera amenaza:")
threat = threats[0]
print(f"Posición inicial: ({threat.x}, {threat.y})")
for _ in range(3):
    threat.move(grid)
    print(f"Nueva posición: ({threat.x}, {threat.y})")