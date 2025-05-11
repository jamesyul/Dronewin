import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_simulation(grid, drones, threats, steps=50):
    """Anima la simulación de drones y amenazas."""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    def update(frame):
        print(f"Actualizando frame {frame}")
        ax.clear()
        # Dibujar mapa
        ax.imshow(grid, cmap='gray')
        
        # Dibujar rutas de los drones
        for i, drone in enumerate(drones):
            if drone.path is not None:
                path = np.array(drone.path)
                ax.plot(path[:, 0], path[:, 1], label=f'Ruta Drone {i+1}')
        
        # Dibujar amenazas
        for threat in threats:
            ax.plot(threat.x, threat.y, 'ro', label=f'Amenaza ({threat.type})')
        
        # Configurar título y leyenda
        ax.set_title(f'Simulación de Drones - Paso {frame}')
        ax.legend()
        ax.grid(True)
        
        # Actualizar amenazas y drones
        for threat in threats:
            threat.move(grid)
        for drone in drones:
            if drone.fuel > 0 and drone.start != drone.goal:
                from src.algorithms.pathfinding import a_star
                drone.path = a_star(grid, drone.start, drone.goal, threats)
                if drone.path is None:
                    print(f"Drone en {drone.start} no encontró ruta a {drone.goal}")
                else:
                    print(f"Drone en {drone.start} encontró ruta: {drone.path}")
                if drone.path is not None:
                    drone.move(drones)

    # Crear animación
    ani = animation.FuncAnimation(fig, update, frames=steps, interval=500, repeat=False)
    plt.show()