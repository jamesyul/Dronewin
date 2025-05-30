import pandas as pd
from utils.grid import load_map, is_transitable
from utils.visualization import animate_simulation
from models.drone import Drone
from models.threats import load_threats

def get_user_drones(grid):
    """Obtiene la información de los drones desde la entrada del usuario."""
    while True:
        try:
            num_drones = int(input("Ingrese el número de drones: "))
            if num_drones <= 0:
                raise ValueError("El número de drones debe ser positivo.")
            break
        except ValueError as e:
            print(f"Error: {e}. Intente de nuevo.")

    drones = []
    for i in range(num_drones):
        while True:
            try:
                start_x = int(input(f"Drone {i+1} - Coordenada X inicial (0-49): "))
                start_y = int(input(f"Drone {i+1} - Coordenada Y inicial (0-49): "))
                goal_x = int(input(f"Drone {i+1} - Coordenada X objetivo (0-49): "))
                goal_y = int(input(f"Drone {i+1} - Coordenada Y objetivo (0-49): "))
                fuel = int(input(f"Drone {i+1} - Combustible inicial: "))

                if not (0 <= start_x < 50 and 0 <= start_y < 50 and 0 <= goal_x < 50 and 0 <= goal_y < 50):
                    raise ValueError("Las coordenadas deben estar entre 0 y 49.")
                if not is_transitable(grid, start_x, start_y):
                    raise ValueError(f"La posición inicial ({start_x}, {start_y}) no es transitable.")
                if not is_transitable(grid, goal_x, goal_y):
                    raise ValueError(f"La posición objetivo ({goal_x}, {goal_y}) no es transitable.")
                if fuel <= 0:
                    raise ValueError("El combustible debe ser positivo.")

                drones.append(Drone((start_x, start_y), (goal_x, goal_y), fuel))
                break
            except ValueError as e:
                print(f"Error: {e}. Intente de nuevo.")

    return drones

def run_simulation():
    # Cargar datos
    grid = load_map("../data/mapas/mapa_inicial.csv")
    print(f"Mapa cargado: {grid.shape}")
    print(f"Valor en (0, 0): {grid[0, 0]}")
    print(f"Valor en (49, 49): {grid[49, 49]}")

    # Cargar amenazas con depuración
    try:
        threats = load_threats("../data/amenazas/amenazas_iniciales.csv")
        print(f"Total de amenazas cargadas: {len(threats)}")
        for threat in threats:
            print(f"Amenaza en ({threat.x}, {threat.y}), tipo: {threat.tipo}, rango: {threat.range}")
    except Exception as e:
        print(f"Error al cargar amenazas: {str(e)}")
        return

    # Obtener drones desde la entrada del usuario
    drones = get_user_drones(grid)

    # Ejecutar animación
    try:
        animate_simulation(grid, drones, threats, steps=100)
    except Exception as e:
        print(f"Error en la animación: {str(e)}")
        return
    
    # Guardar resultados
    with open('resultados_simulacion.txt', 'w') as f:
        for i, drone in enumerate(drones):
            status = "Alcanzó meta" if drone.start == drone.goal else f"Parado en {drone.start} (sin combustible o sin ruta)"
            f.write(f"Drone {i+1}: {status}, Combustible restante: {drone.fuel}\n")
            f.write(f"Historial de posiciones: {drone.history}\n")
    print("Simulación finalizada. Resultados guardados en resultados_simulacion.txt.")

if __name__ == "__main__":
    run_simulation()