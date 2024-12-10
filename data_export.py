import pandas as pd

# Ruta del archivo CSV ordenado
archivo_csv_ordenado = 'atenciones_transfomados.csv'

try:
    # Leer el archivo CSV ordenado
    data_ordenada = pd.read_csv(archivo_csv_ordenado)
    
    # Exportar a Excel
    archivo_excel = 'atenciones_ordenadas.xlsx'
    data_ordenada.to_excel(archivo_excel, index=False)
    
    print(f"Datos exportados exitosamente a {archivo_excel}")
except Exception as e:
    print(f"Error al exportar los datos: {e}")