# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from inline_sql import sql, sql_val

operadores_organicos= pd.read_csv('./TablasOriginales/padron-de-operadores-organicos-certificados.csv')
# =============================================================================
#
# Listado de operadores orgánicos certificados:
#  
# incluye a: productores primarios, elaboradores y comercializadores.
#
# =============================================================================



establecimientos_productivos = pd.read_csv('./TablasOriginales/distribucion_establecimientos_productivos_sexo.csv')
# =============================================================================
#
# Distribución geográfica de los establecimientos productivos.
# 
# Base de datos que contiene coordenadas de los establecimientos productivos (no necesariamente orgánicos) con su 
# respectiva actividad económica, su nivel de empleo, jurisdicción y proporción de mujeres
#
# =============================================================================

localidades = pd.read_csv('./TablasOriginales/localidad_bahra.csv')
# =============================================================================
#
# Localidades de la Base de Asentamientos Humanos de la República Argentina
#
# Esta fuente permite asociar a la fuente primaria “Padrón de Operadores Orgánicos
# Certificados” con los datos de departamento. Lamentablemente la fuente primaria,
# en su campo departamento parece mezclar datos de departamento y ciudad, entre
# otras cosas. Esa fuente también tiene inconvenientes en cuanto al formato y
# escritura de los nombres (por ejemplo, no parecen contar con tildes, etc.). Deberán
# hacer lo necesario para curar y vincular los datos.
# 
# =============================================================================

clae = pd.read_csv('./TablasOriginales/clae_agg.csv')

# =============================================================================
# 
# Diccionario de CLAE: 
# 
# Dicha fuente contiene los nomencladores utilizados por AFIP
# para clasificar actividades con su correspondiente descripción.
# permite asociar a la fuente primaria “establecimiento productivo” los datos de actividades.
# 
# =============================================================================



consultaSQL = """
                   SELECT provincia, Replace(REPLACE(REPLACE(REPLACE(productos,':',','), ' Y ',', '),'+',','),'-',',') AS productos
                   FROM operadores_organicos;
                 """
provincias_productos = sql^consultaSQL
cunsultaSQL2 = """
                SELECT provincia, string_to_array(productos, ',') AS producto, COUNT(*) AS cantidad
                FROM provincias_productos
                GROUP BY provincia, producto
                ORDER BY cantidad DESC;
                """
provincias_productos2= sql^cunsultaSQL2
#string_to_array, es como split pero es SQL
#UNNEST es para pasar de datos en lista a datos por separado(semi normalizar a forma 1)
#TRIM es para borrar los espacios a los costados de los datos, para comparar bien en el count
#hay alguna otra forma de hacerlo?
consultaSQL3 = """
 SELECT provincia, TRIM(UNNEST( string_to_array(productos, ','))) AS producto
 FROM provincias_productos
"""
provincia_producto3= sql^consultaSQL3
ok= sql^consultaSQL  
consultaSQL4 = """ 
SELECT DISTINCT provincia, producto
FROM provincia_producto3
"""

provincia_producto4 = sql^consultaSQL4

consultaSQL5= """
SELECT provincia, producto AS producto, COUNT(*) AS cantidad
FROM provincia_producto3
GROUP BY provincia, producto
ORDER BY cantidad DESC;
"""
provincia_producto5= sql^consultaSQL5

#algunos quedaron con parentesis al pricipio o al finalpor ejemplo el caso de HORTICULTURA, (RAIZ, HOJAS, FRUTOS) , FRUTALES, (CAROZO, PEPITA, CITRICOS), deberia de ahora en este punto,borrar los parentesis, pero tambien se boorarian de el cas CHIA (SALVIA HISPANICA L)