import csv
import random
import statistics
import copy
from entorno import Entorno
from agente import Agente
from busqueda_no_informada import bfs_escape, dfs_escape
from busqueda_informada import a_star_escape, greedy_escape
from algoritmo_genetico import genetico_escape

# Definición de los 3 mapas requeridos por el enunciado
# 0: Libre, 1: Muro, 2: Salida

# Mapa 1: Cuello de botella mediano (15x15) - Todos deben pasar por un pasillo central estrecho
MAPA_1 = [[1 if (j == 7 and i not in [7, 8]) else 0 for j in range(15)] for i in range(15)]
for i in range(15): MAPA_1[0][i] = MAPA_1[14][i] = MAPA_1[i][0] = MAPA_1[i][14] = 1 # Bordes
MAPA_1[7][14] = 2 # Salida

# Mapa 2: Laberinto corporativo mediano (15x15) - Habitaciones y cruces
MAPA_2 = [[0 for _ in range(15)] for _ in range(15)]
for i in range(15): MAPA_2[0][i] = MAPA_2[14][i] = MAPA_2[i][0] = MAPA_2[i][14] = 1
for i in range(2, 13, 3):
    for j in range(2, 13):
        if j % 4 != 0: MAPA_2[i][j] = 1
MAPA_2[1][13] = 2 # Salida

# Mapa 3: Dispersión abierta mediana (15x15) - Pocos obstáculos aislados
MAPA_3 = [[0 for _ in range(15)] for _ in range(15)]
for i in range(15): MAPA_3[0][i] = MAPA_3[14][i] = MAPA_3[i][0] = MAPA_3[i][14] = 1
obstaculos = [(3,4), (3,5), (8,8), (9,8), (11,3), (11,11), (5,10)]
for ox, oy in obstaculos: MAPA_3[ox][oy] = 1
MAPA_3[13][13] = 2 # Salida

def inyectar_estocasticidad(mapa_base, num_fuegos, num_agentes):
    """
    Toma un mapa y de forma aleatoria posiciona focos de fuego (3) 
    y retorna la lista de agentes inicializados en espacios libres (0).
    """
    mapa = copy.deepcopy(mapa_base)
    filas, columnas = len(mapa), len(mapa[0])
    
    # 1. Posicionar fuego inicial al azar
    fuegos_colocados = 0
    while fuegos_colocados < num_fuegos:
        x, y = random.randint(0, filas - 1), random.randint(0, columnas - 1)
        if mapa[x][y] == 0:
            mapa[x][y] = 3
            fuegos_colocados += 1
            
    # 2. Posicionar agentes al azar
    agentes = []
    agentes_colocados = 0
    while agentes_colocados < num_agentes:
        x, y = random.randint(0, filas - 1), random.randint(0, columnas - 1)
        if mapa[x][y] == 0:
            agentes.append(Agente(id_agente=agentes_colocados+1, x_inicial=x, y_inicial=y))
            agentes_colocados += 1
            
    return mapa, agentes

def ejecutar_simulacion(mapa_base, algoritmo_func, k_fuego=3, num_fuegos=1, num_agentes=3):
    """
    Ejecuta una iteración completa hasta que no queden agentes evacuando.
    """
    mapa_estocastico, agentes = inyectar_estocasticidad(mapa_base, num_fuegos, num_agentes)
    entorno = Entorno(mapa_estocastico, k_fuego)
    
    while any(ag.estado == 'evacuando' for ag in agentes):
        posiciones = [(ag.x, ag.y) for ag in agentes if ag.estado == 'evacuando']
        entorno.registrar_posiciones_agentes(posiciones)
        
        for ag in agentes:
            if ag.necesita_replanificar():
                nueva_ruta = algoritmo_func(entorno, ag.x, ag.y)
                ag.asignar_ruta(nueva_ruta)
            ag.mover(entorno)
            
        entorno.propagar_fuego()
        
    sobrevivientes = [ag for ag in agentes if ag.estado == 'salvado']
    tiempo_ultimo = max([ag.turnos_activos for ag in sobrevivientes]) if sobrevivientes else 0
    
    return len(sobrevivientes), tiempo_ultimo, len(agentes)

def main():
    iteraciones = 200
    
    mapas = {
        "Mapa 1 (Alta densidad)": MAPA_1,
        "Mapa 2 (Laberinto)": MAPA_2,
        "Mapa 3 (Abierto)": MAPA_3
    }
    
    algoritmos = {
        "BFS": bfs_escape,
        "DFS": dfs_escape,
        "A*": a_star_escape,
        "Greedy": greedy_escape,
        "Genetico": genetico_escape
    }
    
    # Nombre del archivo de salida (Cámbialo en cada script: mediano, grande, etc.)
    nombre_archivo_csv = 'resultadosb2.csv'
    
    # Lista para guardar los datos de las filas
    datos_csv = []
    
    print("Iniciando Benchmarking...")
    
    for nombre_mapa, mapa in mapas.items():
        print(f"\n{'='*50}\nEvaluando {nombre_mapa}\n{'='*50}")
        
        for nombre_algo, func_algo in algoritmos.items():
            tiempos = []
            total_sobrevivientes = 0
            total_agentes_simulados = 0
            
            for i in range(iteraciones):
                # OJO: Asegúrate de que los parámetros aquí coincidan con el tamaño (pequeño, mediano o grande)
                sobrevivientes, tiempo_ultimo, num_agentes = ejecutar_simulacion(mapa, func_algo, num_fuegos=3, num_agentes=15)
                
                total_sobrevivientes += sobrevivientes
                total_agentes_simulados += num_agentes
                if tiempo_ultimo > 0:
                    tiempos.append(tiempo_ultimo)
                    
            tasa_supervivencia = (total_sobrevivientes / total_agentes_simulados) * 100
            
            print(f"\nAlgoritmo: {nombre_algo}")
            print(f"- Tasa de supervivencia: {tasa_supervivencia:.2f}%")
            
            if tiempos:
                media = statistics.mean(tiempos)
                desv_est = statistics.stdev(tiempos) if len(tiempos) > 1 else 0
                val_min = min(tiempos)
                val_max = max(tiempos)
                print(f"- Tiempo -> Media: {media:.2f} | Desv. Est: {desv_est:.2f} | Mín: {val_min} | Máx: {val_max}")
                
                # Guardar fila con datos exitosos
                datos_csv.append([nombre_mapa, nombre_algo, round(tasa_supervivencia, 2), round(media, 2), round(desv_est, 2), val_min, val_max])
            else:
                print("- Tiempo -> N/A (Ningún sobreviviente)")
                # Guardar fila con datos fallidos
                datos_csv.append([nombre_mapa, nombre_algo, round(tasa_supervivencia, 2), "N/A", "N/A", "N/A", "N/A"])

    # Escribir todo al archivo CSV
    with open(nombre_archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        # Escribir la cabecera
        escritor.writerow(["Mapa", "Algoritmo", "Supervivencia (%)", "Media Turnos", "Desv Est Turnos", "Min Turnos", "Max Turnos"])
        # Escribir los datos
        escritor.writerows(datos_csv)
        
    

if __name__ == "__main__":
    main()