#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:18:26 2023

@author: clinux01
"""
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Ejercicio 1
#Cantidad de establecimientos productivos por provincia
Consultai1_1 = """ 
               SELECT dep.id AS id_departamento, dep.departamento, prov.id AS id_provincia, prov.provincia
               FROM df_Departamento AS dep
               INNER JOIN df_Provincia AS prov
               ON dep.id_provincia = prov.id
               """
Departamento_Provincia = sql^Consultai1_1

Consultai1_2 = """
               SELECT oo.id, dp.provincia
               FROM df_Operadores_organicos AS oo
               INNER JOIN Departamento_Provincia AS dp
               ON oo.id_departamento = dp.id_departamento
               """
op_or_por_provincia = sql^Consultai1_2


op_or_por_provincia['provincia'].value_counts().plot.bar().set(title='Operadores organicos por provincia')
plt.show()
plt.close()


#Ejercicio 2
#Boxplot, por cada provincia, 
#donde se pueda observar la cantidad de productos por operador


Consultai2_1 = """
               SELECT producto, id_op_or, id_provincia
               FROM df_Relacion_Produce
               INNER JOIN df_Operadores_organicos 
               ON id = id_op_or
               """
producto_idop_idporv= sql^Consultai2_1

Consultai2_2 = """
               SELECT id_op_or, provincia, count(*) AS productos_por_operador
               FROM producto_idop_idporv
               INNER JOIN df_Provincia
               ON id_provincia = id
               GROUP BY id_op_or, provincia;
               """

cant_prod_por_prov = sql^Consultai2_2

#como hay datos operadores organicos que producen muchos mas productos del promedio, la visualizacion anterios mustra los datos de manera "desproporcionada" 
#para una visualizacion mas clara usar la variable "cant_prod_por_prov_hasta_10" en vez de "cant_prod_por_prov"

Consultai2_3 = """
               SELECT *
               FROM cant_prod_por_prov
               WHERE productos_por_operador <= 10
               """
cant_prod_por_prov_hasta_10 = sql^Consultai2_3

sns.boxplot(data = cant_prod_por_prov, x = 'provincia' , y = 'productos_por_operador').set(xlabel = 'prvincias' , ylabel='cantidad de productos por operador')
plt.xticks(rotation = 90)
plt.show()
plt.close()


#Ejercicio 3

#Relación entre cantidad de establecimientos de operadores orgánicos 
#certificados de cada provincia y la proporción de mujeres empleadas en
#establecimientos productivos de dicha provincia. Para este punto deberán
#generar una tabla de equivalencia, de manera manual, entre la letra de CLAE
#y el rubro de del operador orgánico.

# los establecimientos productivos que tienen clae 2 e {1,2,3,10,20,21} ya los tengo, son los del df_Establecimiento_productivo

# vamos de nuevo

#Cantidad de establecimientos productivos por provincia
Consultai3_1 = """ 
               SELECT dep.id AS id_departamento, dep.departamento, prov.id AS id_provincia, prov.provincia
               FROM df_Departamento AS dep
               INNER JOIN df_Provincia AS prov
               ON dep.id_provincia = prov.id
               """
Departamento_Provincia = sql^Consultai3_1

Consultai3_2 = """
               SELECT dp.provincia, count(dp.provincia) AS cantidad
               FROM df_Operadores_organicos AS oo
               INNER JOIN Departamento_Provincia AS dp
               ON oo.id_departamento = dp.id_departamento
               GROUP BY provincia
               """
cantidad_op_or_por_provincia = sql^Consultai3_2

# proporcion de mujeres por provincia

Consultai3_3 = """
               SELECT DISTINCT AVG(ep.proporcion_mujeres) AS proporcion_mujeres, dp.provincia
               FROM df_Establecimiento_productivo AS ep
               INNER JOIN Departamento_Provincia AS dp
               ON ep.id_departamento = dp.id_departamento
               GROUP BY dp.provincia
               """
proporcion_mujeres_por_provincia = sql^Consultai3_3

Consultai3_4 = """
               SELECT p.proporcion_mujeres, c.cantidad, c.provincia
               FROM cantidad_op_or_por_provincia AS c
               LEFT OUTER JOIN proporcion_mujeres_por_provincia AS p
               ON c.provincia = p.provincia
               """
proporcion_cantidad_provincia = sql^Consultai3_4


sns.scatterplot(data=proporcion_cantidad_provincia, x="cantidad", y="proporcion_mujeres", hue="provincia")
x_coord = 1.1  # Coordenada X
y_coord = 0.5  # Coordenada Y
plt.legend(loc='center left', bbox_to_anchor=(x_coord, y_coord))
plt.show()
#Ejercicio 4
#¿Cuál es la distribución de los datos correspondientes a la proporción de
#mujeres empleadas en establecimientos productivos en Argentina? 
#Realicen un violinplot por cada provincia. Mostrarlo en un solo gráfico.
Consultai4_1 = """ 
               SELECT dep.id AS id_departamento, dep.departamento, prov.id AS id_provincia, prov.provincia
               FROM df_Departamento AS dep
               INNER JOIN df_Provincia AS prov
               ON dep.id_provincia = prov.id
               """
Departamento_Provincia = sql^Consultai4_1

Consultai4_2 = """
               SELECT ep.proporcion_mujeres, dp.provincia
               FROM df_Establecimiento_productivo AS ep
               INNER JOIN Departamento_Provincia AS dp
               ON ep.id_departamento = dp.id_departamento
               """
proporcion_mujeres_provincia = sql^Consultai4_2

sns.violinplot(data = proporcion_mujeres_provincia, x = 'provincia' , y = 'proporcion_mujeres').set(xlabel = 'provincias' , ylabel='proporcion de mujeres')
plt.xticks(rotation = 90)
plt.show()
plt.close()
