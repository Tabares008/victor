import glob
import os
import matplotlib.pyplot as plt
import pandas as pd


def procesar_todo():
  # PASO 2: Lectura de CSV y XLSX en datos/
  archivos_csv = glob.glob('datos/sucursal_*.csv')
  archivos_xlsx = glob.glob('datos/sucursal_*.xlsx')

  lista_informes = []

  for archivo in archivos_csv:
    lista_informes.append(pd.read_csv(archivo, encoding='utf-8'))

  for archivo in archivos_xlsx:
    lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))

  if not lista_informes:
    print("No se encontraron archivos en la carpeta 'datos/'.")
    return

  # Consolidación y limpieza
  df_consolidado = pd.concat(lista_informes, ignore_index=True)
  df_consolidado = df_consolidado.drop_duplicates()

  os.makedirs('resultados', exist_ok=True)

  # Guardar Excel consolidado
  df_consolidado.to_excel('resultados/consolidado_limpio.xlsx', index=False)

  # Gráfico 1: Ventas por Categoría
  ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
  plt.figure(figsize=(8, 5))
  ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
  plt.ticklabel_format(style='plain', axis='y')
  plt.ylabel('Ventas totales (COP)')
  plt.tight_layout()
  plt.savefig('resultados/grafico_categoria.png')
  plt.close()

  # Gráfico 2: Ventas por Vendedor
  ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
  plt.figure(figsize=(8, 5))
  ventas_vendedor.plot(kind='bar', color='orange', title='Ventas por Vendedor')
  plt.ticklabel_format(style='plain', axis='y')
  plt.ylabel('Ventas totales (COP)')
  plt.tight_layout()
  plt.savefig('resultados/grafico_vendedor.png')
  plt.close()

  # PASO 4: Análisis de métricas (Producto más vendido)
  total_ventas = df_consolidado['precio_unitario'].sum()
  categoria_top = (
      df_consolidado.groupby('categoria')['precio_unitario'].sum().idxmax()
  )
  vendedor_top = (
      df_consolidado.groupby('vendedor')['precio_unitario'].sum().idxmax()
  )
  producto_top = df_consolidado['producto'].value_counts().idxmax()
  promedio_transaccion = df_consolidado['precio_unitario'].mean()

  print('=' * 40)
  print('  PROCESAMIENTO COMPLETADO')
  print(f'  Total Ventas: ${total_ventas:,.0f}')
  print(f'  Producto más vendido: {producto_top}')
  print('=' * 40)

  # Guardar Resumen Ejecutivo
  with open('resultados/resumen_ejecutivo.txt', 'w', encoding='utf-8') as f:
    f.write('RESUMEN EJECUTIVO - BOT DE VENTAS\n')
    f.write(f'Fecha: {pd.Timestamp.now()}\n\n')
    f.write(f'Categoría con mejor desempeño: {categoria_top}\n')
    f.write(f'Vendedor con más ventas: {vendedor_top}\n')
    f.write(f'Producto más vendido: {producto_top}\n')
    f.write(
        f'Promedio de venta por transacción: ${promedio_transaccion:,.2f}\n'
    )
    f.write(f'Total de ventas acumuladas: ${total_ventas:,.0f}\n')


if __name__ == '__main__':
  procesar_todo()