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
padron_operadores = pd.read_csv('./TablasLimpias/padron_operadores.csv')

# Cantidad de operadores por provincia

df = sql^ ''' SELECT * FROM padron_operadores NATURAL JOIN departamentos NATURAL JOIN provincias '''

sns.countplot(y=df['provincia_nombre']).set(title='Cant. Operadores por provincia')
plt.show()
plt.close()

# Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador.
#sns.boxplot



# Relación entre cantidad de emprendimientos certificados de cada provincia y el salario promedio en dicha provincia (para la actividad) en el año 2022. En
#caso de existir más de un salario promedio para ese año, mostrar el último del año 2022.


# ¿Cuál es la distribución de los salarios promedio en Argentina? Realicen un violinplot de 
# los salarios promedio por provincia. Grafiquen el último ingreso medio por provincia.
