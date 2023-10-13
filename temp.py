# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from inline_sql import sql, sql_val

operadores_organicos= pd.read_csv('padron-de-operadores-organicos-certificados.csv')
# =============================================================================
#
# Listado de operadores orgánicos certificados:
#  
# incluye a: productores primarios, elaboradores y comercializadores.
#
# =============================================================================



establecimientos_productivos = pd.read_csv('distribucion_establecimientos_productivos_sexo.csv')
# =============================================================================
#
# Distribución geográfica de los establecimientos productivos.
# 
# Base de datos que contiene coordenadas de los establecimientos productivos (no necesariamente orgánicos) con su 
# respectiva actividad económica, su nivel de empleo, jurisdicción y proporción de mujeres
#
# =============================================================================

localidades = pd.read_csv('localidad_bahra.csv')
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

clae = pd.read_csv('clae_agg.csv')

# =============================================================================
# 
# Diccionario de CLAE: 
# 
# Dicha fuente contiene los nomencladores utilizados por AFIP
# para clasificar actividades con su correspondiente descripción.
# permite asociar a la fuente primaria “establecimiento productivo” los datos de actividades.
# 
# =============================================================================


# Ejercicio h) i)
consultaSQL = """
                   SELECT provincia, Replace(REPLACE(REPLACE(REPLACE(productos,':',','), ' Y ',', '),'+',','),'-',',') AS productos
                   FROM operadores_organicos;
                 """
provincias_productos = sql^consultaSQL

#no se usa
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


consultaSQL4= """
SELECT provincia, producto, COUNT(*) AS cantidad
FROM provincia_producto3
GROUP BY provincia, producto
ORDER BY cantidad DESC, producto Desc;
"""
provincia_producto4= sql^consultaSQL4

#algunos quedaron con parentesis al pricipio o al finalpor ejemplo el caso de HORTICULTURA, (RAIZ, HOJAS, FRUTOS) , FRUTALES, (CAROZO, PEPITA, CITRICOS), deberia de ahora en este punto,borrar los parentesis, pero tambien se borrarian de el cas CHIA (SALVIA HISPANICA L)

# Ejercicio e)

df_Operadores_organicos = pd.DataFrame(columns=['nombre_establecimiento', 'razón_social', 'rubro', 'id_departamento'])
df_Producto = pd.DataFrame(columns=['nombre', 'clae3']) 
df_Departamento = pd.DataFrame(columns=['id', 'nombre', 'id_provincia'])
df_Provincia = pd.DataFrame(columns=['id', 'nombre'])
df_Establecimiento_productivo = pd.DataFrame(columns=['id', 'proporción_mujeres', 'clae6'])
df_CLAE = pd.DataFrame(columns=['clae3','clae2'])
# relación entre operadores orgánicos y producto
df_R_Produce = pd.DataFrame(columns=['nombre_establecimiento', 'razón_social', 'nombre_producto'])

# Ejercicio h) ii)
# =============================================================================
# ¿Cuál es el CLAE2 más frecuente en establecimientos productivos?
# Mencionar el Código y la Descripción de dicho CLAE2.
# =============================================================================

