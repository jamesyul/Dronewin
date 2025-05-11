import matplotlib.pyplot as plt
import numpy as np

def plot_map(grid, drones, threats):
    """Dibuja el mapa, las rutas de los drones y las amenazas."""
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='gray')
    
    # Dibujar rutas de los drones
    for drone in drones:
        if drone.path is not None:
            path = np.array(drone.path)
            plt.plot(path[:, 1], path[:, 0], 'b-', label='Ruta Drone')
    
    # Dibujar amenazas
    for threat in threats:
        plt.plot(threat.y, threat.x, 'ro', label=f'Amenaza ({threat.tipo})')
    
    plt.legend()
    plt.title('Simulación de Drones con Amenazas')
    plt.show()