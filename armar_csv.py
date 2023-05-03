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
# ARMAMOS LOS CSV EN 3FN DE diccionario_clases
#==========================================================

# COLUMNAS DE diccionario_clases: ['clae2', 'clae2_desc', 'letra', 'letra_desc']

# armamos nueva tabla 'dicc_clases'
dicc_clases = sql^ 'SELECT clae2 AS clave, clae2_desc AS clave_desc, letra FROM diccionario_clases'

# armamos nueva tabla 'letra'
letra = sql^ 'SELECT letra, letra_desc FROM diccionario_clases'

# cargamos los nuevo df a csv
letra.to_csv('letra.csv', index=False)
dicc_clases.to_csv('dicc_clases.csv', index=False)


#==========================================================
# ARMAMOS LOS CSV EN 3FN DE diccionario_depto
#==========================================================











