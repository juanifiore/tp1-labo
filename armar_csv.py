'''
@grupo: Falczuk, Sanes, Fiore
@materia: Laboratorio De Datos

CREACION DE TABLAS EN 3FN Y CORREGIDAS PARA EL TRABAJO PRACTICO 1

En este codigo modificaremos mediante Pandas y SQL los .csv para que se encuentren en 3FN,
tambien editaremos datos erroneos que contengan o eliminaremos informacion duplicada o inservible, ya sea mediante SQL, Pandas o manualmente
mediante la planilla excel. 

ACLARACIONES: 1) Es necesario tener todos los .csv a utilizar en el mismo directorio donde se ejecutara el programa.
Al correr el codigo se crean todas las nuevas tablas. Para que sea mas organizado, 
los nuevos .csv se guardaran en subcarpetas dentro del directorio actual donde se ejecuta el programa, 
por lo tanto es necesario tener creada de antemano una carpeta (dentro del mismo directorio  que se encuentre este 
programa) llamada '3FN', y que adentro contenga las carpetas 'diccionario_clases', 'diccionario_depto', 'padron', 'salarios', 'localidades'.

2) Para que el programa sea mas claro, y tambien poder ver claramente cada modificacion hecha a los .csv, separaremos el codigo por cada paso
para llegar a los .csv en 3FN y con todos los errores corregidos, en lugar de juntar varias modificaciones en uno solo algoritmo. Creemos que esto
ademas facilitaria las cosas en el caso de que una modificacion este mal o querramos mejorar alguna especifica. 

3) Los archivos originales que utilizaremos para crear los nuevos .csv fueron modificados mediante excel algunos datos pequeños 
manualmente (detallados en cada caso), por lo que no concuerdan con los originales cargados en las paginas oficiales. Fueron descargados en abril-2023.

4) Los caracteres de los datos de los .csv estaran en minuscula y sin tildes para evitar problemas de matching
'''

import pandas as pd
from inline_sql import sql

localidades = pd.read_csv('./localidades-censales.csv')
salarios_median = pd.read_csv('./w_median_depto_priv_clae2.csv')
padron = pd.read_csv('./padron-de-operadores-organicos-certificados.csv')
diccionario_clases = pd.read_csv('./diccionario_clae2.csv')
diccionario_depto = pd.read_csv('./diccionario_cod_depto.csv')

#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE diccionario_clases
#==========================================================

# COLUMNAS DE diccionario_clases: ['clae2', 'clae2_desc', 'letra', 'letra_desc']

# Ponemos todos los caracteres en minusculas y sin tildes.
diccionario_clases = sql^ '''   SELECT LOWER(translate(clae2,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS clae2,
                                LOWER(translate(clae2_desc,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS clae2_desc,
                                LOWER(translate(letra,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS letra,
                                LOWER(translate(letra_desc,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS letra_desc,
                                FROM diccionario_clases
                         '''

# armamos nueva tabla 'dicc_clases', PK: clave
dicc_clases = sql^ 'SELECT DISTINCT clae2 AS clave, clae2_desc AS clave_desc, letra FROM diccionario_clases'

# armamos nueva tabla 'letra', PK: letra
letra = sql^ 'SELECT DISTINCT letra, letra_desc FROM diccionario_clases'

# cargamos los nuevo df a csv
letra.to_csv('./3FN/diccionario_clases/letra.csv', index=False)
dicc_clases.to_csv('./3FN/diccionario_clases/dicc_clases.csv', index=False)


#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE diccionario_depto
#==========================================================

# Columnas de diccionario_depto: ['codigo_departamento_indec', 'nombre_departamento_indec',
#       'id_provincia_indec', 'nombre_provincia_indec']

# 1) Ponemos todos los caracteres en minuscula y sin tilde
diccionario_depto = sql^ '''    SELECT LOWER(translate(codigo_departamento_indec,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS codigo_departamento_indec,
                                    LOWER(translate(nombre_departamento_indec,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS nombre_departamento_indec,
                                    LOWER(translate(id_provincia_indec,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS id_provincia_indec,
                                    LOWER(translate(nombre_provincia_indec,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS nombre_provincia_indec
                                FROM diccionario_depto
                        '''
# corregir 'caba'
dic6 = {'caba' : 'ciudad autonoma de buenos aires'}
diccionario_cod_depto2['nombre_departamento_indec'] = diccionario_cod_depto2['nombre_departamento_indec'].replace(dic6)




#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE localidades 
#==========================================================

# Columnas de localidades: ['categoria', 'centroide_lat', 'centroide_lon', 'departamento_id',
#       'departamento_nombre', 'fuente', 'funcion', 'id', 'municipio_id',
#       'municipio_nombre', 'nombre', 'provincia_id', 'provincia_nombre']

# 1) Ponemos los caracteres de las columnas a matchear en minuscula y sin tilde
localidades = sql^ '''  SELECT categoria, centroide_lat, centroide_lon, departamento_id, 
                        LOWER(translate(departamento_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS departamento_nombre,
                        fuente, funcion, id, munidicipio_id,
                        LOWER(translate(municipio_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS municipio_nombre,
                        nombre, provincia_id, provincia_nombre
                        FROM localidades
                        '''
# reemplazar valores NaN en 'funcion' por 'no_tiene'
nulls = """
        SELECT   categoria, centroide_lat, centroide_lon, departamento_id, departamento_nombre, fuente,    CASE WHEN funcion IS NULL THEN 'no_tiene'
                   ELSE funcion
                   END AS funcion ,
                   id, municipio_id, municipio_nombre, nombre, provincia_id, provincia_nombre
        FROM localidades_censales
    """
localidades_censales = sql ^ nulls








#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE padron
#==========================================================

# Columnas de padron: ['pais_id', 'pais', 'provincia_id', 'provincia', 'departamento',
#       'localidad', 'rubro', 'productos', 'categoria_id', 'categoria_desc',
#       'Certificadora_id', 'certificadora_deno', 'razon_social',
#       'establecimiento']

# 1) Armamos diccionario a mano para reemplazar valores errados en 'departamento' por los correctos
diccionario_errores = {'carmen de patagones': 'patagones', 'ciudad autonoma buenos aires': 'ciudad autonoma de buenos aires','pigue': 'saavedra', 'villalonga': 'patagones', 'mar del plata':'general pueyrredon', 'guemes':'general guemes', 'centenario':'confluencia', 'san pedro de jujuy':'san pedro', 'villa martelli': 'vicente lopez', 'san miguel de tucuman':'capital', 'salta': 'capital', 'salta capital':'capital', 'ticino':'general san martin', 'cordoba':'capital','cordoba capital':'capital', 'plottier':'confluencia' }

# 2) Reemplazamos los valores usando el diccionario
padron['departamento']= padron['departamento'].replace(diccionario_errores)

# 3) Eliminamos valores 'NC' de la columna 'establecimiento'
padron = sql^ '''SELECT * FROM padron WHERE establecimiento != 'NC' '''

# 4) Eliminamos los departamentos que no se encuentren en el diccionario, tanto en la columna 'departamentos', 
# como 'municipio_nombre'
padron = sql^ '''
                SELECT *
                FROM padron p
                WHERE p.departamento IN (
                    SELECT nombre_departamento_indec
                    FROM diccionario_depto d
                    WHERE d.id_provincia_indec = p.provincia_id
                    UNION
                    SELECT municipio_nombre
                    FROM localidades l
                    WHERE l.provincia_id = p.provincia_id
                )
                '''

# 5) Cambiamos los valores en la columna 'departamento' que sean de municipios, por sus respectivos departamentos
# Primero creamos un DF que tenga los departamentos a reemplazar y su valor correspondiente
deptos_muni = sql^  '''SELECT DISTINCT p.departamento AS municipio, l.departamento_nombre AS departamento
                        FROM padron p
                        INNER JOIN localidades l
                        ON p.departamento = l.municipio_nombre AND p.provincia_id = l.provincia_id
                        WHERE p.departamento != l.departamento_nombre
                        '''

# Creamos un diccionario con los municipios como clave y los departamento como valores a partir del DF 'deptos_muni'
dicc_muni_depto = deptos_muni.set_index('municipio')['departamento'].to_dict()

# Reemplazamos los valores usando el diccionario
padron['departamento']= padron['departamento'].replace(dicc_muni_depto)

# 6) Agregamos una columna 'id_depto' al .csv 'padron', joinneando con el .csv 'diccionario_depto'
padron = sql^ '''   SELECT padron.*, d.codigo_departamento_indec AS id_depto 
                                FROM padron
                                INNER JOIN diccionario_depto d 
                                ON d.nombre_departamento_indec = padron.departamento AND
                                   d.id_provincia_indec = padron.provincia_id
                        '''

# 7) Armamos una tabla que se llame 'productos', que contenga como unica columna los productos
# que producen todos los operadores organicos
conjunto_productos = set()
for fila in posta.loc[:,'productos']:       # recorremos la columna 'productos' 
    if isinstance(fila, str):       
        lista = fila.split(',')       # separamos la string en una lista con cada producto como elemento
        for palabra in lista:
            if palabra[0] == ' ':
                palabra = palabra[1:]
            conjunto_productos.add(palabra)     # añadimos cada producto de la lista anterior a un conjunto
        productos_lista = list(conjunto_productos)      # pasamos el conjunto a una lista

df_productos = pd.DataFrame(productos_lista,columns=['producto'])       # creamos el dataframe


# 8) Creamos una nueva tabla llamada 'produce', que posee como columnas: ['razon_social', 'establecimiento', 'producto']
# para poder poner en 1FN el .csv padron
temp = sql^ ''' SELECT razon_social, establecimiento, productos FROM padron''' # creamos una tabla con las columnas que usaremos 

produce_lista = []    # creamos una lista de listas, que luego convertiremos en DataFrame como la tabla 'produce'

for i in range(posta.shape[0]):    # iteramos la tabla padron, cada 'padron[i]' es una fila
    fila = tabla.iloc[i,:]      #asignamos la fila actual
    if isinstance(fila['productos'], str):
        productos = tabla.iloc[i,2].split(',')     # generamos una lista con los productos del establecimiento actual
        for producto in productos:
            if producto[0] == ' ':
                producto = producto[1:]
            prod_estab.append([fila['razon_social'],fila['establecimiento'],producto])  # agregamos cada lista [razon_social, establecimiento, producto] por iteracion

produce = pd.DataFrame(produce_lista, columns=['razon_social','establecimiento','producto'])  # convertimos produce_lista en el DataFrame 'produce'


# 9) Creamos la tabla principal en 3FN llamada 'padron_operadores', 
# PK: ['establecimiento','razon_social']
# Columnas: 
padron_operadores = sql^ '''SELECT 







#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE salarios 
#==========================================================

# Columnas de 'salario': ['fecha', 'codigo_departamento_indec', 'id_provincia_indec', 'clae2','w_median']

#borramos los -99 en salario
salarios_median = sql^ '''SELECT * FROM salarios_median WHERE w_median != '-99' '''

# creo tabla primaria 'salarios'
salarios = sql^ ''' SELECT fecha, codigo_departamento_indec AS id_depto, w_median AS salario
                    FROM salarios_median
                '''

# creo tabla secundaria 'salario_departamentos'
departamentos_salarios = sql^ ''' SELECT codigo_departamento_indec AS id_depto, id_provincia_indec AS id_provincia
                                FROM salarios_median
                            '''
# cargo los .csv en 3FN:
salarios.to_csv('./3FN/salarios/salarios.csv', index=False)
departamentos_salarios.to_csv('./3FN/salarios/departamentos_salarios.csv', index=False)

