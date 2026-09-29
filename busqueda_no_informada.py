from collections import deque

def bfs_escape(entorno, inicio_x, inicio_y):
    """
    Algoritmo BFS adaptado para encontrar la ruta hacia la salida en la grilla.
    """
    
    cola = deque()
    cola.append((inicio_x, inicio_y))
    
   
    visitados = set()
    visitados.add((inicio_x, inicio_y))
    
  
    padres = {}
    
    # Movimientos ortogonales permitidos: (x, y)
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while cola:
        
        x, y = cola.popleft()
        
       
        if entorno.mapa[x][y] == 2:
            return reconstruir_ruta(padres, (x, y))
            
       
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
           
            if 0 <= nx < entorno.filas and 0 <= ny < entorno.columnas:
                # Verificamos que no sea muro (1) ni fuego (3) y no esté visitado
                if entorno.mapa[nx][ny] not in [1, 3] and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    padres[(nx, ny)] = (x, y) # Guardamos de dónde vinimos
                    cola.append((nx, ny))
                    
    # Si la cola se vacía y no retornó antes, no hay salida posible
    return []

def reconstruir_ruta(padres, meta):
    """
    Rastrea el diccionario de padres desde la meta hasta el inicio 
    para devolver la lista de pasos.
    """
    ruta = []
    actual = meta
    while actual in padres:
        ruta.append(actual)
        actual = padres[actual]
    ruta.reverse() # Invertimos para que vaya desde el inicio a la meta
    return ruta

def dfs_escape(entorno, inicio_x, inicio_y):
    """
    Algoritmo DFS adaptado usando una pila para evitar límites de recursión en mapas grandes.
    """
    # En Python, una lista nativa funciona perfectamente como pila usando append() y pop()
    pila = [(inicio_x, inicio_y)]
    
    visitados = set()
    visitados.add((inicio_x, inicio_y))
    
    padres = {}
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while pila:
        
        x, y = pila.pop()
        
        if entorno.mapa[x][y] == 2:
            return reconstruir_ruta(padres, (x, y))
            
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < entorno.filas and 0 <= ny < entorno.columnas:
                if entorno.mapa[nx][ny] not in [1, 3] and (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    padres[(nx, ny)] = (x, y)
                    pila.append((nx, ny))
                    
    return []


