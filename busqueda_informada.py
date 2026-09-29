import heapq

def distancia_manhattan(x1, y1, x2, y2):
    """
    Heurística admisible: Calcula la distancia en una grilla sin diagonales.
    """
    return abs(x1 - x2) + abs(y1 - y2)

def buscar_salida(entorno):
    """
    Función auxiliar para encontrar las coordenadas de la salida (2).
    """
    for i in range(entorno.filas):
        for j in range(entorno.columnas):
            if entorno.mapa[i][j] == 2:
                return (i, j)
    return None

def a_star_escape(entorno, inicio_x, inicio_y):
    """
    Algoritmo A* que considera tanto la distancia a la meta (heurística) 
    como el costo por congestión de las casillas.
    """
    meta = buscar_salida(entorno)
    if not meta: return []
    meta_x, meta_y = meta

    # Cola de prioridad (F_costo, G_costo, x, y)
    # F_costo = G_costo + Heurística
    cola = []
    heapq.heappush(cola, (0, 0, inicio_x, inicio_y))
    
    # Costos acumulados para llegar a cada nodo (G)
    costos = {(inicio_x, inicio_y): 0}
    padres = {}
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while cola:
        f, g_actual, x, y = heapq.heappop(cola)
        
        if (x, y) == meta:
            from busqueda_no_informada import reconstruir_ruta
            return reconstruir_ruta(padres, (x, y))
            
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < entorno.filas and 0 <= ny < entorno.columnas:
                if entorno.mapa[nx][ny] not in [1, 3]:
                    # Aquí sumamos el costo penalizado por congestión
                    costo_paso = entorno.calcular_costo_casilla(nx, ny)
                    nuevo_g = g_actual + costo_paso
                    
                    if (nx, ny) not in costos or nuevo_g < costos[(nx, ny)]:
                        costos[(nx, ny)] = nuevo_g
                        # f(n) = g(n) + h(n)
                        prioridad = nuevo_g + distancia_manhattan(nx, ny, meta_x, meta_y)
                        
                        heapq.heappush(cola, (prioridad, nuevo_g, nx, ny))
                        padres[(nx, ny)] = (x, y)
                        
    return []

def greedy_escape(entorno, inicio_x, inicio_y):
    """
    Algoritmo Greedy Best-First Search.
    Solo se guía por la heurística, ignorando el costo de las casillas.
    """
    meta = buscar_salida(entorno)
    if not meta: return []
    meta_x, meta_y = meta

    # Cola de prioridad (Heurística, x, y)
    cola = []
    heapq.heappush(cola, (0, inicio_x, inicio_y))
    
    visitados = set()
    visitados.add((inicio_x, inicio_y))
    padres = {}
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while cola:
        h, x, y = heapq.heappop(cola)
        
        if (x, y) == meta:
            from busqueda_no_informada import reconstruir_ruta
            return reconstruir_ruta(padres, (x, y))
            
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < entorno.filas and 0 <= ny < entorno.columnas:
                if entorno.mapa[nx][ny] not in [1, 3] and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    padres[(nx, ny)] = (x, y)
                    
                    # A diferencia de A*, Greedy solo usa la heurística como prioridad
                    prioridad = distancia_manhattan(nx, ny, meta_x, meta_y)
                    heapq.heappush(cola, (prioridad, nx, ny))
                    
    return []