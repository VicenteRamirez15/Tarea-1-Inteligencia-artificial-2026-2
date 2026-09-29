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

def crear_mapa_30x30_tipo(tipo):
    mapa = [[0 for _ in range(30)] for _ in range(30)]
    # Bordes
    for i in range(30): mapa[0][i] = mapa[29][i] = mapa[i][0] = mapa[i][29] = 1

    if tipo == "cuello_botella":
        # Dos grandes muros que dejan solo un pasillo central de 2 bloques
        for i in range(1, 29):
            if i not in [14, 15]: mapa[i][20] = 1
        mapa[14][29] = 2 # Salida

    elif tipo == "laberinto":
        for i in range(2, 28, 4):
            for j in range(2, 28):
                if j % 5 != 0: mapa[i][j] = 1
                if i % 3 == 0: mapa[j][i] = 1
        mapa[1][28] = 2 # Salida

    elif tipo == "abierto":
        # Obstáculos dispersos al azar (con semilla fija para que sea reproducible)
        import random
        random.seed(42)
        for _ in range(80):
            mapa[random.randint(2, 27)][random.randint(2, 27)] = 1
        mapa[28][28] = 2 # Salida

    return mapa

MAPA_1 = crear_mapa_30x30_tipo("cuello_botella")
MAPA_2 = crear_mapa_30x30_tipo("laberinto")
MAPA_3 = crear_mapa_30x30_tipo("abierto")

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
    nombre_archivo_csv = 'resultadosb3.csv'
    
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
                sobrevivientes, tiempo_ultimo, num_agentes = ejecutar_simulacion(mapa, func_algo, num_fuegos=6, num_agentes=40)
                
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