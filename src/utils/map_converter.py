import osmnx as ox
import numpy as np
import pandas as pd
from shapely.geometry import box
import osmium as osm
import tempfile
import os

class PBFHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.nodes = []
        self.ways = []
        self.relations = []

    def node(self, n):
        # Almacenar las coordenadas como floats
        self.nodes.append((n.id, float(n.location.lon), float(n.location.lat)))

    def way(self, w):
        self.ways.append(w)

    def relation(self, r):
        self.relations.append(r)

def convert_pbf_to_grid(pbf_path, csv_path, grid_size=100):
    """
    Parámetros:
    - pbf_path: Ruta al archivo PBF.
    - csv_path: Ruta donde se guardará el CSV de la cuadrícula.
    - grid_size: Tamaño de la cuadrícula.
    """
    try:
        # Crear un handler para procesar el archivo PBF
        handler = PBFHandler()
        handler.apply_file(pbf_path)
        
        if not handler.nodes:
            raise ValueError("No se encontraron nodos en el archivo PBF")
        
        print(f"Número de nodos encontrados: {len(handler.nodes)}")
        
        # Imprimir las coordenadas de los primeros 5 nodos para depuración
        print("Primeros 5 nodos:")
        for i, (node_id, lon, lat) in enumerate(handler.nodes[:5]):
            print(f"Nodo {i+1}: ID={node_id}, lon={lon}, lat={lat}")
        
        # Crear un archivo temporal OSM XML
        with tempfile.NamedTemporaryFile(suffix='.osm', delete=False) as tmp:
            tmp_path = tmp.name
            
            # Escribir el encabezado OSM
            tmp.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tmp.write(b'<osm version="0.6">\n')
            
            # Escribir los nodos
            for node_id, lon, lat in handler.nodes:
                tmp.write(f'  <node id="{node_id}" lat="{lat}" lon="{lon}"/>\n'.encode())
            
            # Escribir el pie del archivo
            tmp.write(b'</osm>')
        
        print(f"Archivo temporal creado: {tmp_path}")
        
        # Cargar el grafo desde el archivo OSM temporal
        G = ox.graph_from_xml(tmp_path, simplify=False)
        
        # Limpiar el archivo temporal
        os.unlink(tmp_path)
    
        # Obtener los límites del mapa
        gdf_nodes = ox.graph_to_gdfs(G, edges=False)
        minx, miny, maxx, maxy = gdf_nodes.total_bounds
        
        print(f"Límites del mapa: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")
        
        # Verificar que los límites sean válidos
        if minx == maxx or miny == maxy:
            # Si los límites son iguales, agregar un pequeño margen
            margin = 0.0001  # Aproximadamente 11 metros
            minx -= margin
            maxx += margin
            miny -= margin
            maxy += margin
            print(f"Ajustando límites con margen: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")
        
        # Crear una cuadrícula de tamaño grid_size x grid_size
        grid = np.zeros((grid_size, grid_size), dtype=int)
        
        # Calcular el paso para cada celda en la cuadrícula
        x_step = (maxx - minx) / grid_size
        y_step = (maxy - miny) / grid_size
        
        print(f"Tamaño de celda: x_step={x_step}, y_step={y_step}")
        
        # Marcar celdas con obstáculos (simplificado: nodos como obstáculos)
        for _, node in gdf_nodes.iterrows():
            try:
                x = (node.geometry.x - minx) / x_step
                y = (node.geometry.y - miny) / y_step
                
                # Verificar que los valores no sean NaN
                if np.isnan(x) or np.isnan(y):
                    print(f"Advertencia: Coordenadas NaN para nodo {node.name}")
                    continue
                
                grid_x = int(x)
                grid_y = int(y)
                
                # Verificar que las coordenadas estén dentro de los límites
                if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
                    grid[grid_y, grid_x] = 1  # 1 para obstáculo
            except (ValueError, TypeError) as e:
                print(f"Advertencia: Error al procesar nodo {node.name}: {str(e)}")
                continue
        
        # Guardar la cuadrícula en un archivo CSV sin encabezado
        pd.DataFrame(grid).to_csv(csv_path, header=False, index=False)
        print(f"Mapa convertido y guardado en {csv_path}")
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        raise

if __name__ == "__main__":
    pbf_path = 'data/mapas/Mapa de Kursk.pbf'
    csv_path = 'data/mapas/mapa_inicial.csv'
    convert_pbf_to_grid(pbf_path, csv_path)