import os
import glob
import pandas as pd

def procesar_todo():
    # 1. Leer y consolidar archivos de la carpeta data/
    archivos_csv = glob.glob("data/*.csv")
    if not archivos_csv:
        print("No se encontraron archivos CSV en la carpeta 'data/'.")
        return

    lista_informes = [pd.read_csv(f, encoding="utf-8") for f in archivos_csv]
    df_consolidado = pd.concat(lista_informes, ignore_index=True).drop_duplicates()

    # 2. Log de automatización (con encoding="utf-8")
    os.makedirs("resultados", exist_ok=True)
    with open("resultados/log_automatizacion.txt", "a", encoding="utf-8") as f:
        f.write(f"Proceso ejecutado: {pd.Timestamp.now()}\n")

    # 3. Banner visual
    total_ventas = df_consolidado['precio_unitario'].sum()
    print("=" * 40)
    print("  NUEVO REPORTE PROCESADO EXITOSAMENTE")
    print(f"  Total ventas acumuladas: ${total_ventas:,.0f}")
    print("=" * 40)
    
    # 4. Cálculo de Métricas (Base + Nuevas)
    categoria_top = df_consolidado.groupby('categoria')['precio_unitario'].sum().idxmax()
    vendedor_top = df_consolidado.groupby('vendedor')['precio_unitario'].sum().idxmax()
    
    # Métrica nueva 1: Producto más vendido
    producto_top = df_consolidado['producto'].value_counts().idxmax()
    
    # Métrica nueva 2: Promedio por transacción
    promedio_transaccion = df_consolidado['precio_unitario'].mean()
    
    # 5. Guardar Resumen Ejecutivo (con encoding="utf-8")
    with open("resultados/resumen_ejecutivo.txt", "w", encoding="utf-8") as f:
        f.write("RESUMEN EJECUTIVO - Bot de Ventas\n")
        f.write(f"Fecha: {pd.Timestamp.now()}\n\n")
        f.write(f"Categoria con mejor desempeño: {categoria_top}\n")
        f.write(f"Vendedor con mas ventas: {vendedor_top}\n")
        f.write(f"Producto mas vendido: {producto_top}\n")
        f.write(f"Promedio de venta por transaccion: ${promedio_transaccion:,.2f}\n")
        f.write(f"Total de ventas acumuladas: ${total_ventas:,.0f}\n")

    print("Proceso completado - archivos actualizados en resultados/")

if __name__ == "__main__":
    procesar_todo()