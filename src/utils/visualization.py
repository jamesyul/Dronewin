import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_simulation(grid, drones, threats, steps=50):
    print(f"Total de amenazas cargadas: {len(threats)}")
    for threat in threats:
        print(f"Amenaza en ({threat.x}, {threat.y}), tipo: {threat.tipo}, rango: {threat.range}")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 49)
    ax.set_ylim(0, 49)
    
    def update(frame):
        ax.clear()
        ax.imshow(grid, cmap='gray', extent=[0, 49, 0, 49])
        
        for i, drone in enumerate(drones):
            if drone.path is not None:
                path = np.array(drone.path)
                ax.plot(path[:, 0], path[:, 1], label=f'Ruta Drone {i+1}')
                print(f"Ruta Drone {i+1}: {path}")
            else:
                print(f"Drone {i+1} en {drone.start} no tiene ruta a {drone.goal}")
            ax.plot(drone.start[0], drone.start[1], 'bo', label=f'Drone {i+1} Pos')
        
        for threat in threats:
            print(f"Dibujando amenaza en ({threat.x}, {threat.y})")
            ax.plot(threat.x, threat.y, 'ro', label=f'Amenaza ({threat.tipo})')
        
        ax.set_title(f'Simulación de Drones - Paso {frame}')
        ax.legend()
        ax.grid(True)
        
        if frame % 5 == 0:  # Mover amenazas cada 5 frames (2.5 segundos)
            for threat in threats:
                threat.move(grid, drones)
        for drone in drones:
            if drone.fuel > 0 and drone.start != drone.goal:
                from src.algorithms.pathfinding import a_star
                drone.path = a_star(grid, drone.start, drone.goal, threats)
                if drone.path is not None:
                    drone.move(drones)
    
    ani = animation.FuncAnimation(fig, update, frames=steps, interval=500, repeat=False)
    plt.show()