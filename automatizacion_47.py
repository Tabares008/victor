# ============================================
# AUTOMATIZACIÓN - Bot de Ventas
# Este script vigila la carpeta de datos y cuando detecta 
# un archivo nuevo, procesa todo automáticamente:
# lee, consolida, limpia, analiza y guarda un registro del proceso
# ============================================
import time
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

ruta_datos = "data/"
archivos_vistos = set(os.listdir(ruta_datos))


def procesar_todo(archivo_nuevo):
    """
    Lee todos los archivos de sucursales, los consolida, 
    limpia duplicados, genera un gráfico de ventas por categoría,
    y guarda un registro (log) de que se hizo el proceso.
    """
    archivos_csv = glob.glob("data/sucursal_*.csv")
    archivos_xlsx = glob.glob("data/sucursal_*.xlsx")
    lista_informes = []
    
    for archivo in archivos_csv:
        lista_informes.append(pd.read_csv(archivo))
    for archivo in archivos_xlsx:
        lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))
    
    df_consolidado = pd.concat(lista_informes, ignore_index=True)
    df_consolidado = df_consolidado.drop_duplicates()
    df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)
    
    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales (COP)')
    plt.tight_layout()
    plt.savefig("resultados/grafico_categoria.png")
    plt.close()
    
    with open("resultados/log_automatizacion.txt", "a") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")
        f.write(f"Archivo detectado: {archivo_nuevo}\n")
        f.write(f"Total de registros procesados: {len(df_consolidado)}\n")
        f.write("---\n")
    
    print("Proceso completado - archivos actualizados en resultados/")


print("Monitoreando carpeta de datos... (Ctrl+C para detener)")
while True:
    archivos_actuales = set(os.listdir(ruta_datos))
    archivos_nuevos = archivos_actuales - archivos_vistos
    
    if archivos_nuevos:
        print(f"Nuevo archivo detectado: {archivos_nuevos}")
        procesar_todo(archivos_nuevos)
        archivos_vistos = archivos_actuales
    
    time.sleep(5)
