import time
import matplotlib.pyplot as plt
from utils.grid import load_map
from models.threats import load_threats
from utils.visualization import plot_map
from models.drone import Drone
from algorithms.pathfinding import a_star

# Cargar el mapa y las amenazas
grid = load_map("data/mapas/mapa_inicial.csv")
threats = load_threats("data/amenazas/amenazas_iniciales.csv")

# Definir drones con posiciones dentro del mapa 50x50
drones = [
    Drone((0, 0), (49, 49), 150),  # Drone 1: de esquina a esquina
    Drone((0, 49), (49, 0), 150)   # Drone 2: de otra esquina a esquina
]

# Simulación principal
for step in range(50):  # 50 pasos para un mapa más pequeño
    for drone in drones:
        if drone.path is None:
            # Calcular ruta evitando amenazas y obstáculos
            drone.path = a_star(grid, drone.start, drone.goal, threats)
        drone.move()  # Mover el drone a lo largo de la ruta
    
    # Visualizar cada 5 pasos
    if step % 5 == 0:
        plot_map(grid, drones, threats)
        time.sleep(0.5)

# Visualización final
plot_map(grid, drones, threats)
plt.show()