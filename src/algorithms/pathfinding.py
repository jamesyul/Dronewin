import heapq
import numpy as np

def heuristic(a, b):
    """Heurística de distancia Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def threat_cost(x, y, threats):
    """Calcula el costo adicional por proximidad a amenazas."""
    total_cost = 0
    for threat in threats:
        dist = max(abs(x - threat.x), abs(y - threat.y))
        if dist <= threat.range:
            total_cost += (threat.range - dist) * 2  # Costo proporcional a la cercanía
    return total_cost

def a_star(grid, start, goal, threats):
    """Algoritmo A* con costos influenciados por amenazas."""
    rows, cols = grid.shape
    if not (0 <= start[0] < cols and 0 <= start[1] < rows and 0 <= goal[0] < cols and 0 <= goal[1] < rows):
        return None  # Fuera de los límites
    if grid[start[1], start[0]] != 0 or grid[goal[1], goal[0]] != 0:
        return None  # Inicio o meta en obstáculo

    open_set = [(0, start)]  # (f_score, posición)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Retorna la lista de tuplas

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos cardinales
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                continue
            if grid[neighbor[1], neighbor[0]] != 0:  # Obstáculo
                continue

            tentative_g_score = g_score[current] + 1 + threat_cost(neighbor[0], neighbor[1], threats)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No se encontró ruta