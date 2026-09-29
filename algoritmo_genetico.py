# Archivo: algoritmos/genetico.py
import random
from busqueda_informada import distancia_manhattan, buscar_salida

def generar_individuo(longitud_max):
    """
    Un individuo (cromosoma) es una lista de movimientos.
    Incluye 'esperar' (0,0) como estipulan las reglas.
    """
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)] 
    return [random.choice(movimientos) for _ in range(longitud_max)]

def evaluar_fitness(individuo, entorno, inicio_x, inicio_y, meta):
    """
    Simula la ruta. El fitness es mayor mientras más cerca quede de la salida.
    """
    x, y = inicio_x, inicio_y
    ruta_valida = []
    
    for mov in individuo:
        nx, ny = x + mov[0], y + mov[1]
        
        # Validar límites del mapa
        if 0 <= nx < entorno.filas and 0 <= ny < entorno.columnas:
            # Si no es muro (1) ni fuego (3)
            if entorno.mapa[nx][ny] not in [1, 3]:
                x, y = nx, ny
                ruta_valida.append((x, y))
                
                if (x, y) == meta:
                    break # Llegó a la meta prematuramente
                    
    # Calculamos la distancia final a la meta
    dist = distancia_manhattan(x, y, meta[0], meta[1])
    
    if dist == 0:
        # Si llega a la meta, el fitness es inmenso. 
        # Premiamos las rutas que toman menos pasos.
        fitness = 10000 - len(ruta_valida) 
    else:
        # Si no llega, el fitness es inversamente proporcional a la distancia.
        fitness = 100 / (dist + 1) 
        
    return fitness, ruta_valida

def genetico_escape(entorno, inicio_x, inicio_y, generaciones=15, tam_poblacion=20, prob_mutacion=0.15):
    """
    Algoritmo metaheurístico bioinspirado optimizado para no colapsar la CPU.
    """
    meta = buscar_salida(entorno)
    if not meta: return []
    
    # OPTIMIZACIÓN CLAVE: En vez de filas * columnas (que da 225 o 900 en mapas grandes),
    # limitamos la "visión" del algoritmo a una distancia prudente.
    # El agente planeará una ruta proporcional al tamaño del mapa, pero sin excederse.
    longitud_max = int((entorno.filas + entorno.columnas) * 1.5)
    
    # 1. Población inicial
    poblacion = [generar_individuo(longitud_max) for _ in range(tam_poblacion)]
    
    mejor_ruta_global = []
    mejor_fitness_global = -1
    
    for generacion in range(generaciones):
        evaluaciones = []
        
        # 2. Evaluar a todos los individuos
        for individuo in poblacion:
            fitness, ruta = evaluar_fitness(individuo, entorno, inicio_x, inicio_y, meta)
            evaluaciones.append((fitness, individuo, ruta))
            
            if fitness > mejor_fitness_global:
                mejor_fitness_global = fitness
                mejor_ruta_global = ruta
                
        if mejor_fitness_global > 9000:
            break
            
        evaluaciones.sort(key=lambda x: x[0], reverse=True)
        
        # 3. Selección (Elitismo: guardamos siempre a los mejores)
        mejores_individuos = [ind for fit, ind, ruta in evaluaciones[:tam_poblacion//2]]
        
        # 4. Cruce
        nueva_poblacion = mejores_individuos.copy()
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = random.choice(mejores_individuos)
            padre2 = random.choice(mejores_individuos)
            punto_corte = random.randint(1, longitud_max - 1)
            hijo = padre1[:punto_corte] + padre2[punto_corte:]
            nueva_poblacion.append(hijo)
            
        # 5. Mutación
        movimientos_posibles = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        for i in range(len(nueva_poblacion)):
            if random.random() < prob_mutacion:
                punto_mutacion = random.randint(0, longitud_max - 1)
                nueva_poblacion[i][punto_mutacion] = random.choice(movimientos_posibles)
                
        poblacion = nueva_poblacion
        
    return mejor_ruta_global