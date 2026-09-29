# Tarea 1: Inteligancie artificial - Simulación de Evacuación

## Integrantes
* Vicente Andrés Ramírez Torrealba


## Descripción
Este proyecto simula la evacuación de un edificio en llamas utilizando agentes inteligentes. Se implementaron cinco algoritmos de búsqueda y optimización para guiar a los agentes hacia una salida única, evadiendo la propagación del fuego y minimizando la congestión o cuellos de botella.

## Requisitos de Ejecución
Para ejecutar el entorno de simulación y el benchmarking, se requiere Python 3.12.3 o superior y las siguientes librerías para la generación de gráficos:
`pip install pandas matplotlib`

## Instrucciones de Ejecución
El proyecto está dividido en tres escenarios de prueba, grillas de 6 * 9, 15 * 15 y 30 * 30 para evaluar la escalabilidad de los algoritmos.

1. **Generar resultados (Benchmarking):**
   Ejecutar cualquiera de los siguientes scripts en la terminal para iniciar la simulación automática (80 iteraciones). Cada script generará un archivo `.csv` con las estadísticas:
   * `python benchmark1.py` -> Genera `resultadosb1.csv`
   * `python benchmark2.py` -> Genera `resultadosb2.csv`
   * `python benchmark3.py`  -> Genera `resultadosb3.csv`

2. **Generar Gráficos:**
   Una vez obtenidos los archivos `.csv`, ejecutar el siguiente comando para generar los gráficos comparativos en formato `.png`:
   * `python grafico1.py`

   Se puede ver el paso a paso de los algoritmos en los tableros a elección recalcando que el 30*30 es mas pesado para ejecutar en consola 
   * `python main.py`

## Origen del Código y Citaciones
* **Algoritmos BFS y DFS:** Adaptados de código fuente propio de del ramo Estructura de Datos.
* **Asistencia de IA Generativa:** La estructuración del entorno matricial, la optimización metaheurística bioinspirada (Algoritmo Genético) y los scripts de recolección de métricas/benchmarking fueron desarrollados en colaboración estructurada con Gemini (Google AI) debido a la complejidad de los algoritmos.