from inline_sql import sql
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#categorias.csv      departamentos.csv  establecimiento_rubro.csv  localidades_censales.csv  padron_operadores.csv  produce.csv    provincias.csv  salarios.csv
#certificadoras.csv  dicc_clases.csv    letra.csv                  municipios.csv            paises.csv             productos.csv  rubros.csv

padron_operadores = pd.read_csv('./TablasLimpias/padron_operadores.csv')
departamentos = pd.read_csv('./TablasLimpias/departamentos.csv')
provincias = pd.read_csv('./TablasLimpias/provincias.csv')
produce = pd.read_csv('./TablasLimpias/produce.csv')
productos = pd.read_csv('./TablasLimpias/productos.csv')
salarios = pd.read_csv('./TablasLimpias/salarios.csv')
establecimiento_rubro = pd.read_csv('./TablasLimpias/establecimiento_rubro.csv')

# Cantidad de operadores por provincia

df = sql^ ''' SELECT * FROM padron_operadores NATURAL JOIN departamentos NATURAL JOIN provincias '''

sns.countplot(y=df['provincia_nombre']).set(title='Cant. Operadores por provincia')
plt.show()
plt.close()

# Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador.
#sns.boxplot



# Relación entre cantidad de emprendimientos certificados de cada provincia y el salario promedio en dicha provincia (para la actividad) en el año 2022. En
#caso de existir más de un salario promedio para ese año, mostrar el último del año 2022.

provdepto = sql ^ """ SELECT *

                    FROM padron_operadores as p1

                    INNER JOIN departamentos as d1

                    ON p1.id_depto = d1.id_depto

                    INNER JOIN provincias

                    ON provincias.id_provincia = d1.id_provincia

                """

ultimoSalario = sql ^ """
                    SELECT *
                    FROM salarios 
                    WHERE MONTH(CAST(fecha AS date)) = '12'
                    """

consultaSQL3 = """
                SELECT DISTINCT provincia_nombre, count(*) as cantidadEmpC, AVG(salario) as salarioPromedio
                FROM padron_operadores AS p1
                NATURAL JOIN departamentos 
                NATURAL JOIN provincias
                NATURAL JOIN ultimoSalario
                INNER JOIN establecimiento_rubro as e1
                ON p1.razon_social = e1.razon_social AND p1.establecimiento = e1.establecimiento
                WHERE fecha LIKE '2022%'
                GROUP BY provincia_nombre, rubros;
            """

relacionCantidadSalario = sql ^ consultaSQL3
df = sql ^ consultaSQL3

sns.set_style('whitegrid')
ax1 = sns.barplot(x='provincia_nombre', y='salarioPromedio', data=df, color='blue')
ax2 = ax1.twinx()
sns.barplot(x='provincia_nombre', y='cantidadEmpC', data=df, color='red')

#ax1.set_ylim([0, max(salarios) * 1.2])
#ax2.set_ylim([0, max(productores) * 2])

ax1.set_title('Relación entre salario promedio y cantidad de emprendimientos certificados')
ax1.set_xlabel('Provincia')
ax1.set_ylabel('Salario promedio')
ax2.set_ylabel('Cantidad de emprendimientos certificados')

plt.show()

sns.barplot(x='provincia_nombre', y='salarioPromedio', data=df, color='blue')
sns.barplot(x='provincia_nombre', y='cantidadEmpC', data=df, color='red')
#sns.lineplot(data=df, x='cantidadEmpC', y='salarioPromedio', hue='provincia_nombre')
#sns.barplot(data = df, x = 'provincia_nombre', y = 'cantidadEmpC', hue = 'salarioPromedio')
plt.show()
plt.close()

sns.scatterplot(data=relacionCantidadSalario, x="salarioPromedio", y="cantidadEmpC", hue = "provincia_nombre", palette = "viridis").legend(framealpha=0.25,loc=[-0.75,0.05])
plt.show()
plt.close()


# ¿Cuál es la distribución de los salarios promedio en Argentina? Realicen un violinplot de 
# los salarios promedio por provincia. Grafiquen el último ingreso medio por provincia.
