import pandas as pd
"""
SELECCIONAR COLUMNAS PARA MI ANALISIS
"""
def seleccionar_columnas(df, columnas):
    df_seleccionado = df[columnas]
    return df_seleccionado

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Num. Doc.', 'Ap. Paterno', 'Ap. Materno', 'Primer Nombre', 'Otros Nombres', 'Fec. Nac', 'Edad', 'Sexo', 'ID Servicio', ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 'Destino Asegurado','Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']
file_path = 'atenciones_guardado.csv'
df = pd.read_csv(file_path)
df_seleccionado = seleccionar_columnas(df, columnas_personalizadas)

"""
CONCATENAR COLUMNAS
"""
def concatenar_y_excluir(df, paterno, materno, primer_nombre, segundo_nombre, nueva_columna, separador=' '):
    # Concatenar las columnas especificadas en la nueva columna
    df[nueva_columna] = df[[paterno, materno, primer_nombre, segundo_nombre]].apply(lambda row: separador.join(row.values.astype(str)), axis=1)
    
    # Excluir las columnas originales
    df_resultante = df.drop(columns=[paterno, materno, primer_nombre, segundo_nombre])
    
    # Reordenar las columnas para insertar 'Beneficiario' después de 'Tipo Doc.'
    cols = df_resultante.columns.tolist()
    index = cols.index('Tipo Doc.') + 2  # Asegúrate de que el nombre de la columna es exacto
    cols.insert(index, nueva_columna)
    df_resultante = df_resultante[cols]
    
    return df_resultante

# Crear DataFrame de ejemplo (aquí df_seleccionado debería ser tu DataFrame ya preseleccionado)
df = pd.DataFrame(df_seleccionado)

paterno = 'Ap. Paterno'
materno = 'Ap. Materno'
primer_nombre = 'Primer Nombre'
segundo_nombre = 'Otros Nombres'
nueva_columna = 'Beneficiario'

# Concatenar las columnas y excluir las originales
df_concatenado = concatenar_y_excluir(df, paterno, materno, primer_nombre, segundo_nombre, nueva_columna)

"""
ELIMINAR COLUMNA BENEFICIARIO
"""
def seleccionar_columnas(df, columnas):
    df_seleccionado = df[columnas]
    return df_seleccionado

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 'Num. Doc.', 'Fec. Nac', 'Edad', 'Sexo', 'ID Servicio', ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 'Destino Asegurado', 'Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']
df = pd.DataFrame(df_concatenado)
df_col_delete = seleccionar_columnas(df, columnas_personalizadas)

"""
CALCULAR EDAD DEL PACIENTE AÑOS MESES Y DIAS
"""
from datetime import datetime

def calcular_edad(fecha_nac, fecha_atencion):
    fecha_nac = datetime.strptime(fecha_nac, '%d/%m/%Y')
    fecha_atencion = datetime.strptime(fecha_atencion, '%d/%m/%Y %H:%M')
    
    años = fecha_atencion.year - fecha_nac.year
    meses = fecha_atencion.month - fecha_nac.month
    días = fecha_atencion.day - fecha_nac.day

    if días < 0:
        meses -= 1
        días += (fecha_atencion.replace(month=fecha_atencion.month) - fecha_nac.replace(month=fecha_nac.month, day=1)).days

    if meses < 0:
        meses += 12
        años -= 1

    return f"{años} años {meses} meses {días} días"

def agregar_columna_edad(df, col_fecha_nac, col_fecha_atencion, col_edad):
    df[col_edad] = df.apply(lambda row: calcular_edad(row[col_fecha_nac], row[col_fecha_atencion]), axis=1)
    return df

# Crear el DataFrame
df = pd.DataFrame(df_col_delete)

# Agregar la columna de edad
df_cal_edad = agregar_columna_edad(df, 'Fec. Nac', 'Fecha Atencion', 'Edad Paciente')

# Reordenar las columnas para colocar 'Edad_personal' junto a 'Edad'
columnas_ordenadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 'Num. Doc.', 'Fec. Nac', 'Edad', 'Edad Paciente','Sexo', 'ID Servicio', ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 'Destino Asegurado', 'Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']

df_cal_edad_final = df[columnas_ordenadas]
# print(df_cal_edad_final)
"""
ELIMINAR COLUMNA DUPLICADA
"""
def seleccionar_columnas(df, columnas):
    # Verificar y seleccionar solo columnas existentes
    columnas_existentes = [col for col in columnas if col in df.columns]
    df_seleccionado = df[columnas_existentes]
    
    # Eliminar columnas duplicadas
    df_seleccionado = df_seleccionado.loc[:, ~df_seleccionado.columns.duplicated()]
    
    return df_seleccionado

def extraer_columnas(df):
    columnas = df.columns.tolist()
    return columnas

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 'Num. Doc.', 'Fec. Nac', 'Edad', 'Edad Paciente','Sexo', 'ID Servicio', ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 'Destino Asegurado', 'Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']

# Supongo que df_concatenado es un DataFrame ya existente
df = pd.DataFrame(df_concatenado)

# Seleccionar columnas existentes y eliminar duplicados
df_col_delete_final = seleccionar_columnas(df, columnas_personalizadas)

# Uso de la función para extraer los nombres de las columnas
nombres_columnas = extraer_columnas(df_col_delete_final)

# Imprimir el DataFrame resultante y los nombres de las columnas
# print('DataFrame con columnas seleccionadas y sin duplicados:')
# print(df_col_delete_final)
# print('Nombres de las columnas:', nombres_columnas)


# Guardar el DataFrame en un archivo CSV 
def guardar_como_csv(dataframe, archivo_salida):
    try:
        dataframe.to_csv(archivo_salida, index=False)
        print(f'Archivo guardado como {archivo_salida}')
    except Exception as e:
        print(f"Se produjo un error al guardar el archivo: {e}")

# Uso de la función
dataframe = pd.DataFrame(df_col_delete_final)

# Guardar el DataFrame como un nuevo archivo CSV
if dataframe is not None:
    archivo_salida = 'atenciones_transfomados.csv'
    guardar_como_csv(dataframe, archivo_salida)
    print('Nombre de las columnas: \n', dataframe.columns.tolist())
    print(dataframe.head())  # Comprobación del contenido
