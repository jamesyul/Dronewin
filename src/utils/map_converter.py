import numpy as np
import pandas as pd
from shapely.geometry import box, Polygon, LineString
import osmium as osm

class PBFHandler(osm.SimpleHandler):
    def __init__(self, bbox):
        osm.SimpleHandler.__init__(self)
        self.nodes = {}  # node_id -> (lon, lat)
        self.obstacles = []  # (tipo, coordenadas)
        self.bbox = bbox  # (min_lon, min_lat, max_lon, max_lat)

    def node(self, n):
        lon, lat = float(n.location.lon), float(n.location.lat)
        if self.bbox:
            min_lon, min_lat, max_lon, max_lat = self.bbox
            if not (min_lon <= lon <= max_lon and min_lat <= lat <= max_lat):
                return
        self.nodes[n.id] = (lon, lat)

    def way(self, w):
        tags = dict(w.tags)
        coords = [self.nodes[node_ref.ref] for node_ref in w.nodes if node_ref.ref in self.nodes]
        if len(coords) < 2:
            return

        # Identificar tipo de obstáculo
        obstacle_type = None
        if 'building' in tags:
            obstacle_type = 'building'
        elif 'waterway' in tags and tags['waterway'] in ['river', 'stream', 'canal']:
            obstacle_type = 'river'
        elif 'highway' in tags and tags['highway'] in ['motorway', 'primary', 'secondary']:
            obstacle_type = 'road'
        elif 'landuse' in tags and tags['landuse'] == 'forest':
            obstacle_type = 'forest'
        elif 'landuse' in tags and tags['landuse'] == 'industrial':
            obstacle_type = 'industrial'
        elif 'landuse' in tags and tags['landuse'] == 'residential':
            obstacle_type = 'residential'
        elif 'natural' in tags and tags['natural'] in ['wetland', 'hill', 'ridge']:
            obstacle_type = 'natural'

        if obstacle_type:
            self.obstacles.append((obstacle_type, coords))

    def relation(self, r):
        tags = dict(r.tags)
        if 'natural' in tags and tags['natural'] == 'water':
            coords = []
            for member in r.members:
                if member.type == 'n' and member.ref in self.nodes:
                    coords.append(self.nodes[member.ref])
            if len(coords) >= 2:
                self.obstacles.append(('lake', coords))

def convert_pbf_to_grid(pbf_path, csv_path, grid_size=50):
    """
    Convierte un archivo PBF de OSM a una cuadrícula CSV con múltiples obstáculos.

    Parámetros:
    - pbf_path: Ruta al archivo PBF.
    - csv_path: Ruta donde se guardará el CSV de la cuadrícula.
    - grid_size: Tamaño de la cuadrícula.
    """
    try:
        # Caja delimitadora para Kursk
        kursk_bbox = (36.1, 51.65, 36.25, 51.75)
        handler = PBFHandler(bbox=kursk_bbox)
        handler.apply_file(pbf_path)

        print(f"Nodos almacenados: {len(handler.nodes)}")
        print(f"Obstáculos encontrados: {len(handler.obstacles)}")
        print("Tipos de obstáculos:", set(obstacle[0] for obstacle in handler.obstacles))

        if not handler.nodes or not handler.obstacles:
            raise ValueError("No se encontraron nodos u obstáculos en el área especificada. Verifica el archivo PBF o la caja delimitadora.")

        # Calcular límites basados en nodos
        lons, lats = zip(*handler.nodes.values())
        minx, maxx = min(lons), max(lons)
        miny, maxy = min(lats), max(lats)

        print(f"Límites del mapa: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")

        # Ajustar límites si son idénticos
        if minx == maxx or miny == maxy:
            margin = 0.001  # ~100 metros
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

        # Función para marcar obstáculos
        def mark_obstacle(coords, obstacle_type):
            try:
                if len(coords) < 2:
                    return

                if obstacle_type in ['building', 'forest', 'industrial', 'residential', 'natural', 'lake']:
                    if len(coords) >= 4 and coords[0] == coords[-1]:
                        poly = Polygon(coords)
                        if not poly.is_valid:
                            return
                        min_px, min_py, max_px, max_py = poly.bounds
                        min_gx = max(0, int((min_px - minx) / x_step))
                        min_gy = max(0, int((min_py - miny) / y_step))
                        max_gx = min(grid_size, int((max_px - minx) / x_step) + 1)
                        max_gy = min(grid_size, int((max_py - miny) / y_step) + 1)
                        for gy in range(min_gy, max_gy):
                            for gx in range(min_gx, max_gx):
                                cell_x = minx + gx * x_step
                                cell_y = miny + gy * y_step
                                cell_box = box(cell_x, cell_y, cell_x + x_step, cell_y + y_step)
                                if poly.intersects(cell_box):
                                    grid[gy, gx] = 1
                    else:
                        line = LineString(coords)
                        min_px, min_py, max_px, max_py = line.bounds
                        min_gx = max(0, int((min_px - minx) / x_step))
                        min_gy = max(0, int((min_py - miny) / y_step))
                        max_gx = min(grid_size, int((max_px - minx) / x_step) + 1)
                        max_gy = min(grid_size, int((max_py - miny) / y_step) + 1)
                        for gy in range(min_gy, max_gy):
                            for gx in range(min_gx, max_gx):
                                cell_x = minx + gx * x_step
                                cell_y = miny + gy * y_step
                                cell_box = box(cell_x, cell_y, cell_x + x_step, cell_y + y_step)
                                if line.intersects(cell_box):
                                    grid[gy, gx] = 1
                elif obstacle_type == 'river':
                    line = LineString(coords)
                    min_px, min_py, max_px, max_py = line.bounds
                    min_gx = max(0, int((min_px - minx) / x_step))
                    min_gy = max(0, int((min_py - miny) / y_step))
                    max_gx = min(grid_size, int((max_px - minx) / x_step) + 1)
                    max_gy = min(grid_size, int((max_py - miny) / y_step) + 1)
                    for gy in range(min_gy, max_gy):
                        for gx in range(min_gx, max_gx):
                            cell_x = minx + gx * x_step
                            cell_y = miny + gy * y_step
                            cell_box = box(cell_x, cell_y, cell_x + x_step, cell_y + y_step)
                            if line.intersects(cell_box):
                                grid[gy, gx] = 1
                elif obstacle_type == 'road':
                    # Carreteras transitables
                    pass
            except Exception as e:
                print(f"Error al procesar obstáculo {obstacle_type}: {str(e)}")

        # Marcar obstáculos
        for obstacle_type, coords in handler.obstacles:
            mark_obstacle(coords, obstacle_type)

        # Guardar cuadrícula
        pd.DataFrame(grid).to_csv(csv_path, header=False, index=False)
        print(f"Mapa convertido y guardado en {csv_path}")
        print(f"Número de celdas marcadas como obstáculos: {np.sum(grid)}")

    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        raise

if __name__ == "__main__":
    pbf_path = 'data/mapas/Mapa de Kursk.pbf'
    csv_path = 'data/mapas/mapa_inicial.csv'
    convert_pbf_to_grid(pbf_path, csv_path, grid_size=50)