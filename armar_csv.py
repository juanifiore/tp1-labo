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
import os
from inline_sql import sql
import chardet

with open('./localidades-censales.csv', 'rb') as f:
    tipo = chardet.detect(f.read())

with open('./padron-de-operadores-organicos-certificados.csv', 'rb') as f:
    tipo1 = chardet.detect(f.read())
    
localidades = pd.read_csv('./localidades-censales.csv',encoding=tipo['encoding'])
#salarios = pd.read_csv('./w_median_depto_priv_clae2.csv')
padron = pd.read_csv('./padron-de-operadores-organicos-certificados.csv',encoding=tipo1['encoding'])
diccionario_clases = pd.read_csv('./diccionario_clae2.csv')
diccionario_depto = pd.read_csv('./diccionario_cod_depto.csv')

#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE diccionario_clases
#==========================================================

# COLUMNAS DE diccionario_clases: ['clae2', 'clae2_desc', 'letra', 'letra_desc']

# armamos nueva tabla 'dicc_clases', PK: clave
dicc_clases = sql^ 'SELECT clae2 AS clave, clae2_desc AS clave_desc, letra FROM diccionario_clases'

# armamos nueva tabla 'letra', PK: letra
letra = sql^ 'SELECT letra, letra_desc FROM diccionario_clases'

# cargamos los nuevo df a csv
letra.to_csv('./3FN/diccionario_clases/letra.csv', index=False)
dicc_clases.to_csv('./3FN/diccionario_clases/dicc_clases.csv', index=False)


#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE diccionario_depto
#==========================================================





#==========================================================
# ARMAMOS LOS CSV CORREGIDOS Y EN 3FN DE padron
#==========================================================








