'''
@grupo: Falczuk, Sanes, Fiore
@materia: Laboratorio De Datos

RESPUESTA A CONSULTAS USANDO SQL 

Consigna: 
    Responder las siguientes consultas a través de consultas SQL:
        
Antes de responder a las consignas cargaremos los .csv de los cuales haremos uso para respodner a las consultas:
'''
import pandas as pd
from inline_sql import sql
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

#diccionario_depto
provincias = pd.read_csv('./TablasLimpias/provincias.csv')

establecimiento_rubro = pd.read_csv('./TablasLimpias/establecimiento_rubro.csv')
departamentos = pd.read_csv('./TablasLimpias/departamentos.csv')
produce = pd.read_csv('./TablasLimpias/produce.csv')

#padron
padron_operadores = pd.read_csv('./TablasLimpias/padron_operadores.csv')

certificadoras = pd.read_csv('./TablasLimpias/certificadoras.csv')

#salarios
salarios = pd.read_csv('./TablasLimpias/salarios.csv')
#fecha, id_depto, salario
deptosalarios = pd.read_csv('./TablasLimpias/departamentos.csv')
#id_depto, id_provincia
'./TablasLimpias/''
        
A) ¿Existen provincias que no presentan Operadores Orgánicos Certificados?
    ¿En caso de que sí, cuántas y cuáles son?
'''

provincias_sin_op_organicos = sql^ """SELECT DISTINCT p.id_provincia, p.provincias_nombre
                                    FROM provincias p 
                                    WHERE p.id_provincia NOT IN (
                                        SELECT DISTINCT d.id_provincia
                                        FROM departamentos d 
                                        WHERE d.id_depto IN (
                                            SELECT DISTINCT o.id_depto
                                            FROM padron_operadores o
                                            ))   
                                    ORDER BY p.provincias_nombre
                                    """     

'''
B) ¿Existen departamentos que no presentan Operadores Orgánicos Certificados? 
    ¿En caso de que sí, cuántos y cuáles son?
'''

departamentos_sin_op_organicos = sql^ """SELECT DISTINCT d.departamento_nombre, p.provincias_nombre
                                    FROM departamentos d 
                                    INNER JOIN provincias p
                                    ON d.id_provincia = p.id_provincia
                                    WHERE d.id_depto NOT IN (
                                        SELECT DISTINCT o.id_depto
                                        FROM padron_operadores o
                                        )
                                    ORDER BY d.departamento_nombre, p.provincias_nombre
                                    """
#
#consultaSQL21 = """
#                SELECT DISTINCT departamento_nombre, provincias_nombre
#                FROM padron_operadores 
#                INNER JOIN departamentos d
#                INNER JOIN provincias p
#                ON d.id_provincia = p.id_provincia
#                ON d.id_depto = padron_operadores.id_depto
#            """
#            
#deptosConOOC = sql^ consultaSQL21
#
#consultaSQL22 = """
#                SELECT DISTINCT departamentos.departamento_nombre, provincias_nombre
#                FROM departamentos 
#                EXCEPT 
#                SELECT DISTINCT *
#                FROM deptosConOOC;
#            """
#deptosSinOOC = sql^ consultaSQL22
#
#consultaSQL23 = """
#                SELECT count(*) as cantidadSinOOC
#                FROM deptosSinOOC;
#            """
#cantidadDeptosSinOOC = sql ^ consultaSQL23
#
'''
C) ¿Cuál es la actividad que más operadores tiene?
    
'''

rubro_con_cantidad = sql^''' SELECT DISTINCT r.rubros as rubros, count(*) as cantidad
                     FROM establecimiento_rubro r 
                     INNER JOIN padron_operadores p
                     ON p.razon_social = r.razon_social and p.establecimiento = p.establecimiento
                     GROUP BY r.rubros
                     ORDER BY r.rubros
                     '''

act_mas_op = sql^''' SELECT DISTINCT r1.rubros as actividad
                     FROM rubro_con_cantidad r1
                     WHERE r1.cantidad >= ALL (
                         SELECT R2.cantidad 
                         FROM rubro_con_cantidad R2
                         WHERE r2.rubros !=r1.rubros
                         )
                     GROUP BY r1.rubros 
                     ORDER BY r1.rubros
'''

'''
D) ¿Cuál fue el salario promedio de esa actividad en 2022? (si hay varios registros de salario, mostrar el más actual de ese año)
'''

actividad = act_mas_op['actividad'][0]
id_depto_dedicados_a_actividad = sql^''' SELECT DISTINCT p.id_depto as id_depto
                                     FROM padron_operadores p
                                     INNER JOIN establecimiento_rubro r 
                                     ON r.razon_social = p.razon_social and r.establecimiento = p.establecimiento 
                                     WHERE r.rubros = $actividad
                                     GROUP BY p.id_depto
                                     '''

salarios_actividad_2022 = sql^'''SELECT DISTINCT fecha, id_depto, clae2, salario
                                 FROM salarios s
                                 WHERE s.fecha LIKE '%2022%' and s.id_depto IN (
                                     SELECT DISTINCT a.id_depto
                                     FROM id_depto_dedicados_a_actividad a
                                     )
                                 GROUP BY fecha, id_depto, salario, clae2
                                 ORDER BY fecha ASC, id_depto ASC
                                 '''
                                
salario_promedio_2022 = sql^'''SELECT AVG(salario) FROM salarios_actividad_2022'''                            

consultaSQL41 = """
                SELECT DISTINCT AVG(salario) AS salarioPromedio2022
                FROM padron_operadores as p1
                INNER JOIN establecimiento_rubro as r1
                ON p1.establecimiento = r1.establecimiento and p1.razon_social = r1.razon_social
                INNER JOIN salarios
                ON p1.id_depto = salarios.id_depto
                WHERE rubros = 'fruticultura' AND fecha LIKE '%2022%'
            """
promedioSalarios = sql ^ consultaSQL41       


'''
F) ¿Cuál es el promedio anual de los salarios en Argentina y cual es su
desvío?, ¿Y a nivel provincial? ¿Se les ocurre una forma de que sean
comparables a lo largo de los años? ¿Necesitarían utilizar alguna fuente de
datos externa secundaria? ¿Cuál?

'''

"""
for fila in salarios.loc[:,'fecha']:
    if len(fila)>4:
        salarios['fecha'] = salarios['fecha'].replace(fila, fila[0:4])

prom_anual = sql^'''SELECT fecha, AVG(salario) as salarioPromedio, STDDEV(salario) FROM salarios GROUP BY fecha ORDER BY fecha asc'''

prom_anual_provincial = sql^'''SELECT fecha, AVG(salario) as salarioPromedio, STDDEV(salario), id_provincia
                                FROM salarios s
                                INNER JOIN departamentos d 
                                ON s.id_depto = d.id_depto
                                GROUP BY fecha, id_provincia 
                                ORDER BY fecha ASC, id_provincia ASC
                                '''
"""


promedioDesvioNacional =sql ^ """
                SELECT DISTINCT AVG(salario) as salarioPromedio, STDDEV(salario) as desvio,  YEAR(CAST(fecha AS date))
                FROM salarios             
                GROUP BY  YEAR(CAST(fecha AS date))
            """

promedioDesvioProvincial =sql ^ """
                SELECT DISTINCT  YEAR(CAST(fecha AS date)) as año, AVG(salario) as salarioPromedio, STDDEV(salario) as desvio, id_provincia
                FROM salarios
                INNER JOIN departamentos
                ON salarios.id_depto = departamentos.id_depto
                GROUP BY id_provincia,  YEAR(CAST(fecha AS date))
            """
                                
'''
Mostrar, utilizando herramientas de visualización, la siguiente información:

    i) Cantidad de Operadores por provincia.
'''
operadores_por_provincia = sql^'''SELECT DISTINCT d.id_provincia, prov.provincias_nombre, count(*) as cantidadDeOperadores 
                                  FROM padron_operadores p 
                                  INNER JOIN departamentos d 
                                  ON p.id_depto = d.id_depto 
                                  INNER JOIN provincias prov
                                  ON d.id_provincia = prov.id_provincia
                                  GROUP BY d.id_provincia, provincias_nombre
                                  ORDER BY cantidadDeOperadores ASC;
                                  '''
# HAY ALGO RARO CON EL RIGHT OUTER JOIN REVISAR ID_DEPTO
sns.barplot(x = "cantidadDeOperadores", y = "provincias_nombre", data = operadores_por_provincia)
plt.show()
plt.close()

'''
    ii) Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador. 
'''
cant_prod_por_operador = sql^'''SELECT DISTINCT provincias_nombre, count(*) as cantidad
                                FROM produce r
                                INNER JOIN padron_operadores p
                                ON p.razon_social = r.razon_social and p.establecimiento = r.establecimiento
                                INNER JOIN departamentos d
                                ON d.id_depto = p.id_depto
                                INNER JOIN provincias prov
                                ON d.id_provincia = prov.id_provincia
                                GROUP BY r.razon_social, r.establecimiento, provincias_nombre
                                '''
                          
sns.boxplot(x ='cantidad', y ='provincias_nombre', data = cant_prod_por_operador)
plt.show()
plt.close()
                                
'''
    iii) Relación entre cantidad de emprendimientos certificados de cada provincia y el salario promedio en dicha provincia 
    (para la actividad) en el año 2022. En caso de existir más de un salario promedio para ese año, mostrar el último del año 2022.
'''
promedioDesvioProvincial2 = sql^'''SELECT DISTINCT * FROM promedioDesvioProvincial WHERE año = '2022' '''
cant_certif_por_prov = sql^''' SELECT DISTINCT provincias_nombre, count(*)
                                FROM padron_operadores p
                                INNER JOIN departamentos d
                                ON d.id_depto = p.id_depto
                                INNER JOIN provincias prov
                                ON d.id_provincia = prov.id_provincia
                                GROUP BY provincias_nombre,
                                '''

'''
    iv) ¿Cuál es la distribución de los salarios promedio en Argentina? Realicen un violinplot de los salarios promedio por provincia. 
    Grafiquen el último ingreso medio por provincia.
'''

sns.violinplot(data = promedioDesvioProvincial ,
               x = 'id_provincia' , y = 'salarioPromedio' ,  cut=0,  bw=.15).set(xlabel = 'provincia' , ylabel='salarioPromedio')
plt.show()
plt.close()
sns.barplot(x = "id_provincia", y = "salarioPromedio", data = promedioDesvioProvincial2)
plt.show()
plt.close()

