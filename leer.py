import pandas as pd
import os
from inline_sql import sql
import chardet

with open('./localidades-censales.csv', 'rb') as f:
    tipo = chardet.detect(f.read())

with open('./padron-de-operadores-organicos-certificados.csv', 'rb') as f:
    tipo1 = chardet.detect(f.read())
    
localidades_censales = pd.read_csv('./localidades-censales.csv',encoding=tipo['encoding'])
#w_median_depto_priv_clae2 = pd.read_csv('./w_median_depto_priv_clae2.csv')
padron_de_operadores_organicos_certificados = pd.read_csv('./padron-de-operadores-organicos-certificados.csv',encoding=tipo1['encoding'])
diccionario_clae2 = pd.read_csv('./diccionario_clae2.csv')
diccionario_cod_depto = pd.read_csv('./diccionario_cod_depto.csv')


#localidades_censales.columns
#w_median_depto_priv_clae2 = pd.read_csv('./w_median_depto_priv_clae2.csv')
#padron_de_operadores_organicos_certificados = pd.read_csv('./padron-de-operadores-organicos-certificados.csv',encoding=tipo1['encoding'])
#diccionario_clae2 = pd.read_csv('./diccionario_clae2.csv')
#diccionario_cod_depto = pd.read_csv('./diccionario_cod_depto.csv')

#o = sql^ ''' SELECT DISTINCT  provincia_id, departamento, p.establecimiento, razon_social FROM (select djfoer) p  padron_de_operadores_organicos_certificados p
 #               WHERE establecimiento != 'NC'
  #              '''

#salario = sql^ '''SELECT * FROM w_median_depto_priv_clae2 WHERE w_median != -99 AND codigo_departamento_indec != 'NAN' AND id_provincia_indec != 'NAN' '''

#salario.to_csv('salario.csv')
               
posta = sql^ '''SELECT DISTINCT * FROM padron_de_operadores_organicos_certificados WHERE establecimiento != 'NC' '''

estab = sql^ '''SELECT DISTINCT establecimiento, razon_social FROM padron_de_operadores_organicos_certificados WHERE establecimiento != 'NC' '''

posta.to_csv('posta.csv')

estab.to_csv('estab.csv')

# FUNCION PARA ARMAR LA TABLA ''PRODUCTOS''

conjunto_productos = set()

for fila in posta.loc[:,'productos']:
    if isinstance(fila, str):
        lista = fila.split(',')
        for palabra in lista:
            if palabra[0] == ' ':
                palabra = palabra[1:]
            conjunto_productos.add(palabra)
        productos_lista = list(conjunto_productos)

df_productos = pd.DataFrame(productos_lista,columns=['producto'])
    
# FUNCION PARA ARMAR LA TABLA DE LA RELACION ''PRODUCE''

tabla = sql^ ''' SELECT razon_social, establecimiento, productos FROM posta '''


prod_estab = []

for i in range(posta.shape[0]):    # itero la tabla padron, cada padron[i] es una fila
    fila = tabla.iloc[i,:]
    if isinstance(fila['productos'], str):
        productos = tabla.iloc[i,2].split(',')     # re
        for producto in productos:
            if producto[0] == ' ':
                producto = producto[1:]
            prod_estab.append([fila['razon_social'],fila['establecimiento'],producto])

df_productos_establecimiento = pd.DataFrame(prod_estab, columns=['razon_social','establecimiento','producto'])


# FUNCION PARA AGREGAR UNA COLUMNA ID_DEPTO A LA TABLA DE PADRON

tabla_con_id_depto = sql^ '''   SELECT posta.*, d.codigo_departamento_indec AS codigo_depto
                                FROM posta
                                INNER JOIN diccionario_cod_depto d 
                                ON UPPER(d.nombre_departamento_indec) = posta.departamento AND
                                   UPPER(d.id_provincia_indec) = posta.provincia_id
                        '''

    







a = ['bananá', 'perá', 'pédo', 'bóca']

df = pd.DataFrame({'a':a})

d = sql^ '''SELECT translate(a, 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU') AS dep FROM df'''
