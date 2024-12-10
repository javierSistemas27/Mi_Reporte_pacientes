import pandas as pd
import chardet

def extract_from_csv(file):
    try:
        # Detectar la codificación del archivo
        with open(file, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']

        # Leer el archivo CSV con la codificación detectada
        dataframe = pd.read_csv(file, encoding=encoding)
        return dataframe

    except FileNotFoundError:
        print(f"Error: El archivo {file} no fue encontrado.")
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo {file} está vacío.")
    except pd.errors.ParserError:
        print(f"Error: Error al analizar el archivo {file}. Por favor, verifica el formato.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

def guardar_como_csv(dataframe, archivo_salida):
    try:
        dataframe.to_csv(archivo_salida, index=False)
        print(f'Archivo guardado como {archivo_salida}')
    except Exception as e:
        print(f"Se produjo un error al guardar el archivo: {e}")

# Uso de la función
file_path = 'atenciones.csv'
dataframe = extract_from_csv(file_path)

# Guardar el DataFrame como un nuevo archivo CSV
if dataframe is not None:
    archivo_salida = 'atenciones_guardado.csv'
    guardar_como_csv(dataframe, archivo_salida)
    print('Nombre de las columnas: \n', dataframe.columns.tolist())
    print(dataframe.head())  # Comprobación del contenido
