Dronewin
Descripción
Dronewin es un proyecto de simulación de drones que utiliza el algoritmo A* para encontrar rutas óptimas en un mapa de 50x50, evitando obstáculos y minimizando riesgos por amenazas (como radares y sistemas antiaéreos). El mapa y las amenazas se cargan desde archivos CSV, y la simulación se visualiza usando Matplotlib. Este proyecto incluye:

Generación de mapas a partir de datos OSM (archivos PBF).
Cálculo de rutas considerando costos por amenazas.
Visualización animada del movimiento de los drones.
Soporte para múltiples drones con colisiones evitadas.

Demostración
Aquí tienes un video que muestra la simulación en acción, con un dron moviéndose desde la posición (35, 15) hasta (26, 0) con 100 unidades de combustible:
Ver video de demostración
(Nota: Reemplaza <tu-usuario> con tu nombre de usuario de GitHub y asegúrate de subir el video al directorio demo/ en tu repositorio.)
Requisitos
Para ejecutar este proyecto, necesitas tener instalado:

Python 3.8 o superior
Las siguientes bibliotecas de Python (puedes instalarlas con pip):pandas numpy matplotlib osmium shapely



Instalación

Clona el repositorio desde GitHub:
git clone https://github.com/<tu-usuario>/Dronewin.git
cd Dronewin


(Opcional) Crea un entorno virtual para mantener las dependencias aisladas:
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


Instala las dependencias:
pip install pandas numpy matplotlib osmium shapely


Asegúrate de que los archivos de datos estén en su lugar:

data/mapas/mapa_inicial.csv: Mapa generado (puedes generarlo con map_converter.py).
data/amenazas/amenazas_iniciales.csv: Lista de amenazas.



Uso

Genera el mapa si no tienes mapa_inicial.csv:
python src/map_converter.py

Esto generará data/mapas/mapa_inicial.csv a partir de un archivo PBF (asegúrate de tener data/mapas/Mapa de Kursk.pbf o ajusta la ruta en el script).

Ejecuta la simulación:
cd src
python simulation.py


Ingresa los datos del dron cuando se te solicite. Por ejemplo, para replicar el video de demostración:
Ingrese el número de drones: 1
Drone 1 - Coordenada X inicial (0-49): 35
Drone 1 - Coordenada Y inicial (0-49): 15
Drone 1 - Coordenada X objetivo (0-49): 26
Drone 1 - Coordenada Y objetivo (0-49): 0
Drone 1 - Combustible inicial: 100


Observa la simulación en la ventana de Matplotlib. Los resultados se guardarán en resultados_simulacion.txt.


Estructura del proyecto

src/: Código fuente del proyecto.
simulation.py: Script principal para ejecutar la simulación.
visualization.py: Visualización de la simulación con Matplotlib.
pathfinding.py: Implementación del algoritmo A* con costos por amenazas.
drone.py: Clase Drone para gestionar drones.
threats.py: Clase Threat y funciones para cargar amenazas.
map_converter.py: Convierte datos OSM (PBF) a un mapa CSV.
utils/grid.py: Funciones para cargar y verificar el mapa.


data/: Archivos de datos.
mapas/mapa_inicial.csv: Mapa de 50x50 con obstáculos.
amenazas/amenazas_iniciales.csv: Lista de amenazas.


resultados_simulacion.txt: Resultados de la simulación (generado automáticamente).

Notas

Asegúrate de que mapa_inicial.csv y amenazas_iniciales.csv estén presentes en las rutas especificadas. Puedes usar transitable.py para verificar las celdas transitables:python src/transitable.py


Si el dron no se mueve, verifica que las coordenadas iniciales y objetivo sean transitables (valor 0 en el mapa) y que el combustible sea suficiente.

Contribuciones
¡Las contribuciones son bienvenidas! Si deseas colaborar, por favor:

Haz un fork del repositorio.
Crea una rama para tu feature (git checkout -b feature/nueva-funcionalidad).
Haz commit de tus cambios (git commit -m "Añadir nueva funcionalidad").
Sube tu rama al remoto (git push origin feature/nueva-funcionalidad).
Crea un Pull Request en GitHub.

Licencia
Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles. (Nota: Si no tienes un archivo LICENSE, te recomiendo crearlo con el texto estándar de la Licencia MIT.)
Autor

Yul Cardenas - GitHub

