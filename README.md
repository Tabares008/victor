# Sistema de Automatización de Ventas por Sucursal

## ¿Qué hace el sistema?

Este proyecto implementa un **bot de automatización** que vigila continuamente la carpeta `data/` en busca de nuevos archivos de ventas de sucursales. Cada vez que se agrega un archivo nuevo (por ejemplo, un reporte CSV o XLSX de una sucursal), el sistema ejecuta automáticamente todo el flujo de procesamiento de datos:

1. **Consolidación**: Lee todos los archivos `sucursal_*.csv` y `sucursal_*.xlsx` de la carpeta `data/` y los une en un solo DataFrame.
2. **Limpieza**: Elimina registros duplicados con `drop_duplicates()` para garantizar datos únicos.
3. **Exportación**: Guarda el archivo consolidado y limpio en `resultados/consolidado_limpio.xlsx`.
4. **Visualización**: Genera un gráfico de barras de ventas totales por categoría y lo guarda como imagen en `resultados/grafico_categoria.png`.
5. **Registro (Log)**: Registra la fecha/hora de ejecución, el nombre del archivo detectado y el total de registros procesados en `resultados/log_automatizacion.txt`.

## ¿Cómo detecta los archivos nuevos?

El script `automatizacion_47.py` utiliza un **bucle infinito de monitoreo** basado en comparación de conjuntos (sets) de nombres de archivo:

- Al iniciar, el script captura un **conjunto (set) con los nombres de todos los archivos** que ya existen en la carpeta `data/`. Esto se guarda en la variable `archivos_vistos`.
- Dentro del bucle `while True`, cada **5 segundos** (usando `time.sleep(5)`) el script vuelve a listar los archivos de `data/` y los guarda en `archivos_actuales`.
- Usando la operación de **diferencia de conjuntos** (`archivos_actuales - archivos_vistos`), el script identifica si hay archivos que no existían antes.
- Si la diferencia no está vacía, significa que **se detectó uno o más archivos nuevos**, y el script ejecuta la función `procesar_todo()` con la información del archivo detectado.
- Después de procesar, actualiza `archivos_vistos` con la lista actual para no volver a procesar los mismos archivos.

## Flujo de ejecución al detectar un archivo nuevo

```
Archivo nuevo detectado en data/
        │
        ▼
Leer todos los sucursal_*.csv y sucursal_*.xlsx
        │
        ▼
Concatenar en un solo DataFrame (pd.concat)
        │
        ▼
Eliminar duplicados (drop_duplicates)
        │
        ▼
Guardar consolidado → resultados/consolidado_limpio.xlsx
        │
        ▼
Generar gráfico de ventas por categoría → resultados/grafico_categoria.png
        │
        ▼
Registrar en log → resultados/log_automatizacion.txt
```

## Estructura del proyecto

```
victor/
├── automatizacion_47.py        # Script de monitoreo y procesamiento
├── data/                       # Carpeta vigilada (archivos de sucursales)
│   ├── sucursal_medellin.csv
│   ├── sucursal_cali.csv
│   ├── sucursal_barranquilla.xlsx
│   └── sucursal_bogota.xlsx
├── resultados/                 # Salidas generadas automáticamente
│   ├── consolidado_limpio.xlsx
│   ├── grafico_categoria.png
│   └── log_automatizacion.txt
└── README.md
```

## Cómo usar

1. Instalar dependencias: `pip install pandas openpyxl matplotlib`
2. Ejecutar el script: `python automatizacion_47.py`
3. Copiar o mover archivos de sucursales a la carpeta `data/`
4. El sistema procesará automáticamente y generará los resultados
