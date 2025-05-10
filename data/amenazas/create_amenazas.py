import pandas as pd

amenazas = [
    {"x": 25, "y": 0, "tipo": "antiaerea", "rango": 5},
    {"x": 30, "y": 20, "tipo": "radar", "rango": 8},
    {"x": 26, "y": 0, "tipo": "antiaerea", "rango": 6},
    {"x": 40, "y": 45, "tipo": "radar", "rango": 10},
]

df = pd.DataFrame(amenazas)
df.to_csv('data/amenazas/amenazas_iniciales.csv', index=False)
print("Archivo actualizado.")