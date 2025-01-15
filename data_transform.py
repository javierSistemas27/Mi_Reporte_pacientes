import pandas as pd
"""****************************************************************************
SELECCIONAR COLUMNAS PARA MI ANALISIS
****************************************************************************"""
def seleccionar_columnas(df, columnas):
    df_seleccionado = df[columnas]
    return df_seleccionado

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Num. Doc.', 'Ap. Paterno', 
                        'Ap. Materno', 'Primer Nombre', 'Otros Nombres', 'Fec. Nac', 'Edad', 'Sexo',
                        'ID Servicio', ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 
                        'Tipo Profesional', 'Fecha Registro', 'Hora Registro', 'Lugar Atencion',
                        'Destino Asegurado','Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']
file_path = 'atenciones_guardado.csv'
df = pd.read_csv(file_path)
df_seleccionado = seleccionar_columnas(df, columnas_personalizadas)

"""****************************************************************************
CONCATENAR COLUMNAS
****************************************************************************"""
def concatenar_y_excluir(df, paterno, materno, primer_nombre, segundo_nombre, nueva_columna, separador=' '):
    # Reemplazar NaN con cadena vacía
    df[[paterno, materno, primer_nombre, segundo_nombre]] = df[[paterno, materno, primer_nombre, segundo_nombre]].fillna('')
    
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

# Crear DataFrame de ejemplo
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

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 'Num. Doc.',
                            'Fec. Nac', 'Edad', 'Sexo', 'ID Servicio', ' Servicio', 'Digitador', 
                            'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 'Fecha Registro', 
                            'Hora Registro', 'Lugar Atencion', 'Destino Asegurado', 'Gestante', 
                            'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']
df = pd.DataFrame(df_concatenado)
df_col_delete = seleccionar_columnas(df, columnas_personalizadas)

"""****************************************************************************
CALCULAR EDAD DEL PACIENTE AÑOS MESES Y DIAS
****************************************************************************"""
from datetime import datetime

def calcular_edad(fecha_nac, fecha_atencion):
    # Convertir las fechas a objetos datetime
    fecha_nac = datetime.strptime(fecha_nac, '%d/%m/%Y')
    fecha_atencion = datetime.strptime(fecha_atencion, '%d/%m/%Y %H:%M')
    
    # Calcular años, meses y días
    años = fecha_atencion.year - fecha_nac.year
    meses = fecha_atencion.month - fecha_nac.month
    días = fecha_atencion.day - fecha_nac.day

    # Ajustar si los días son negativos
    if días < 0:
        meses -= 1
        # Obtener los días del mes anterior
        mes_anterior = (fecha_atencion.month - 1) or 12
        año_anterior = fecha_atencion.year if fecha_atencion.month > 1 else fecha_atencion.year - 1
        dias_mes_anterior = (datetime(año_anterior, mes_anterior, 1) - datetime(año_anterior, mes_anterior - 1, 1)).days
        días += dias_mes_anterior

    # Ajustar si los meses son negativos
    if meses < 0:
        meses += 12
        años -= 1

    return f"{años} años {meses} meses {días} días"

def agregar_columna_edad(df, col_fecha_nac, col_fecha_atencion, col_edad):
    df[col_edad] = df.apply(lambda row: calcular_edad(row[col_fecha_nac], row[col_fecha_atencion]), axis=1)
    return df

# Crear el DataFrame
df = pd.DataFrame(df_col_delete)

# Agregar la columna Edad Paciente
df_cal_edad = agregar_columna_edad(df, 'Fec. Nac', 'Fecha Atencion', 'Edad Paciente')

# Reordenar las columnas para colocar 'Edad_personal' junto a 'Edad'
columnas_ordenadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 
                    'Num. Doc.', 'Fec. Nac', 'Edad', 'Edad Paciente','Sexo', 'ID Servicio', 
                    ' Servicio', 'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 
                    'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 'Destino Asegurado', 
                    'Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']

df_cal_edad_final = df[columnas_ordenadas]
# print(df_cal_edad_final)
"""****************************************************************************
ELIMINAR COLUMNA DUPLICADA
****************************************************************************"""
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

columnas_personalizadas = ['?FUA', 'Fecha Atencion', 'EESS', 'Tipo Doc.', 'Beneficiario', 'Num. Doc.', 
                        'Fec. Nac', 'Edad', 'Edad Paciente','Sexo', 'ID Servicio', ' Servicio', 
                        'Digitador', 'DNI Resp. Aten.', 'Profesional', 'Tipo Profesional', 
                        'Fecha Registro', 'Hora Registro', 'Lugar Atencion', 
                        'Destino Asegurado', 'Gestante', 'Nro. Cred', 'Fecha Probable Parto', 'Fecha Parto']

# Supongo que df_concatenado es un DataFrame ya existente
df = pd.DataFrame(df_cal_edad_final)

# Seleccionar columnas existentes y eliminar duplicados
df_col_delete_final = seleccionar_columnas(df, columnas_personalizadas)

# Uso de la función para extraer los nombres de las columnas
nombres_columnas = extraer_columnas(df_col_delete_final)

"""****************************************************************************
AGREGAR LA COLUMNA "NOMBRE_D" DONDE SE ALMACENA EL NOMBRE DIGITADOR DF=df_col_delete_final
****************************************************************************"""
# Crear un DataFrame de ejemplo
df = pd.DataFrame(df_col_delete_final)
# Crear un diccionario con los identificadores y los nombres de los creadores
creadores = {
    70038401: 'JAVIER',
    75101750: 'DANITZA',
    70609648: 'MAYRA'
}
# Definir una función para mapear los identificadores a los nombres de los creadores
def agregar_nombre_creador(row):
    return creadores.get(row['Digitador'], 'Desconocido')  # Devuelve 'Desconocido' si no encuentra el ID
# Agregar una nueva columna 'Creador' al DataFrame
df['Nombre_D'] = df.apply(agregar_nombre_creador, axis=1)
# Reordenar las columnas para colocar 'Creador' después de 'Registro'
columnas = df.columns.tolist()
idx = columnas.index('Digitador') + 1
columnas.insert(idx, columnas.pop(columnas.index('Nombre_D')))
df_col_dig = df[columnas]
"""****************************************************************************
FILTRO DE EDADE (1- 4 AÑOS) Y PRESTACIONES (1,2,7,8,16,19,61,75)
****************************************************************************"""
# Filtrar Pacientes con edad 0 to 4 años
def filtrar_por_Edad(df, ids):
    df_filtrado = df[df['Edad'].isin(ids)]
    return df_filtrado
# Crear un DataFrame de ejemplo
df = pd.DataFrame(df_col_dig)

# Lista de IDs para filtrar
ids_a_filtrar = [0, 1, 2, 3, 4]

# Usar la función para filtrar el DataFrame
df_filtrado = filtrar_por_Edad(df, ids_a_filtrar)

# Imprimir el DataFrame resultante
print('DataFrame filtrado por Edades específicos:')
# print(df_filtrado)

#Filtrar por prestaciones 001, 002, 007, 008, 016, 019, 061, 075
def filtrar_por_ids(df, nombres):
    df_filtrado_1 = df[df['ID Servicio'].isin(nombres)]
    return df_filtrado_1

# Crear un DataFrame de ejemplo
df = pd.DataFrame(df_filtrado)

# Lista de nombres para filtrar
ids_a_filtrar = [1,2,7,8,16,19,61,75]

# Usar la función para filtrar el DataFrame
df_filtrado_1 = filtrar_por_ids(df, ids_a_filtrar)

# Columnas personalidas
col_personal = ['?FUA', 'Fecha Atencion', 'EESS', 'Beneficiario', 'Num. Doc.', 'Fec. Nac', 'Edad',
                'Edad Paciente', 'Sexo', 'ID Servicio', 'Digitador', 'Nombre_D', 'Profesional', 
                'Tipo Profesional', 'Fecha Registro', 'Nro. Cred']
df_personalizada = df_filtrado_1[col_personal]
"""****************************************************************************
ORDENAR DATAFRAME
****************************************************************************"""
# Crear el DataFrame
df = pd.DataFrame(df_personalizada)

# Definir la función para ordenar el DataFrame
def ordenar_dataframe(df):
    # Ordenar primero por 'Nombre de Empresa' y luego por 'Nombre del Dueño'
    df_ordenado = df.sort_values(by=['EESS', 'Beneficiario'], ascending=True)
    return df_ordenado

# Llamar a la función y ordenar el DataFrame
df_ordenado_final = ordenar_dataframe(df)
"""****************************************************************************
GUARDAR EL DATAFRAME EN FORMATO CSV
****************************************************************************"""
# Guardar el DataFrame en un archivo CSV 
def guardar_como_csv(dataframe, archivo_salida):
    try:
        dataframe.to_csv(archivo_salida, index=False)
        print(f'Archivo guardado como {archivo_salida}')
    except Exception as e:
        print(f"Se produjo un error al guardar el archivo: {e}")

# Uso de la función
dataframe = pd.DataFrame(df_ordenado_final)

# Guardar el DataFrame como un nuevo archivo CSV
if dataframe is not None:
    archivo_salida = 'atenciones_transfomados.csv'
    guardar_como_csv(dataframe, archivo_salida)
    print('Nombre de las columnas: \n', dataframe.columns.tolist())
    print(dataframe.head())  # Comprobación del contenido
