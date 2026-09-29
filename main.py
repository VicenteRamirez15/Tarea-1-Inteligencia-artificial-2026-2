import time
from entorno import Entorno
from agente import Agente
from busqueda_informada import a_star_escape
from benchmark3 import crear_mapa_30x30_tipo

def imprimir_mapa(entorno, agentes):
    mapa_visual = [fila[:] for fila in entorno.mapa]
    
    for ag in agentes:
        if ag.estado == 'evacuando':
            mapa_visual[ag.x][ag.y] = 'A'
            
    print(f"\n--- Turno {entorno.turno_actual} ---")
    for fila in mapa_visual:
        fila_str = []
        for celda in fila:
            if celda == 0: fila_str.append('.')
            elif celda == 1: fila_str.append('█')
            elif celda == 2: fila_str.append('S')
            elif celda == 3: fila_str.append('F')
            else: fila_str.append(str(celda))
        print(" ".join(fila_str))
    print("-" * 30)

def main():
    print("Seleccione el escenario a visualizar:")
    print("1. Pequeño (6x9, 3 agentes)")
    print("2. Mediano (15x15, 15 agentes)")
    print("3. Grande (30x30, 40 agentes)")
    opcion = input("Ingrese 1, 2 o 3: ")

    if opcion == "1":
        mapa = [
            [1, 1, 1, 1, 1, 1, 1, 2, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
        num_fuegos, num_agentes = 1, 3
        
    elif opcion == "2":
        mapa = [[1 if (j == 7 and i not in [7, 8]) else 0 for j in range(15)] for i in range(15)]
        for i in range(15): mapa[0][i] = mapa[14][i] = mapa[i][0] = mapa[i][14] = 1 
        mapa[7][14] = 2
        num_fuegos, num_agentes = 3, 15
        
    else:
        mapa = crear_mapa_30x30_tipo("cuello_botella")
        num_fuegos, num_agentes = 6, 40

    from benchmark3 import inyectar_estocasticidad 
    mapa_estocastico, agentes = inyectar_estocasticidad(mapa, num_fuegos, num_agentes)
    entorno = Entorno(mapa_estocastico, k_fuego=3)

    while any(ag.estado == 'evacuando' for ag in agentes):
        imprimir_mapa(entorno, agentes)
        
        posiciones = [(ag.x, ag.y) for ag in agentes if ag.estado == 'evacuando']
        entorno.registrar_posiciones_agentes(posiciones)
        
        for ag in agentes:
            if ag.necesita_replanificar():
                nueva_ruta = a_star_escape(entorno, ag.x, ag.y)
                ag.asignar_ruta(nueva_ruta)
            ag.mover(entorno)
            
        entorno.propagar_fuego()
        time.sleep(0.3)

    print("Simulación terminada.")

if __name__ == "__main__":
    main()