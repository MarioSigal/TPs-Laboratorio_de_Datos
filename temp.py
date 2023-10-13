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
df_CLAE = pd.DataFrame(columns=['clae2', 'clae2_desc','clae3','clae3_desc'])
# relación entre operadores orgánicos y producto
df_R_Produce = pd.DataFrame(columns=['nombre_establecimiento', 'razón_social', 'nombre_producto'])


# Limpieza

limpieza_clae = """
                SELECT DISTINCT clae2, clae2_desc, clae3, clae3_desc
                FROM clae
                WHERE letra == 'A' or (letra == 'C' and clae2 == 10)
                ORDER BY clae2 ASC, clae3 ASC
              """
df_CLAE = sql^limpieza_clae

limpieza_provincia = """
                       SELECT DISTINCT codigo_indec_provincia AS id, nombre_provincia AS nombre
                       FROM localidades
                       ORDER BY id ASC
                     """
df_Provincia= sql^limpieza_provincia

limpieza_departamento1 = """
                         SELECT DISTINCT codigo_indec_departamento AS id, nombre_departamento AS nombre, codigo_indec_provincia AS id_provincia
                         FROM localidades                         
                         ORDER BY id_provincia ASC, id ASC
                        """
df_Departamento = sql^limpieza_departamento1

# Nos aparecieron todas las comunas de CABA juntas por lo que vamos a renombrar
# a las comunas como CABA y su índice será el mayor de los que aparecía

limpieza_departamento2 = """
                         SELECT REPLACE(id,'02001,02002,02003,02004,02005,02006,02007,02008,02009,02010,02011,02012,02013,02014,02015', '02015') as id,
                         REPLACE(nombre,'Comuna 1,Comuna 10,Comuna 11,Comuna 12,Comuna 13,Comuna 14,Comuna 15,Comuna 2,Comuna 3,Comuna 4,Comuna 5,Comuna 6,Comuna 7,Comuna 8,Comuna 9', 'CABA') as nombre, 
                         id_provincia
                         FROM df_Departamento                         
                         ORDER BY id_provincia ASC, id ASC
                        """

df_Departamento = sql^limpieza_departamento2


limpieza_estableciminento1= """
SELECT "razón social" AS razón_social, REGEXP_REPLACE(establecimiento, '\\bNC\\b', 'ESTABLECIMIENTO ÚNICO') AS establecimiento
FROM operadores_organicos
"""

df_Operadores_organicos= sql^limpieza_estableciminento1



# Ejercicio h) ii)
# =============================================================================
# ¿Cuál es el CLAE2 más frecuente en establecimientos productivos?
# Mencionar el Código y la Descripción de dicho CLAE2.
# =============================================================================

