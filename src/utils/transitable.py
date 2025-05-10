import pandas as pd

# Cargar el mapa
grid = pd.read_csv('data/mapas/mapa_inicial.csv', header=None).values

# Listar celdas transitables
transitables = [(x, y) for y in range(50) for x in range(50) if grid[y, x] == 0]

# Imprimir las primeras 10 celdas transitables
print("Celdas transitables (primeras 10):")
for x, y in transitables[:10]:
    print(f"({x}, {y})")