'''
@grupo: Falczuk, Sanes, Fiore
@materia: Laboratorio De Datos

CREACION DE TABLAS EN 3FN Y CORREGIDAS PARA EL TRABAJO PRACTICO 1

En este codigo modificaremos mediante Pandas y SQL los .csv para que se encuentren en 3FN,
tambien editaremos datos erroneos que contengan o eliminaremos informacion duplicada o inservible, ya sea mediante SQL, Pandas o manualmente
mediante la planilla excel. 

ACLARACIONES: 1) Es necesario tener todos los .csv originales a utilizar en una carpeta llamada TablasOriginales, el mismo directorio donde se ejecutara el programa.
Al correr el codigo se crean todas las nuevas tablas. Para que sea mas organizado, 
los nuevos .csv se guardaran en subcarpetas dentro del directorio actual donde se ejecuta el programa, 
por lo tanto es necesario tener creada de antemano una carpeta (dentro del mismo directorio  que se encuentre este 
programa) llamada '3FN', y que adentro contenga las carpetas 'diccionario_clases', 'diccionario_depto', 'padron', 'salarios', 'localidades'.
A su vez, los .csv limpios que usaremos en las consultas se guardaran en la carpeta TablasLimpias

2) Para que el programa sea mas claro, y tambien poder ver claramente cada modificacion hecha a los .csv, separaremos el codigo por cada paso
para llegar a los .csv en 3FN y con todos los errores corregidos, en lugar de juntar varias modificaciones en uno solo algoritmo. Creemos que esto
ademas facilitaria las cosas en el caso de que una modificacion este mal o querramos mejorar alguna especifica. 

3) Los archivos originales que utilizaremos para crear los nuevos .csv fueron modificados mediante excel algunos datos pequeños 
manualmente (detallados en cada caso), por lo que no concuerdan con los originales cargados en las paginas oficiales. Fueron descargados en abril-2023.

4) Los caracteres de las columnas de los .csv que usaremos para hacer JOIN estaran en minuscula y sin tildes para evitar problemas de matching
'''

import pandas as pd
from inline_sql import sql

localidades = pd.read_csv('./TablasOriginales/localidades-censales.csv')
salarios_median = pd.read_csv('./TablasOriginales/w_median_depto_priv_clae2.csv')
padron = pd.read_csv('./TablasOriginales/padron-de-operadores-organicos-certificados.csv')
diccionario_clases = pd.read_csv('./TablasOriginales/diccionario_clae2.csv')
diccionario_depto = pd.read_csv('./TablasOriginales/diccionario_cod_depto.csv')

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
letra.to_csv('./TablasLimpias/letra.csv', index=False)
dicc_clases.to_csv('./3FN/diccionario_clases/dicc_clases.csv', index=False)
dicc_clases.to_csv('./TablasLimpias/dicc_clases.csv', index=False)


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
# 2) Creamos diccionario para reemplazar errores por su valor correcto
diccionario_err_depto = {'caba' : 'ciudad autonoma de buenos aires'}
diccionario_depto['nombre_departamento_indec'] = diccionario_depto['nombre_departamento_indec'].replace(diccionario_err_depto)

# 3) Creamos tabla principal en 3FN 'diccionario_departamentos'
# PK: ['id_depto']
diccionario_departamentos = sql^ '''SELECT DISTINCT codigo_departamento_indec AS id_depto, 
                                        nombre_departamento_indec AS departamento_nombre,
                                        id_provincia_indec AS id_provincia
                                    FROM diccionario_depto '''
diccionario_departamentos.to_csv('./3FN/diccionario_depto/diccionario_departamentos.csv', index=False)
diccionario_departamentos.to_csv('./TablasLimpias/diccionario_departamentos.csv', index=False)

# 4) Creamos tabla secundaria 'provincias'
# PK: ['id_provincia']
provincias = sql^ '''   SELECT DISTINCT id_provincia_indec AS id_provincia, nombre_provincia_indec AS provincias_nombre
                        FROM diccionario_depto '''
provincias.to_csv('./3FN/diccionario_depto/provincias.csv',index=False)
provincias.to_csv('./TablasLimpias/provincias.csv',index=False)




#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE localidades 
#==========================================================

# Columnas de localidades: ['categoria', 'centroide_lat', 'centroide_lon', 'departamento_id',
#       'departamento_nombre', 'fuente', 'funcion', 'id', 'municipio_id',
#       'municipio_nombre', 'nombre', 'provincia_id', 'provincia_nombre']

# 1) Ponemos los caracteres de las columnas a matchear en minuscula y sin tilde, 
# tambien cambiamos los valores NULL de la columna 'funcion' por el valor 'no_tiene'
localidades = sql^ '''  SELECT categoria, centroide_lat, centroide_lon, departamento_id, 
                        LOWER(translate(departamento_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS departamento_nombre,
                        fuente, 
                        CASE WHEN funcion IS NULL THEN 'no_tiene' ELSE funcion END AS funcion,
                        id, municipio_id,
                        LOWER(translate(municipio_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS municipio_nombre,
                        nombre, provincia_id, provincia_nombre
                        FROM localidades
                        '''
# 2) Creamos diccionario para reemplazar errores por su valor correcto
diccionario_errores_loc = ({"CABA": "Ciudad autónoma de Buenos Aires"})  
localidades['departamento_nombre'] = localidades['departamento_nombre'].replace(diccionario_errores_loc) 

# 3) Creamos tabla principal en 3FN 'localidades_censales'
# PK: ['id']
localidades_censales = sql^ ''' SELECT DISTINCT id, departamento_id AS id_depto, municipio_id, nombre, funcion, categoria, centroide_lat, centroide_lon
                                FROM localidades
                            '''
localidades_censales.to_csv('./3FN/localidades/localidades_censales.csv',index=False)
localidades_censales.to_csv('./TablasLimpias/localidades_censales.csv',index=False)

# 4) Creamos tabla secundaria 'departamentos'
# PK: ['id_depto']
departamentos = sql^ '''SELECT DISTINCT departamento_id AS id_depto, departamento_nombre AS nombre_departamento, 
                        provincia_id AS id_provincia
                        FROM localidades'''
departamentos.to_csv('./3FN/localidades/departamentos.csv',index=False)

# 5) Creamos tabla secundaria 'municipios'
# PK: ['municipio_id']
municipios = sql^ '''SELECT DISTINCT municipio_id, municipio_nombre
                        FROM localidades'''
municipios.to_csv('./3FN/localidades/municipios.csv',index=False)
municipios.to_csv('./TablasLimpias/municipios.csv',index=False)

# 6) Creamos tabla secundaria 'provincias'
# PK: ['id_provincia']
provincias = sql^ '''SELECT DISTINCT provincia_id AS id_provincia, provincia_nombre 
                        FROM localidades'''
provincias.to_csv('./3FN/localidades/provincias.csv',index=False)



#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE padron
#==========================================================

# Columnas de padron: ['pais_id', 'pais', 'provincia_id', 'provincia', 'departamento',
#       'localidad', 'rubro', 'productos', 'categoria_id', 'categoria_desc',
#       'Certificadora_id', 'certificadora_deno', 'razon_social',
#       'establecimiento']

# Ponemos las columnas que nececitamos matchear en minusculas y sin tildes
padron = sql^ '''   SELECT pais_id, pais, provincia_id,
                    LOWER(translate(provincia,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS provincia, 
                    LOWER(translate(departamento,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS departamento, 
                    localidad, 
                    LOWER(translate(rubro,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS rubro, 
                    LOWER(translate(productos,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS productos, 
                    categoria_id, categoria_desc, Certificadora_id, certificadora_deno,
                    LOWER(translate(razon_social,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS razon_social, 
                    LOWER(translate(establecimiento,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS establecimiento, 
                    FROM padron '''

# 1) Armamos diccionario a mano para reemplazar valores errados en 'departamento' y 'provincia' por los correctos
diccionario_errores_depto = {'carmen de patagones': 'patagones', 'ciudad autonoma buenos aires': 'ciudad autonoma de buenos aires','pigue': 'saavedra', 'villalonga': 'patagones', 'mar del plata':'general pueyrredon', 'guemes':'general guemes', 'centenario':'confluencia', 'san pedro de jujuy':'san pedro', 'villa martelli': 'vicente lopez', 'san miguel de tucuman':'capital', 'salta': 'capital', 'salta capital':'capital', 'ticino':'general san martin', 'cordoba':'capital','cordoba capital':'capital', 'plottier':'confluencia' }

diccionario_errores_prov = ({"TIERRA DEL FUEGO": "Tierra del Fuego, Antártida e Islas del Atlántico Sur"})

# 2) Reemplazamos los valores usando el diccionario
padron['departamento']= padron['departamento'].replace(diccionario_errores_depto)
padron['provincia'] = padron['provincia'].replace(diccionario_errores_prov)

# 3) Eliminamos valores 'NC' de la columna 'establecimiento'
padron = sql^ '''SELECT * FROM padron WHERE establecimiento != 'nc' '''

# 4) Cambiamos los valores en la columna 'departamento' que sean de municipios, por sus respectivos departamentos
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


# 5) Eliminamos los departamentos que no se encuentren en el diccionario, tanto en la columna 'departamentos', 
# como 'municipio_nombre'

padron = sql^ """
                SELECT DISTINCT *
                FROM padron 
                WHERE departamento IN (
                    SELECT nombre_departamento_indec
                    FROM diccionario_depto
                    WHERE provincia_id = id_provincia_indec)
                ORDER BY departamento
            """


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
productos_lista = []
for fila in padron.loc[:,'productos']:       # recorremos la columna 'productos' 
    if isinstance(fila, str):       
        lista = fila.split(',')       # separamos la string en una lista con cada producto como elemento
        for palabra in lista:
            if palabra[0] == ' ':
                palabra = palabra[1:]
            conjunto_productos.add(palabra)     # añadimos cada producto de la lista anterior a un conjunto
        productos_lista = list(conjunto_productos)      # pasamos el conjunto a una lista

df_productos = pd.DataFrame(productos_lista,columns=['producto'])       # creamos el dataframe
df_productos.to_csv('./3FN/padron/productos.csv',index=False)
df_productos.to_csv('./TablasLimpias/productos.csv',index=False)


# 8) Creamos una nueva tabla llamada 'produce', que posee como columnas: ['razon_social', 'establecimiento', 'producto']
# para poder poner en 1FN el .csv padron
temp = sql^ ''' SELECT razon_social, establecimiento, productos FROM padron''' # creamos una tabla con las columnas que usaremos 

produce_lista = []    # creamos una lista de listas, que luego convertiremos en DataFrame como la tabla 'produce'

for i in range(padron.shape[0]):    # iteramos la tabla padron, cada 'padron[i]' es una fila
    fila = temp.iloc[i,:]      #asignamos la fila actual
    if isinstance(fila['productos'], str):
        productos = temp.iloc[i,2].split(',')     # generamos una lista con los productos del establecimiento actual
        for producto in productos:
            if producto[0] == ' ':
                producto = producto[1:]
            produce_lista.append([fila['razon_social'],fila['establecimiento'],producto])  # agregamos cada lista [razon_social, establecimiento, producto] por iteracion

produce = pd.DataFrame(produce_lista, columns=['razon_social','establecimiento','producto'])  # convertimos produce_lista en el DataFrame 'produce'
produce.to_csv('./3FN/padron/produce.csv',index=False)
produce.to_csv('./TablasLimpias/produce.csv',index=False)

# 9) Armamos una tabla que se llame 'rubros', que contenga como unica columna los rubros a los cuales puede pertenecer un establecimiento determinado

conjunto_rubros = set()
rubros_lista = []
for fila in padron.loc[:,'rubro']:       # recorremos la columna 'productos'
    if isinstance(fila, str):
        rep = ['/', ' y ', ';', '.', 'elaboracion de ']
        for c in rep:
            fila = fila.replace(c,',')
        lista = fila.split(',')       # separamos la string en una lista con cada rubro como elemento
        for palabra in lista:
            if len(palabra) > 0 and palabra[0] == ' ':
                palabra = palabra[1:]
            if len(palabra) > 0 and palabra[-1] == ' ':
                palabra = palabra[0:len(palabra)-1]
            conjunto_rubros.add(palabra)         # añadimos cada rubro de la lista anterior a un conjunto
rubros_lista = list(conjunto_rubros)      # pasamos el conjunto a una lista
       
df_rubros = pd.DataFrame(rubros_lista,columns=['rubros'])       # creamos el dataframe
# modificamos a mano los datos mal cargados
df_rubros['rubros'] = df_rubros['rubros'].replace('agicultura', 'agricultura')

df_rubros.to_csv('./3FN/padron/rubros.csv',index=False)
df_rubros.to_csv('./TablasLimpias/rubros.csv',index=False)


# 10) Creamos una nueva tabla llamada 'establecimiento_rubro', que posee como columnas: ['razon_social', 'establecimiento', 'rubros']
# para poder poner en 1FN el .csv padron

temp = sql^ ''' SELECT razon_social, establecimiento, rubro FROM padron''' # creamos una tabla con las columnas que usaremos

establecimiento_rubro_lista = []    # creamos una lista de listas, que luego convertiremos en DataFrame como la tabla 'establecimiento_rubro'

for i in range(padron.shape[0]):    # iteramos la tabla padron, cada 'padron[i]' es una fila
    fila = temp.iloc[i,:]      #asignamos la fila actual
    if isinstance(fila['rubro'], str):
        rep = ['/', ' y ', ';', '.', 'elaboracion de ']
        for c in rep:
            fila['rubro'] = fila['rubro'].replace(c,',')
        rubros = temp.iloc[i,2].split(',') # generamos una lista con los rubros del establecimiento actual
        for rubro in rubros:
            if len(rubro) > 0 and rubro[0] == ' ':
                rubro = rubro[1:]
            if len(rubro) > 0 and rubro[-1] == ' ':
                rubro = rubro[0:len(rubro)-1]
            establecimiento_rubro_lista.append([fila['razon_social'],fila['establecimiento'],rubro])  # agregamos cada lista [razon_social, establecimiento, producto] por iteracion

establecimiento_rubro = pd.DataFrame(establecimiento_rubro_lista, columns=['razon_social','establecimiento','rubros'])  # convertimos establecimiento_rubro_lista en el DataFrame 'establecimiento_rubro'
# modificamos a mano los datos mal cargados
establecimiento_rubro['rubros'] = establecimiento_rubro['rubros'].replace('agicultura', 'agricultura')
establecimiento_rubro.to_csv('./3FN/padron/establecimiento_rubro.csv')
establecimiento_rubro.to_csv('./TablasLimpias/establecimiento_rubro.csv')


# 11) Creamos la tabla principal en 3FN llamada 'padron_operadores' y la cargamos como .csv
# PK: ['establecimiento','razon_social']
padron_operadores = sql^ '''SELECT DISTINCT establecimiento, razon_social, id_depto, categoria_id, Certificadora_id
                            FROM padron '''
padron_operadores.to_csv('./3FN/padron/padron_operadores.csv', index=False)
padron_operadores.to_csv('./TablasLimpias/padron_operadores.csv', index=False)


# 12) Creamos tabla secundaria 'departamentos',
# PK: ['id_depto']
departamentos = sql^ '''SELECT DISTINCT id_depto, departamento AS departamento_nombre, provincia_id AS id_provincia
                        FROM padron'''
departamentos.to_csv('./3FN/padron/departamentos.csv',index=False)

# 13) Creamos tabla secundaria 'certificadoras'
# PK: ['certificadora_id']
certificadoras = sql^ '''SELECT DISTINCT Certificadora_id, certificadora_deno FROM padron'''
certificadoras.to_csv('./3FN/padron/certificadoras.csv',index=False)
certificadoras.to_csv('./TablasLimpias/certificadoras.csv',index=False)

# 14) Creamos tabla secundaria 'paises'
# PK: ['pais_id']
paises = sql^ '''SELECT DISTINCT pais_id, pais FROM padron '''
paises.to_csv('./3FN/padron/paises.csv',index=False)
paises.to_csv('./TablasLimpias/paises.csv',index=False)

# 15) Creamos tabla secundaria 'categorias'
# PK: ['categoria_id']
categorias = sql^ '''SELECT DISTINCT categoria_id, categoria_desc FROM padron '''
categorias.to_csv('./3FN/padron/categorias.csv',index=False)
categorias.to_csv('./TablasLimpias/categorias.csv',index=False)
                                



#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE salarios 
#==========================================================

# Columnas de 'salario': ['fecha', 'codigo_departamento_indec', 'id_provincia_indec', 'clae2','w_median']

#borramos los -99 en salario
salarios_median = sql^ '''SELECT * FROM salarios_median WHERE w_median != '-99' '''

# creamos tabla primaria 'salarios'
salarios = sql^ ''' SELECT fecha, codigo_departamento_indec AS id_depto, clae2, w_median AS salario
                    FROM salarios_median
                '''

# creamos tabla secundaria 'salario_departamentos'
departamentos_salarios = sql^ ''' SELECT DISTINCT codigo_departamento_indec AS id_depto, id_provincia_indec AS id_provincia
                                  FROM salarios_median
                            '''
# cargamos los .csv en 3FN:
salarios.to_csv('./3FN/salarios/salarios.csv', index=False)
salarios.to_csv('./TablasLimpias/salarios.csv', index=False)
departamentos_salarios.to_csv('./3FN/salarios/departamentos.csv', index=False)

