class Entorno:
    def __init__(self, matriz_mapa, k_fuego):
        # Guardamos la matriz original del mapa
        self.mapa = matriz_mapa
        
        # Dimensiones del mapa (filas y columnas)
        self.filas = len(matriz_mapa)
        self.columnas = len(matriz_mapa[0])
        
       
      
        self.densidad_personas = {}
        
        
        self.k_fuego = k_fuego # Cada cuántos turnos se propaga el fuego
        self.turno_actual = 0
    
    def registrar_posiciones_agentes(self, lista_posiciones):
        """
        Actualiza el diccionario de densidad en cada turno para saber 
        dónde están los cuellos de botella.
        """
        self.densidad_personas = {}
        for (x, y) in lista_posiciones:
            if (x, y) not in self.densidad_personas:
                self.densidad_personas[(x, y)] = 0
            self.densidad_personas[(x, y)] += 1

    def calcular_costo_casilla(self, x, y):
        """
        Calcula cuánto cuesta entrar a una casilla.
        Aplica penalización si hay muchas personas (saturación de vías).
        """
        costo_base = 1
        
        # Si no hay nadie, el costo es simplemente 1
        ocupantes = self.densidad_personas.get((x, y), 0)
        
        # Decisión de diseño: Penalización cuadrática.
        # Mientras más personas, el costo sube drásticamente.
        costo_total = costo_base + (ocupantes ** 2) 
        
        return costo_total

    def propagar_fuego(self):
        """
        Propaga el fuego a las casillas adyacentes cada 'k' turnos.
        """
        self.turno_actual += 1
        
        # Solo se propaga si el turno actual es múltiplo de k_fuego
        if self.turno_actual % self.k_fuego != 0:
            return # No toca propagar el fuego en este turno
            
        nuevos_fuegos = []
        # Recorremos el mapa buscando el fuego actual
        for x in range(self.filas):
            for y in range(self.columnas):
                if self.mapa[x][y] == 3: # Si hay fuego aquí
                    # Revisamos las 4 casillas ortogonales (arriba, abajo, izq, der)
                    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for mx, my in movimientos:
                        nx, ny = x + mx, y + my
                        # Si la casilla adyacente está dentro del mapa y es un pasillo libre (0)
                        if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                            if self.mapa[nx][ny] == 0: 
                                nuevos_fuegos.append((nx, ny))
                                
        # Convertimos las nuevas casillas en fuego de manera irreversible
        for nx, ny in nuevos_fuegos:
            self.mapa[nx][ny] = 3