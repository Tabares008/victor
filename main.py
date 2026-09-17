import glob
import os
import matplotlib.pyplot as plt
import pandas as pd


def procesar_todo():
  # PARTE 1: Buscar y leer los archivos en datos/
  archivos_csv = glob.glob('datos/sucursal_*.csv')
  archivos_xlsx = glob.glob('datos/sucursal_*.xlsx')

  lista_informes = []

  # Carga de archivos CSV (comentario IA: lee cada reporte y lo añade a la lista)
  for archivo in archivos_csv:
    df = pd.read_csv(archivo, encoding='utf-8')
    lista_informes.append(df)

  # Carga de archivos Excel (comentario IA: lee reportes .xlsx)
  for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)

  if not lista_informes:
    print("No se encontraron archivos en la carpeta 'datos/'.")
    return

  # PARTE 3: Aplicación directa del template.py
  # Identificamos el archivo con columnas distintas mediante su columna única
  for i, df in enumerate(lista_informes):
    if 'vendedor_nombre' in df.columns or 'valor_unitario' in df.columns:
      lista_informes[i] = df.rename(
          columns={
              'vendedor_nombre': 'vendedor',
              'valor_unitario': 'precio_unitario',
          }
      )

  # Consolidación final (7 columnas exactas)
  df_consolidado = pd.concat(lista_informes, ignore_index=True)

  # PARTE 4: Limpieza de duplicados y valores nulos
  df_consolidado = df_consolidado.drop_duplicates()
  df_consolidado['vendedor'] = df_consolidado['vendedor'].fillna('Desconocido')
  df_consolidado['precio_unitario'] = df_consolidado['precio_unitario'].fillna(
      0
  )

  os.makedirs('resultados', exist_ok=True)

  # PARTE 5: Guardar consolidado
  df_consolidado.to_excel('resultados/consolidado_limpio.xlsx', index=False)

  # Generación de reportes y gráficos
  ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
  plt.figure(figsize=(8, 5))
  ventas_categoria.plot(kind='bar', title='Ventas por Categoría')
  plt.ticklabel_format(style='plain', axis='y')
  plt.ylabel('Ventas totales (COP)')
  plt.tight_layout()
  plt.savefig('resultados/grafico_categoria.png')
  plt.close()

  ventas_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
  plt.figure(figsize=(8, 5))
  ventas_vendedor.plot(kind='bar', color='orange', title='Ventas por Vendedor')
  plt.ticklabel_format(style='plain', axis='y')
  plt.ylabel('Ventas totales (COP)')
  plt.tight_layout()
  plt.savefig('resultados/grafico_vendedor.png')
  plt.close()

  print('Procesamiento correcto con plantilla integrada.')


if __name__ == '__main__':
  procesar_todo()