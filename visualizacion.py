#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:18:26 2023

@author: clinux01
"""

#visualizacion

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
#donde se pueda observar la cantidad deproductos por operador

Consutai2_1 = """
SELECT 
"""

Consultah1_1 = """
SELECT producto, id
FROM df_Relacion_Produce
INNER JOIN df_Operadores_organicos 
ON id = id_op_or
"""
Producto_Departamento = sql^Consultah1_1

#Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador
#sns.boxplot(data = df ,
#               x = 'species' , y = 'body_mass_g' , hue = 'sex').set(xlabel = 'especie' , ylabel='masa(g)')
#plt.show()
#plt.close()


#Ejercicio 3

#Relación entre cantidad de establecimientos de operadores orgánicos 
#certificados de cada provincia y la proporción de mujeres empleadas en
#establecimientos productivos de dicha provincia. Para este punto deberán
#generar una tabla de equivalencia, de manera manual, entre la letra de CLAE
#y el rubro de del operador orgánico.


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

sns.violinplot(data = proporcion_mujeres_provincia,
               x = 'provincia' , y = 'proporcion_mujeres').set(xlabel = 'provincias' , ylabel='proporcion de mujeres')
plt.xticks(rotation = 90)
plt.show()
plt.close()