import pandas as pd

# Cargar el mapa
grid = pd.read_csv("../../data/mapas/mapa_inicial.csv", header=None).values

# Listar celdas transitables
transitables = [(x, y) for y in range(50) for x in range(50) if grid[y, x] == 0]

# Mostrar un resumen
total_transitables = len(transitables)
print(f"Total de celdas transitables: {total_transitables}")

# Opcional: Guardar en un archivo si hay muchas
if total_transitables > 50:
    with open("celdas_transitables.txt", "w") as f:
        f.write("Celdas transitables:\n")
        for x, y in transitables:
            f.write(f"({x}, {y})\n")
    print("Lista completa guardada en 'celdas_transitables.txt' debido a la gran cantidad de celdas.")
else:
    print("Celdas transitables:")
    for x, y in transitables:
        print(f"({x}, {y})")