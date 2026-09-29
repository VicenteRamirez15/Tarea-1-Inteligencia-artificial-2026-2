import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_graficos(archivo_csv):
    # Validar si el archivo existe antes de intentar leerlo
    if not os.path.exists(archivo_csv):
        print(f"Saltando '{archivo_csv}': El archivo no existe o aún no se ha generado.")
        return

    print(f"Generando gráficos para {archivo_csv}...")
    df = pd.read_csv(archivo_csv)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # 1. Gráfico de Tasa de Supervivencia
    pivot_supervivencia = df.pivot(index='Mapa', columns='Algoritmo', values='Supervivencia (%)')
    pivot_supervivencia.plot(kind='bar', ax=ax1, colormap='viridis', edgecolor='black')
    ax1.set_title('Tasa de Supervivencia por Mapa y Algoritmo', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Supervivencia (%)', fontsize=12)
    ax1.set_xlabel('Topología del Entorno', fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.tick_params(axis='x', rotation=15)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 2. Gráfico de Media de Turnos
    # Manejar los casos de "N/A" convirtiéndolos a numérico, los errores se vuelven NaN
    df['Media Turnos'] = pd.to_numeric(df['Media Turnos'], errors='coerce')
    pivot_turnos = df.pivot(index='Mapa', columns='Algoritmo', values='Media Turnos')
    pivot_turnos.plot(kind='bar', ax=ax2, colormap='plasma', edgecolor='black')
    ax2.set_title('Tiempo Medio de Evacuación (Turnos)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Media de Turnos', fontsize=12)
    ax2.set_xlabel('Topología del Entorno', fontsize=12)
    ax2.tick_params(axis='x', rotation=15)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    nombre_imagen = archivo_csv.replace('.csv', '.png')
    plt.savefig(nombre_imagen, dpi=300)
    print(f"Gráfico guardado exitosamente como: {nombre_imagen}\n")
    
    # Cerramos la figura para liberar memoria antes de la siguiente iteración
    plt.close()

if __name__ == "__main__":
    # Lista de los tres archivos que generaste
    archivos = ['resultadosb1.csv', 'resultadosb2.csv', 'resultadosb3.csv']
    
    for archivo in archivos:
        generar_graficos(archivo)
        