#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 14:28:14 2023

@author: matematica2
"""
import pandas as pd
from inline_sql import sql

localidades = pd.read_csv('./localidades-censales.csv')
salarios_median = pd.read_csv('./w_median_depto_priv_clae2.csv')
padron = pd.read_csv('./padron-de-operadores-organicos-certificados.csv')
diccionario_clases = pd.read_csv('./diccionario_clae2.csv')
diccionario_depto = pd.read_csv('./diccionario_cod_depto.csv')


padron = sql^ '''SELECT pais_id, pais, provincia_id, provincia, LOWER(translate(departamento,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS departamento,
                        rubro, productos, categoria_id, categoria_desc, Certificadora_id, certificadora_deno, razon_social, establecimiento
                FROM padron'''

padron = sql^ '''SELECT * FROM padron WHERE establecimiento != 'NC' '''
# Columnas de departamento_depto: ['pais_id', 'pais', 'provincia_id', 'provincia', 'departamento',
#       'localidad', 'rubro', 'productos', 'categoria_id', 'categoria_desc',
#       'Certificadora_id', 'certificadora_deno', 'razon_social',
#       'establecimiento']
#localidades = sql^ ''' SELECT provincia_id, LOWER(translate(municipio_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS municipio_nombre,
#                        LOWER(translate(departamento_nombre,'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu')) AS departamento_nombre
#                        FROM localidades
#                        '''
#
#

deptos_muni = sql^  '''SELECT DISTINCT p.departamento, l.departamento_nombre
                        FROM padron p
                        INNER JOIN localidades l
                        ON p.departamento = l.municipio_nombre AND p.provincia_id = l.provincia_id
                        WHERE p.departamento != l.departamento_nombre
                        '''

# Eliminamos los departamentos que no se encuentren en el diccionario, y tambien los que no  
# coincidan con la columna 'municipio_nombre' del csv localidades censales.
#padron = sql^ '''   SELECT * FROM padron 
#                    EXCEPT 
#                    SELECT * FROM padron p
#                    WHERE p.departamento NOT IN (
#                        SELECT DISTINCT nombre_departamento_indec
#                        FROM diccionario_depto d
#                        WHERE p.provincia_id = d.id_provincia_indec)
#                        OR p.departamento NOT IN (
#                        SELECT DISTINCT municipio_nombre
#                        FROM localidades l
#                        WHERE p.provincia_id = l.id_provincia)
#                        '''
#
