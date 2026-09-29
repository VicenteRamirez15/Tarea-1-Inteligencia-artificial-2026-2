class Agente:
    def __init__(self, id_agente, x_inicial, y_inicial):
        """
        Inicializa un agente en una posición de inicio.
        """
        self.id = id_agente
        self.x = x_inicial
        self.y = y_inicial
        
        # Estados posibles
        self.estado = 'evacuando'
        
        # Aquí guardaremos la lista de coordenadas que el algoritmo de búsqueda le asigne
        self.ruta_planeada = []
        
        # Métrica de tiempo: cantidad de turnos que toma el agente
        self.turnos_activos = 0

    def asignar_ruta(self, nueva_ruta):
        """
        Guarda la ruta calculada por el algoritmo de búsqueda utilizado
        """
        self.ruta_planeada = nueva_ruta

    def mover(self, entorno):
        """
        Ejecuta el siguiente paso del agente basado en su ruta planeada.
        """
        # Si ya escapó o fue consumido por el fuego, ya no hace acciones
        if self.estado != 'evacuando':
            return
            
        self.turnos_activos += 1
        
        # 1. Verificar si el fuego lo alcanzó en su casilla actual antes de moverse
        if entorno.mapa[self.x][self.y] == 3:
            self.estado = 'muerto'
            return
            
        # 2. Si tiene una ruta planeada, intenta dar el siguiente paso
        if len(self.ruta_planeada) > 0:
            siguiente_x, siguiente_y = self.ruta_planeada[0]
            
            # Verificamos si la siguiente casilla fue consumida por el fuego (dinamismo)
            if entorno.mapa[siguiente_x][siguiente_y] == 3:
               
                self.ruta_planeada = []
                return # Termina su turno aquí (esperando)
            
            # Si el camino está libre de fuego, ejecuta el movimiento
            self.x = siguiente_x
            self.y = siguiente_y
            self.ruta_planeada.pop(0) # Eliminamos el paso que acabamos de dar
            
        # 3. Verificar si llegó a la salida de evacuación (meta)
        if entorno.mapa[self.x][self.y] == 2:
            self.estado = 'salvado'

    def necesita_replanificar(self):
        """
        Retorna True si el agente no tiene ruta y sigue evacuando.
        """
        return len(self.ruta_planeada) == 0 and self.estado == 'evacuando'