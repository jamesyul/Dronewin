import osmnx as ox
import numpy as np
import pandas as pd
from shapely.geometry import box, Polygon, LineString
import osmium as osm
import tempfile
import os

class PBFHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.nodes = {}  # Diccionario para nodos: node_id -> (lon, lat)
        self.obstacles = []  # Lista de obstáculos: (tipo, coordenadas)

    def node(self, n):
        # Almacenar coordenadas de nodos
        self.nodes[n.id] = (float(n.location.lon), float(n.location.lat))

    def way(self, w):
        tags = dict(w.tags)
        coords = []
        # Obtener coordenadas de los nodos del way
        for node_ref in w.nodes:
            if node_ref.ref in self.nodes:
                coords.append(self.nodes[node_ref.ref])
        
        if not coords:
            return

        # Identificar tipo de obstáculo según etiquetas
        if 'building' in tags:
            # Edificios como polígonos
            self.obstacles.append(('building', coords))
        elif 'waterway' in tags and tags['waterway'] in ['river', 'stream', 'canal']:
            # Ríos como líneas
            self.obstacles.append(('river', coords))
        elif 'highway' in tags and tags['highway'] in ['motorway', 'primary', 'secondary']:
            # Carreteras principales como líneas (opcional: decidir si son obstáculos)
            self.obstacles.append(('road', coords))
        elif 'landuse' in tags and tags['landuse'] == 'forest':
            # Bosques como polígonos
            self.obstacles.append(('forest', coords))
        elif 'landuse' in tags and tags['landuse'] == 'industrial':
            # Áreas industriales como polígonos
            self.obstacles.append(('industrial', coords))
        elif 'natural' in tags and tags['natural'] in ['wetland', 'hill']:
            # Pantanos o colinas como polígonos
            self.obstacles.append(('natural', coords))

    def relation(self, r):
        tags = dict(r.tags)
        if 'natural' in tags and tags['natural'] == 'water':
            # Lagos como polígonos (simplificado)
            coords = []
            for member in r.members:
                if member.type == 'n' and member.ref in self.nodes:
                    coords.append(self.nodes[member.ref])
            if coords:
                self.obstacles.append(('lake', coords))

def convert_pbf_to_grid(pbf_path, csv_path, grid_size=100):
    """
    Convierte un archivo PBF de OSM a una cuadrícula CSV con múltiples obstáculos.

    Parámetros:
    - pbf_path: Ruta al archivo PBF.
    - csv_path: Ruta donde se guardará el CSV de la cuadrícula.
    - grid_size: Tamaño de la cuadrícula.
    """
    try:
        # Procesar el archivo PBF
        handler = PBFHandler()
        handler.apply_file(pbf_path)

        if not handler.nodes:
            raise ValueError("No se encontraron nodos en el archivo PBF")

        print(f"Número de nodos encontrados: {len(handler.nodes)}")
        print(f"Número de obstáculos encontrados: {len(handler.obstacles)}")
        print("Tipos de obstáculos:", set(obstacle[0] for obstacle in handler.obstacles))

        # Crear archivo temporal OSM XML para compatibilidad con osmnx
        with tempfile.NamedTemporaryFile(suffix='.osm', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tmp.write(b'<osm version="0.6">\n')
            for node_id, (lon, lat) in handler.nodes.items():
                tmp.write(f'  <node id="{node_id}" lat="{lat}" lon="{lon}"/>\n'.encode())
            tmp.write(b'</osm>')

        print(f"Archivo temporal creado: {tmp_path}")

        # Cargar el grafo desde el archivo OSM temporal
        G = ox.graph_from_xml(tmp_path, simplify=False)
        os.unlink(tmp_path)

        # Obtener los límites del mapa
        gdf_nodes = ox.graph_to_gdfs(G, edges=False)
        minx, miny, maxx, maxy = gdf_nodes.total_bounds

        print(f"Límites del mapa: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")

        # Verificar límites válidos
        if minx == maxx or miny == maxy:
            margin = 0.0001  # ~11 metros
            minx -= margin
            maxx += margin
            miny -= margin
            maxy += margin
            print(f"Ajustando límites: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")

        # Crear cuadrícula
        grid = np.zeros((grid_size, grid_size), dtype=int)
        x_step = (maxx - minx) / grid_size
        y_step = (maxy - miny) / grid_size

        print(f"Tamaño de celda: x_step={x_step}, y_step={y_step}")

        # Función para marcar celdas dentro de un polígono o a lo largo de una línea
        def mark_obstacle(coords, obstacle_type):
            try:
                if len(coords) < 2:
                    return
                if obstacle_type in ['building', 'forest', 'industrial', 'natural', 'lake']:
                    # Tratar como polígono
                    poly = Polygon(coords)
                    if not poly.is_valid:
                        return
                    # Marcar todas las celdas dentro del polígono
                    for gy in range(grid_size):
                        for gx in range(grid_size):
                            cell_x = minx + gx * x_step + x_step / 2
                            cell_y = miny + gy * y_step + y_step / 2
                            if poly.contains(box(cell_x, cell_y, cell_x + x_step, cell_y + y_step)):
                                grid[gy, gx] = 1
                elif obstacle_type in ['river', 'road']:
                    # Tratar como línea
                    line = LineString(coords)
                    # Marcar celdas cercanas a la línea
                    for gy in range(grid_size):
                        for gx in range(grid_size):
                            cell_x = minx + gx * x_step + x_step / 2
                            cell_y = miny + gy * y_step + y_step / 2
                            cell_box = box(cell_x, cell_y, cell_x + x_step, cell_y + y_step)
                            if line.intersects(cell_box):
                                grid[gy, gx] = 1 if obstacle_type == 'river' else 1  # Carreteras como obstáculos
            except Exception as e:
                print(f"Error al procesar obstáculo {obstacle_type}: {str(e)}")

        # Marcar obstáculos en la cuadrícula
        for obstacle_type, coords in handler.obstacles:
            mark_obstacle(coords, obstacle_type)

        # Guardar la cuadrícula
        pd.DataFrame(grid).to_csv(csv_path, header=False, index=False)
        print(f"Mapa convertido y guardado en {csv_path}")
        print(f"Número de celdas marcadas como obstáculos: {np.sum(grid)}")

    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        raise

if __name__ == "__main__":
    pbf_path = 'data/mapas/Mapa de Kursk.pbf'
    csv_path = 'data/mapas/mapa_inicial.csv'
    convert_pbf_to_grid(pbf_path, csv_path)