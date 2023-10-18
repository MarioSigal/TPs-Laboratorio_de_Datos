#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:18:26 2023

@author: clinux01
"""

#visualizacion

#Visualización

# Ejercicio i)

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
               FROM producto_idop_prov
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

#como separamos a los operadores organicos por clae 2, decidimos quedarnos con los establecimientos productivos que tengan la misma clae2, pues clae2 es mas restrictiva que clae Letra entonces seguimos cumpliendo el objetivo del ejercicio
#si un operador organico produce dos o mas productos con distnta clae2 decidimos tomarlos como operadores organicos distintos

#entonces como dijo jack el destripador, vamos por partes (meme de una de las clases)

#juntar clae con producto
#ya esta en df producto

#juntar clae con operador organico
#df_producto -inner join- df_realcion_produce -INNER JOIN- df_operadororganico

Consultai3_1 = """
               SELECT DISTINCT prod.clae2, rel.id_op_or
               FROM df_Producto AS prod
               INNER JOIN df_Relacion_Produce AS rel
               ON prod.producto = rel.producto
               """
clae2_idopor = sql^Consultai3_1 

Consultai3_2 = """
               SELECT DISTINCT clae2, id_op_or, id_departamento
               FROM clae2_idopor
               INNER JOIN df_Operadores_organicos
               ON id_op_or = id
               """
clae2_idopor_idprov = sql^Consultai3_2

# bueno me acabo de dar cuenta que lo anterior no era recesario xd

# busco.... ya no se lo que busco.... estoy cansado jefe.....
# busco los establecimientos productivos que tienen clae 2 entre 1,2,3,10,20,21, ya los tengo, son los del df_Establecimiento_productivo

# entonces es mucho mas facil de lo que pensaba


#uno departamento_provincia
Consultai3_4 = """ 
               SELECT dep.id AS id_departamento, dep.departamento, prov.id AS id_provincia, prov.provincia
               FROM df_Departamento AS dep
               INNER JOIN df_Provincia AS prov
               ON dep.id_provincia = prov.id
               """
Departamento_Provincia = sql^Consultai3_4


#me quedo con los operadores organicos por provincia, teniendo en cuenta lo que pueden tener claes distintas(saco clae 999)
Consultai3_3 = """
               SELECT DISTINCT c2oo.clae2, c2oo.id_op_or, dp.provincia
               FROM clae2_idopor_idprov AS c2oo
               INNER JOIN Departamento_Provincia AS dp
               ON c2oo.id_departamento = dp.id_departamento
               WHERE clae2 != 999
               """
op_or_por_provincia = sql^Consultai3_3



#proporcion de mujeres empleadas en establecimientos productivos en cada provincia
Consultai3_5 = """
               SELECT DISTINCT ep.id, ep.clae2, ep.proporcion_mujeres, dp.provincia
               FROM df_Establecimiento_productivo AS ep
               INNER JOIN Departamento_Provincia AS dp
               ON ep.id_departamento = dp.id_departamento
               """
est_prod_por_provincia = sql^Consultai3_5

#promedio de proporcion de mujeres por



# vamos de nuevo


# cantidad de estabelcimientos productivos por provincia

#Cantidad de establecimientos productivos por provincia
Consultai1_1 = """ 
               SELECT dep.id AS id_departamento, dep.departamento, prov.id AS id_provincia, prov.provincia
               FROM df_Departamento AS dep
               INNER JOIN df_Provincia AS prov
               ON dep.id_provincia = prov.id
               """
Departamento_Provincia = sql^Consultai1_1

Consultai1_2 = """
               SELECT dp.provincia, count(dp.provincia)AS cantidad
               FROM df_Operadores_organicos AS oo
               INNER JOIN Departamento_Provincia AS dp
               ON oo.id_departamento = dp.id_departamento
               GROUP BY provincia
               """
op_or_por_provincia = sql^Consultai1_2















sns.scatterplot(data=tips, x="proporcion de mujeres", y="cantidad de operadores organicos", hue="provincias")

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

plt.show()
plt.close()






