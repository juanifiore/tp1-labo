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

# corregir 'caba'
dic6 = {'caba' : 'ciudad autonoma de buenos aires'}
diccionario_cod_depto2['nombre_departamento_indec'] = diccionario_cod_depto2['nombre_departamento_indec'].replace(dic6)



#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE padron
#==========================================================

# armamos diccionario a mano para reemplazar valores errados en 'departamento' por los correctos

diccionario_errores = {'carmen de patagones': 'patagones', 'ciudad autonoma buenos aires': 'ciudad autonoma de buenos aires','pigue': 'saavedra', 'villalonga': 'patagones', 'mar del plata':'general pueyrredon', 'guemes':'general guemes', 'centenario':'confluencia', 'san pedro de jujuy':'san pedro', 'villa martelli': 'vicente lopez', 'san miguel de tucuman':'capital', 'salta': 'capital', 'salta capital':'capital', 'ticino':'general san martin', 'cordoba':'capital','cordoba capital':'capital', 'plottier':'confluencia' }

padron_organico2['departamento']= padron_organico2['departamento'].replace(diccionario_errores)


consultaSQL8 = """
                SELECT *
                FROM padron_organico2 as p1
                WHERE departamento NOT IN (
                    SELECT nombre_departamento_indec
                    FROM diccionario_cod_depto2
                    WHERE provincia_id = id_provincia_indec)
                OR establecimiento = 'NC'
            """
deptosNoDicONC = sql ^ consultaSQL8
consultaSQL10 = """
                SELECT DISTINCT *
                FROM deptosNoDicONC as d
                WHERE departamento NOT IN (
                SELECT DISTINCT municipio_nombre
                FROM localidades_censales as l
                WHERE l.provincia_id = d.provincia_id)
            """
deptosNoMun = sql ^ consultaSQL10

#deptosNoMun son los deptos q no matchean con un depto del diccionario, ni con un municipio. son los q volariamos.
consultaSQL9 = """
                SELECT DISTINCT *
                FROM padron_organico2
                EXCEPT
                SELECT DISTINCT *
                FROM deptosNoMun
            """
padron_organico3 = sql ^ consultaSQL9







#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE localidades 
#==========================================================

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

