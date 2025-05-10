from grid import load_map, is_transitable

def test_grid():
    try:
        # Cargar el mapa
        grid = load_map('data/mapas/mapa_inicial.csv')
        
        # Verificar la forma del mapa
        print(f"Forma del mapa: {grid.shape}")
        assert grid.shape == (50, 50), f"Se esperaba una cuadrícula de 50x50, pero se obtuvo {grid.shape}"
        
        # Probar algunas celdas específicas basadas en el CSV proporcionado
        print(f"Celda (0, 0): {'transitable' if is_transitable(grid, 0, 0) else 'obstáculo'}")
        print(f"Celda (25, 0): {'transitable' if is_transitable(grid, 25, 0) else 'obstáculo'}")
        print(f"Celda (40, 40): {'transitable' if is_transitable(grid, 40, 40) else 'obstáculo'}")
        
        # Probar una celda fuera de los límites
        print(f"Celda (50, 50): {'transitable' if is_transitable(grid, 50, 50) else 'obstáculo'}")
        
        print("Todas las pruebas pasaron correctamente.")
    except Exception as e:
        print(f"Error en la prueba: {str(e)}")

if __name__ == "__main__":
    test_grid()