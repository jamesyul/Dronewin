import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_simulation(grid, drones, threats, steps=100):  # Aumentamos a 100 pasos
    print(f"Total de amenazas cargadas: {len(threats)}")
    for threat in threats:
        print(f"Amenaza en ({threat.x}, {threat.y}), tipo: {threat.tipo}, rango: {threat.range}")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 49)
    ax.set_ylim(0, 49)
    
    move_interval = 60  # Amenazas se mueven cada 30 segundos
    
    def update(frame):
        ax.clear()
        ax.imshow(grid, cmap='gray', extent=[0, 49, 0, 49])
        
        # Dibujar drones y sus rutas
        for i, drone in enumerate(drones):
            # Dibujar el historial completo del dron
            if drone.history:
                history = np.array(drone.history)
                ax.plot(history[:, 0], history[:, 1], 'b.-', markersize=5, label=f'Trayecto Drone {i+1}')
                print(f"Trayecto Drone {i+1}: {drone.history}")
            
            # Dibujar la posición actual
            if drone.start == drone.goal:
                ax.plot(drone.start[0], drone.start[1], 'g*', markersize=10, label=f'Drone {i+1} ¡Objetivo!')
            else:
                ax.plot(drone.start[0], drone.start[1], 'bo', label=f'Drone {i+1} Pos')
        
        # Dibujar amenazas
        for threat in threats:
            print(f"Dibujando amenaza en ({threat.x}, {threat.y})")
            ax.plot(threat.x, threat.y, 'ro', label=f'Amenaza ({threat.tipo})')
        
        ax.set_title(f'Simulación de Drones - Paso {frame}')
        ax.legend()
        ax.grid(True)
        
        # Mover amenazas cada 'move_interval' frames
        if frame % move_interval == 0:
            for threat in threats:
                threat.move(grid, drones)
        
        # Actualizar posición de los drones
        for drone in drones:
            if drone.fuel > 0 and drone.start != drone.goal:
                from algorithms.pathfinding import a_star
                if drone.path is None or len(drone.path) <= 1:  # Solo recalcular si es necesario
                    drone.path = a_star(grid, drone.start, drone.goal, threats)
                if frame % 2 == 0:  # Mover dron cada 2 frames (1 paso por segundo)
                    if drone.path is not None:
                        drone.move(drones)
                        print(f"Dron movido a {drone.start}")
                    else:
                        print(f"No se encontró ruta para Drone {i+1} desde {drone.start} a {drone.goal}")
    
    ani = animation.FuncAnimation(fig, update, frames=steps, interval=500, repeat=False)
    plt.show()